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

        urls = sess.query('url').from_statement('SELECT url FROM song')
	votes = sess.query('votes').from_statement('SELECT votes FROM song')

	#For every song in the queue grab the video ID and number of votes
        videoIDs = [url[0].partition('v=')[2][:11] for url in urls.all()]
	votesList = [int(vote[0]) for vote in votes]
	dbHashmap = dict()
	dbHashmap.setdefault('null',-1)

	#dbHashmap[value] = key
	i = 0
	maxVotes = -1
	for id in videoIDs:
		dbHashmap[votesList[i]] = id
		if maxVotes < votesList[i]:
			maxVotes = votesList[i]
		i += 1

        if index < len(dbHashmap):
        	ws.send(json.dumps({'output': dbHashmap.get(maxVotes)}))
		#sess.delete(Song.query.filter_by(url=dbHashmap.values()[index]).first())
		#sess.commit()
		index += 1
        else:
        	ws.send(json.dumps({'output': dbHashmap.values()[0]}))
        	index = 1

