run:
	python manage.py runserver

test:
	python manage.py test

shell:
	python manage.py shell

migrate:	
	python manage.py makemigrations && python manage.py migrate
