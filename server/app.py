import base64
import json
import os
import random

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.web import url


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        user_id = random.randint(0, 100)
        self.render('index.html', user_id=user_id)


class ChatHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    messages = []

    def open(self, *args, **kwargs):
        self.waiters.add(self)
        self.write_message({'messages': self.messages})

    def on_message(self, message):
        message = json.loads(message)
        self.messages.append(message)
        for waiter in self.waiters:
            if waiter == self:
                continue
            waiter.write_message({'id': message['id'], 'message': message['message']})

    def on_close(self):
        self.waiters.remove(self)


class PepperController(tornado.websocket.WebSocketHandler):
    browsers = set()
    robots = set()

    def open(self, *args, **kwargs):
        print("on open")
        self.browsers.add(self)
        self.write_message({'action': 'get_token', 'data': '123456'})

    def on_message(self, message):
        message = json.loads(message)
        # print('Received: {0}'.format(message))
        action = message['action']
        data = message['data']
        if action == 'browser_token':
            self.browsers.add(self)
        elif action == 'robottoken':
            self.robots.add(self)
        elif action == 'robot_action':
            self.send_to_robot(action='robot_action', data=data)
        elif action == 'pepper_eye':
            # ここだけ情報の流れがPepper -> browser
            _, _, b64_img, _ = data.split('||||')
            for browser in self.browsers:
                browser.write_message({'action': 'pepper_eye', 'data': b64_img})
        elif action == 'robot_talk':
            import urllib.parse
            self.send_to_robot(action='robot_talk', data=urllib.parse.quote(data))
        elif action == 'get_token':
            self.send_to_robot(action='get_token', data=data)
        elif action == 'actioncomplete':
            pass
            # self.send_to_robot()
        elif action == 'get_token':
            self.send_to_robot(action=action, data='connection_token')
        elif action == 'send_access_token':
            self.send_to_robot(action='success_connection', data=data)
        elif action == 'product_img':
            path, _ = data.split('?')
            img_file = path.replace('/static/', 'static/')
            b64 = base64.encodestring(open(img_file, "rb").read())
            sendData = 'data:image/jpeg;base64,' + b64.decode('utf8')
            self.send_to_robot(action=action, data=sendData)
        else:
            pass

    def on_close(self):
        print('on close')
        if self in self.browsers:
            self.browsers.remove(self)
        else:
            self.robots.remove(self)

    def send_to_robot(self, action, data):
        for robot in self.robots:
            robot.write_message({'action': action, 'data': data})



class Application(tornado.web.Application):
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        tornado.web.Application.__init__(self,
                                         [
                                             url(r'/', IndexHandler, name='index'),
                                             url(r'/chat', ChatHandler, name='chat'),
                                         ],
                                         template_path=os.path.join(BASE_DIR, 'templates'),
                                         static_path=os.path.join(BASE_DIR, 'static'),
                                         )


if __name__ == '__main__':
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
