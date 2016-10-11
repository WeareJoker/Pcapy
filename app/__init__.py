#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
from flask_script import Manager
from celery import Celery

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_pyfile('config.py')


def make_celery(app):
    c = Celery(app.import_name, backend=app.config['CELERY_BACKEND'],
               broker=app.config['CELERY_BROKER_URL'])
    c.conf.update(app.config)
    task_base = c.Task

    class ContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return task_base.__call__(self, *args, **kwargs)

    c.Task = ContextTask
    return c


celery = make_celery(app)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

migrate = Migrate(app, db)

from .views import *