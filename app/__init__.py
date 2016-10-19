#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
from flask_script import Manager
from celery import Celery

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
db = SQLAlchemy()
celery = Celery()

try:
    import MySQLdb
except ImportError:
    import pymysql

    pymysql.install_as_MySQLdb()


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


def create_app(app):
    from .main import main_blueprint
    from .user import user_blueprint
    from .pcap import pcap_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint, url_prefix='/'+user_blueprint.name)
    app.register_blueprint(pcap_blueprint, url_prefix='/'+pcap_blueprint.name)

    app.config.from_pyfile('config.py')

    return app

app = create_app(app)

db.init_app(app)

celery = make_celery(app)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

migrate = Migrate(app, db)

from .views import *
