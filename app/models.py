#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import db

from datetime import datetime


def add_and_commit(session, obj):
    session.add(obj)
    try:
        session.commit()
    except:
        session.rollback()
        raise


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


class KakaoImage(db.Model):
    __tablename__ = 'kakaoimage'
    id = db.Column(db.INTEGER, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)

    def __init__(self, filename):
        self.filename = filename

    def __repr__(self):
        return "<KakaoImage %d>" % self.id


class DNSHost(db.Model):
    __tablename__ = 'dnshost'
    id = db.Column(db.INTEGER, primary_key=True)
    host = db.Column(db.String(100), nullable=False)
    analysis_id = db.Column(db.INTEGER, db.ForeignKey('analysis.id'))

    def __init__(self, host):
        self.host = host

    def __repr__(self):
        return "<DNSHost %s>" % self.host


class Messenger(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    analysis_id = db.Column(db.INTEGER, db.ForeignKey('analysis.id'))

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return "<Messenger %d>" % self.id


class Analysis(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    pcap_id = db.Column(db.INTEGER, db.ForeignKey('pcap.id'))
    total_packet = db.Column(db.INTEGER, nullable=False)
    dns_packet = db.relationship(DNSHost, backref='analysis')
    messenger_packet = db.relationship(Messenger)

    def __init__(self):
        pass

    def __repr__(self):
        return "<Analysis %s>" % self.pcap.filename


class Pcap(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    fake_filename = db.Column(db.String(50), nullable=False, unique=True)
    filename = db.Column(db.String(50), nullable=False)
    is_done = db.Column(db.BOOLEAN, nullable=False, default=False)

    when_upload = db.Column(db.DATETIME, default=datetime.now(), nullable=False)
    when_analysis_started = db.Column(db.DATETIME)
    when_analysis_finished = db.Column(db.DATETIME)

    analysis = db.relationship(Analysis, backref='pcap')

    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))

    def __init__(self, fake_filename, real_filename):
        self.fake_filename = fake_filename
        self.filename = real_filename

    def __repr__(self):
        return "<Pcap %s>" % self.filename


class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    userid = db.Column(db.String(30), nullable=False, unique=True)
    userpw = db.Column(db.String(30), nullable=False)
    pcap = db.relationship(Pcap, backref='user')

    def __init__(self, userid, userpw):
        self.userid = userid
        self.userpw = userpw

    def __repr__(self):
        return "<User %s>" % self.userid
