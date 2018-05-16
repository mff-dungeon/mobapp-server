web: gunicorn server.wsgi --log-file -

debugweb: ./manage.py runserver
migrate: ./manage.py makemigrations && ./manage.py migrate
