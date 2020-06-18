#!/bin/bash
python manage.py makemigrations
python manage.py migrate                  # Apply database migrations
#python manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &

echo Starting Gunicorn.

termination()
{
  echo "Terminating daemons ..." >> /var/log/run.log
  exit $?
}

echo "Running daemons ..." > /var/log/run.log

trap termination SIGINT

cd /srv/mstwebapp
gunicorn mstwebapp.wsgi:application \
    --name mstwebapp \
    --bind 0.0.0.0:80 \
    --workers 4 \
    --log-level=info \
    --log-file=/srv/logs/gunicorn.log \
    --access-logfile=/srv/logs/access.log \
    "$@"

#while true
#do
#  sleep 1000
#done

