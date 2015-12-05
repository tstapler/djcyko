install:
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
