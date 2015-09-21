del:
	python manage.py delete_db
new:
	python manage.py create_db
seed:
	python manage.py seed_db --seedfile data/db_items.json
reset:
	python manage.py delete_db
	python manage.py create_db
	python manage.py seed_db --seedfile data/db_items.json
	python manage.py seed_db --seedfile data/db_items2.json
