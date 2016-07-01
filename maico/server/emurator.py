# -*- coding: utf-8 -*-
import _thread
import json

import websocket


def on_message(ws, message):
    print(message)
    message = json.loads(message)


#    ws.send(json.dumps(message))

def on_error(ws, error):
    print(error)


def on_close(ws):
    print("on closed")


def on_open(ws):
    def run(*args):
        ws.send(json.dumps({'action': 'robottoken', 'data': 'none'}))
        import os
        import time
        from maico.server.data_processor import SensingHandler
        i = 1
        SENSING_FILE = os.path.join(os.path.dirname(__file__), "../../tests/samples/sensing_protocol_samples.txt")
        SensingHandler.set_watch_file(SENSING_FILE)

        while True:
            # d = random.random()
            ln = SensingHandler.file_read()
            ws.send(json.dumps(ln))
            # ws.send(json.dumps({'action': 'update_chart', 'data': {'year': i, 'value': d}}))
            time.sleep(1)
            # i += 1

    _thread.start_new_thread(run, ())


if __name__ == "__main__":
    url = 'ws://localhost:8888/observation'
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
