install:
	sudo apt-get install python -y
	sudo apt-get install python-dev -y
	sudo apt-get install python-setuptools -y
	sudo easy_install pip
	sudo pip install Flask
	sudo pip install Flask-SQLAlchemy
	sudo pip install gevent-websocket
	sudo pip install -r requirements.txt	

del:
	sudo python manage.py delete_db

new:
	sudo python manage.py create_db

seed:
	sudo python manage.py seed_db --seedfile data/db_items.json
	sudo python manage.py seed_db --seedfile data/db_items2.json

reset:
	sudo make del
	sudo make new
	sudo make seed
