import json
import os
import time
import urllib.parse
from collections import defaultdict

import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options
from tornado.web import url

from maico.server.dialogue_system.bot import Bot
from maico.server.utils.data_processor import FirstActionHandModel, TrainingHandler

define('debug', default=True, help='debug mode')


class Index(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        return self.render('index.html')


class Observers(object):
    def __init__(self):
        self.observers = set()

    def add(self, el):
        self.observers.add(el)

    def remove(self, el):
        self.observers.remove(el)

    def notify_msg(self, msg):
        for observer in self.observers:
            observer.write_message(msg)


observers = Observers()


class Observation(tornado.websocket.WebSocketHandler):
    """
    observers can watch human-machine dialog.
    And judge whether speak to or not.
    """
    robots = set()
    browsers = set()
    models = {}

    def open(self, *args, **kwargs):
        print('on open')
        observers.add(self)

    def on_message(self, message):
        message_d = tornado.escape.json_decode(message)
        print(message_d)
        if 'action' in message_d and isinstance(message_d, dict):
            message = message_d
            action = message['action']
            data = message['data']
            if action == 'update_chart':
                observers.notify_msg(message)
            elif action == 'browser_token':
                self.browsers.add(self)
            elif action == 'robottoken':
                self.robots.add(self)
            elif action == 'robot_action':
                self.send_to_robot(action='robot_action', data=data)
            elif action == 'pepper_eye':
                # ここだけ情報の流れがPepper -> browser
                _, _, b64_img, _ = data.split('||||')
                observers.notify_msg({'action': 'pepper_eye', 'data': b64_img})
            elif action == 'robot_talk':
                self.send_to_robot(action='robot_talk', data=urllib.parse.quote(data))
            elif action == 'get_token':
                self.send_to_robot(action='get_token', data=data)
            elif action == 'actioncomplete':
                pass
            elif action == 'get_token':
                self.send_to_robot(action=action, data='connection_token')
            elif action == 'send_access_token':
                self.send_to_robot(action='success_connection', data=data)
        elif 'feature' in message_d:
            target_id = message_d['_id']

            if target_id not in self.models:
                if Bot.in_automatic_dialog == False:
                    self.send_to_robot(action='robot_talk', data=urllib.parse.quote('いらっしゃいませー'))
                self.models[target_id] = FirstActionHandModel()

            model = self.models[target_id]
            # self.sensing_data[target_id].append(message_d)  # do not need to store the sensing datas. it consume the memory
            TrainingHandler.model = model  # it is dirty way. must implements predict method in this handler
            predicted = json.loads(TrainingHandler.predict(message))
            message = {'action': 'update_chart',
                       'data': {'value': round(predicted['prediction']['probability'], 3),
                                'time': message_d['timestamp'],
                                'id': target_id,
                                },
                       }
            observers.notify_msg(message)
            if predicted['prediction']['execution'] and Bot.in_automatic_dialog == False:
                msg = '時期はいつ頃とかありますか？'
                self.send_to_robot(action='robot_talk', data=urllib.parse.quote(msg))
                observers.notify_msg(msg={'action': 'system_utt', 'data': msg})
                Bot.in_automatic_dialog = True

    def on_close(self):
        print('on close')
        observers.remove(self)

    def send_to_robot(self, action, data):
        for robot in self.robots:
            robot.write_message({'action': action, 'data': data})


class Dialog(tornado.web.RequestHandler):
    """
    do dialog
    if user utterance is POSTed, response system utterance.
    state management by session
    if user utterance is POSTed and system utterance is generated,
    distribute those to observers.
    """
    cookie_name = "session_id"

    def create_or_read_bot(self):
        bot = Bot()
        session_id = str(time.time())
        return bot, session_id
        """
        if not self.get_cookie(self.cookie_name):
            sessioin_id = str(time.time())
            self.set_cookie(self.cookie_name, sessioin_id)
        else:
            sessioin_id = self.get_cookie(self.cookie_name)
            self.set_cookie(self.cookie_name, sessioin_id)
            bot.read_state(sessioin_id)
        return bot, sessioin_id
        """

    bot = Bot()

    def post(self, *args, **kwargs):
        # bot, session_id = self.create_or_read_bot()
        usr_utt = tornado.escape.json_decode(self.request.body.decode('utf-8'))
        observers.notify_msg(msg={'action': 'user_utt', 'data': usr_utt['usr_utt']})
        if Bot.in_manual_dialog:
            return self.write(json.dumps({'utt': ''}))
        sys_utt = self.bot.reply(usr_utt['usr_utt'])
        #bot.write_state(session_id)
        if sys_utt['utt'] == 'pass':
            observers.notify_msg(msg={'action': 'change_operator', 'data': sys_utt['utt']})
            Bot.in_manual_dialog = True
            return self.write(json.dumps({'utt': '少々お待ち下さいね'}))
        else:
            observers.notify_msg(msg={'action': 'system_utt', 'data': sys_utt['utt']})
            return self.write(json.dumps(sys_utt))


class Reset(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        Bot.in_manual_dialog = False
        Bot.in_automatic_dialog = False


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings = {}
settings['debug'] = options.debug
settings['static_path'] = os.path.join(BASE_DIR, 'static')
settings['template_path'] = os.path.join(BASE_DIR, 'templates')

application = tornado.web.Application([
    url(r'/', Index, name='index'),
    url(r'/observation', Observation),
    url(r'/dialog', Dialog),
    url(r'/reset', Reset),
],
    **settings
)

if __name__ == '__main__':
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()