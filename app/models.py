#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import db

from datetime import datetime


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


class Analysis(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)


class Pcap(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    fake_filename = db.Column(db.String(50), nullable=False, unique=True)
    filename = db.Column(db.String(50), nullable=False)
    size = db.Column(db.INTEGER, nullable=False)
    is_done = db.Column(db.BOOLEAN, nullable=False, default=False)

    when_upload = db.Column(db.DATETIME, default=datetime.now(), nullable=False)
    when_analysis_started = db.Column(db.DATETIME)



    result = db.relationship(Analysis, backref='pcap')

    def __init__(self, fake_filename, real_filename, filesize):
        self.fake_filename = fake_filename
        self.filename = real_filename
        self.size = filesize

    def __repr__(self):
        return "<Pcap %s>" % self.filename
