#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask

app = Flask(__name__)


def create_app():
    from main import main_blueprint
    app.register_blueprint(main_blueprint)
    return app