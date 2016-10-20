#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import db

from datetime import datetime
from flask_sqlalchemy import event


def add_and_commit(session, obj):
    session.add(obj)
    try:
        session.commit()
    except:
        session.rollback()
        raise
    return obj


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


class ARP(db.Model):
    __tablename__ = 'arp'
    id = db.Column(db.INTEGER, primary_key=True)
    op = db.Column(db.INTEGER)
    hwsrc = db.Column(db.String(20))
    hwdst = db.Column(db.String(20))
    psrc = db.Column(db.String(20))
    pdst = db.Column(db.String(20))

    analysis_id = db.Column(db.INTEGER, db.ForeignKey('analysis.id'))

    def __init__(self, hwsrc, hwdst, psrc, pdst, op=None):
        if op is not None:
            self.op = op
        self.hwsrc = hwsrc
        self.hwdst = hwdst
        self.psrc = psrc
        self.pdst = pdst

    def __repr__(self):
        return "<ARP %s>" % self.hwsrc


class HTTP(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    host = db.Column(db.String(150), nullable=False)
    uri = db.Column(db.String(30), nullable=False)
    kakao = db.Column(db.BOOLEAN, default=False, nullable=False)
    method = db.Column(db.String(20), nullable=False)
    analysis_id = db.Column(db.INTEGER, db.ForeignKey('analysis.id'))

    def __init__(self, host, uri, method, kakao=False):
        self.host = host
        self.uri = uri
        self.method = method
        self.kakao = kakao

    def __repr__(self):
        return "<HTTP %s>" % self.host


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


class IPMAC(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    ip = db.Column(db.String(20), nullable=False)
    mac = db.Column(db.String(20), nullable=False)
    analysis_id = db.Column(db.INTEGER, db.ForeignKey('analysis.id'))

    def __init__(self, ip, mac):
        self.ip = ip
        self.mac = mac

    def __repr__(self):
        return "<IPMAC %s : %s>" % (self.ip, self.mac)


class Analysis(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    pcap_id = db.Column(db.INTEGER, db.ForeignKey('pcap.id'))
    total_packet = db.Column(db.INTEGER)
    dns_packet = db.relationship(DNSHost, backref='analysis')
    messenger_packet = db.relationship(Messenger, backref='analysis')
    ip_mac = db.relationship(IPMAC, backref='analysis')
    arp = db.relationship(ARP, backref='analysis')
    http = db.relationship(HTTP, backref='analysis')
    when_analysis_started = db.Column(db.DATETIME)
    when_analysis_finished = db.Column(db.DATETIME)

    def __init__(self):
        self.when_analysis_started = datetime.now()

    def __repr__(self):
        return "<Analysis %s>" % self.pcap.filename


@event.listens_for(Analysis, 'after_insert')
def add_alarm_start_analysis(mapper, connection, target):
    p = target.pcap
    u = p.user

    connection.execute(Alarm.__table__.insert().values(
        type="Info",
        content="Start Analysis %s" % p.filename),
        simple_content="Start Analysis",
        user_id=u.id
    )


class Pcap(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    fake_filename = db.Column(db.String(50), nullable=False, unique=True)
    filename = db.Column(db.String(50), nullable=False)
    is_done = db.Column(db.Integer, nullable=False, default=0)
    error_info = db.Column(db.TEXT)
    when_upload = db.Column(db.DATETIME, nullable=False)
    analysis = db.relationship(Analysis, backref='pcap', uselist=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))

    def __init__(self, fake_filename, real_filename, user):
        self.fake_filename = fake_filename
        self.filename = real_filename
        self.user = user
        self.when_upload = datetime.now()

    def __repr__(self):
        return "<Pcap %s by %s>" % (self.filename, self.user.userid)

    @property
    def upload_timestamp(self):
        return str(self.when_upload).split('.')[0]


@event.listens_for(Pcap, 'after_insert')
def add_alarm_upload_pcap(mapper, connection, target):
    connection.execute(Alarm.__table__.insert().values(
        type="Success",
        content="Successfully Upload %s" % target.filename),
        simple_content="File Uploaded",
        user_id=target.user.id
    )


class Alarm(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    type = db.Column(db.String(15), nullable=False)
    content = db.Column(db.String(40), nullable=False)
    simple_content = db.Column(db.String(20), nullable=False)
    time = db.Column(db.DATETIME)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))

    def __init__(self, type_id, content, simple_content):
        self.type = type_id
        self.content = content
        self.time = datetime.now()
        if simple_content is not None:
            self.simple_content = simple_content

    def __repr__(self):
        return "<Alarm %s by %s>" % (self.user.userid, self.content)


class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    userid = db.Column(db.String(30), nullable=False, unique=True)
    userpw = db.Column(db.String(30), nullable=False)
    pcap = db.relationship(Pcap, backref='user', order_by='Pcap.when_upload')
    alarm = db.relationship(Alarm, backref='user')

    def __init__(self, userid, userpw):
        self.userid = userid
        self.userpw = userpw

    def __repr__(self):
        return "<User %s>" % self.userid
