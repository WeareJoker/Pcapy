#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.script import Manager

from app import app, manager


@manager.command
def run():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == "__main__":
    manager.run()
