web: gunicorn orders.wsgi:application --log-file - --log-level debug
python orders/manage.py collectstatic --noinput
orders/manage.py migrate
