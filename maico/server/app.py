import json
import os
import pickle
import time

import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options
from tornado.web import url

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
    idx = 0

    def open(self, *args, **kwargs):
        print('on open')
        observers.add(self)

    def on_message(self, message):
        message_d = tornado.escape.json_decode(message)
        print(message_d)
        print(dir(message_d))
        if 'action' in message_d and isinstance(message_d, dict):
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
                # for browser in self.browsers:
                #   browser.write_message({'action': 'pepper_eye', 'data': b64_img})
            elif action == 'robot_talk':
                import urllib.parse
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
            from maico.server.data_processor import FirstActionHandModel, TrainingHandler
            model = FirstActionHandModel()
            TrainingHandler.model = model
            predicted = json.loads(TrainingHandler.predict(message))
            print(predicted)
            message = {'action': 'update_chart',
                       'data': {'value': round(predicted['prediction']['probability'], 3), 'time': self.idx}}
            observers.notify_msg(message)
            if predicted['prediction']['execution']:
                import urllib.parse
                self.send_to_robot(action='robot_talk', data=urllib.parse.quote('\rspd=200\なまむぎなまごめなまたまご'))
            self.idx += 1

    def on_close(self):
        print('on close')
        observers.remove(self)

    def send_to_robot(self, action, data):
        for robot in self.robots:
            robot.write_message({'action': action, 'data': data})


class Bot(object):
    def __init__(self):
        self.state = 0
        self.file_name = 'state.pkl'

    def generate_response(self, usr_utt):
        if self.state == 0:
            utt = 'こんにちは'
        elif self.state == 1:
            utt = '私はボットです。'
        elif self.state == 2:
            utt = '状態を記憶しています。'
        else:
            utt = 'ありがとう'
        self.state += 1
        return {'utt': utt}

    def read_states(self):
        try:
            with open(self.file_name, 'rb') as f:
                states = pickle.load(f)
        except FileNotFoundError as e:
            print(e.strerror)
            states = {}
        except EOFError:
            states = {}
        return states

    def read_state(self, session_id):
        states = self.read_states()
        self.state = states.get(session_id)

    def write_state(self, session_id):
        states = self.read_states()
        states[session_id] = self.state
        with open(self.file_name, 'wb') as f:
            pickle.dump(states, f)


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

        if not self.get_cookie(self.cookie_name):
            sessioin_id = str(time.time())
            self.set_cookie(self.cookie_name, sessioin_id)
        else:
            sessioin_id = self.get_cookie(self.cookie_name)
            self.set_cookie(self.cookie_name, sessioin_id)
            bot.read_state(sessioin_id)
        return bot, sessioin_id

    def post(self, *args, **kwargs):
        bot, session_id = self.create_or_read_bot()
        usr_utt = tornado.escape.json_decode(self.request.body.decode('utf-8'))
        sys_utt = bot.generate_response(usr_utt)
        bot.write_state(session_id)
        observers.notify_msg(msg={'action': 'user_utt', 'data': usr_utt['usr_utt']})
        return self.write(json.dumps(sys_utt))


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings = {}
settings['debug'] = options.debug
settings['static_path'] = os.path.join(BASE_DIR, 'static')
settings['template_path'] = os.path.join(BASE_DIR, 'templates')

application = tornado.web.Application([
    url(r'/', Index, name='index'),
    url(r'/observation', Observation),
    url(r'/dialog', Dialog),
],
    **settings
)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()