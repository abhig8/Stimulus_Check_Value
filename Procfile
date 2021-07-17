worker: python3 -m src.updater
web: newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT run_server:app