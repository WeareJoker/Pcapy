#!/bin/bash
rm app/testdb.db;
rm -rf migrations/;
python manage.py db init;
python manage.py db migrate;
python manage.py db upgrade;
