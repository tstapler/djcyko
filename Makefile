install:
	apt-get install python-dev -y
	apt-get install bcrypt -y
	pip install scrapy
	apt-get install libffi-dev libssl-dev libxml2-dev libxslt1-dev -y
	pip install Flask-JWT
	pip install -r requirements.txt

del:
	python manage.py delete_db

new:
	python manage.py create_db

seed:
	python manage.py seed_db --seedfile data/users.json
	python manage.py seed_db --seedfile data/queues.json
	python manage.py seed_db --seedfile data/songs.json

reset:
	make del
	make new
	make seed
