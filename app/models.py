#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import db


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


class Pcap(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    fake_filename = db.Column(db.String(50), nullable=False, unique=True)
    real_filename = db.Column(db.String(50), nullable=False)
    is_done = db.Column(db.BOOLEAN, nullable=False, default=False)

    def __init__(self, fake_filename, real_filename):
        self.fake_filename = fake_filename
        self.real_filename = real_filename

    def __repr__(self):
        return "<Pcap %s>" % self.real_filename
