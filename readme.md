python manage.py dumpdata gateway --indent 4 > email_gateway/fixtures/email_template.json
python manage.py loaddata apps/gateway/fixtures/email_template.json
