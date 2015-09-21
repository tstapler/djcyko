# coding: utf-8
import json
import time
from sqlalchemy import *
from sqlalchemy.orm import *
Session = sessionmaker()
engine = create_engine('sqlite:////tmp/angular_flask.db')
Session.configure(bind=engine)
sess=Session()

def handle_websocket(ws, url='xjB7J9dOtSM'):
    index = 0
    while True:

        # ws.receive seems to block until a message comes through
        message = ws.receive()
        if message is None: #if message is none, it probably timed out
            break
        else:
            message = json.loads(message)

        q = sess.query('url').from_statement('SELECT url from song')
        #For every song in the queue grab the vidid
        vids = [x[0].partition('v=')[2][:11] for x in q.all()]

        if index < len(vids):
            ws.send(json.dumps({'output': vids[index]}))
            index += 1
        else:
            ws.send(json.dumps({'output': vids[0]}))
            index = 1

