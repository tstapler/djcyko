install:
	sudo apt-get install python -y
	sudo apt-get install python-dev -y
	sudo apt-get install python-setuptools -y
	sudo easy_install pip
	sudo pip install Flask
	sudo pip install gevent-websocket
	sudo pip install -r requirements.txt

del:
	python manage.py delete_db

new:
	python manage.py create_db

seed:
	python manage.py seed_db --seedfile data/db_items.json
	python manage.py seed_db --seedfile data/db_items2.json

reset:
	make del
	make new
	make seed
