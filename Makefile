install:
	pip install -r requirements.txt

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
