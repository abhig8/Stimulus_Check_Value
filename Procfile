heroku ps:scale web=1 worker=5 web: gunicorn --bind 0.0.0.0:$PORT wsgi:app worker: python src/updater.py