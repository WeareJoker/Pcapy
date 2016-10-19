#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app, manager


@manager.command
def run():
    app.run(host='0.0.0.0', port=5000, debug=True)


@manager.command
def db_init():
    from app import db
    from app.models import User, add_and_commit
    u = User('asdf', 'asdf')
    add_and_commit(db.session, u)


if __name__ == "__main__":
    manager.run()
