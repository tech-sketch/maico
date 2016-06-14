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
