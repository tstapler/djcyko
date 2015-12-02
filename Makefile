install:
	pip install scrapy
	apt-get install libffi-dev libssl-dev libxml2-dev libxslt1-dev
	pip install -r requirements.txt

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
