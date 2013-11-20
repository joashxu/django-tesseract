#!/bin/bash
set -e
LOGFILE=/home/ubuntu/webapps/tesseract/tesseract.log
NUM_WORKERS=2
USER=ubuntu

# user/group to run as
cd /home/ubuntu/webapps/tesseract/django-tesseract
source /home/ubuntu/webapps/tesseract/tesseractenv/bin/activate
exec python manage.py run_gunicorn --bind=127.0.0.1:8000 --settings=djangotesseract.settings 1>>$LOGFILE 2>>$LOGFILE
