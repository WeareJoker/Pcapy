#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import db

from datetime import datetime
from flask_sqlalchemy import event


class NoInfoException(Exception):
    pass


class CustomGroupBy:
    def __init__(self, query_data):

        self.query_data = query_data
        self.print_format = None
        if len(self.query_data) != 0:
            self.time_list = list(set(map(lambda x: x.timestamp, self.query_data)))
            self.time_unit_func = self.__check_time_unit()
            self.pkt_data = self.time_unit_func()
        else:
            self.time_list = None
            self.time_unit_func = None
            self.pkt_data = None

    def __check_time_unit(self):
        time_diff = datetime.fromtimestamp(
            max(self.time_list).timestamp() - min(self.time_list).timestamp()
        )

        if time_diff.hour > 14:
            # this is hour type
            return self.__hour
        elif time_diff.minute > 15:
            # this is minute type
            return self.__minute
        else:
            # this is second type
            return self.__second

    def __hour(self):
        self.print_format = "%Y-%m-%d %H:00:00"
        self.time_list = [i.replace(minute=0, second=0, microsecond=0) for i in self.time_list]
        time_list = list(set(map(lambda x: x.timestamp.hour, self.query_data)))
        return [[y for y in self.query_data if y.timestamp.hour == x] for x in time_list]

    def __minute(self):
        self.print_format = "%Y-%m-%d %H:%M:00"
        self.time_list = [i.replace(second=0, microsecond=0) for i in self.time_list]
        time_list = list(set(map(lambda x: x.timestamp.minute, self.query_data)))
        return [[y for y in self.query_data if y.timestamp.minute == x] for x in time_list]

    def __second(self):
        self.print_format = "%Y-%m-%d %H:%M:%S"
        self.time_list = [i.replace(microsecond=0) for i in self.time_list]
        time_list = list(set(map(lambda x: x.timestamp.second, self.query_data)))
        return [[y for y in self.query_data if y.timestamp.second == x] for x in time_list]

    @staticmethod
    def sum_time_list(*args):
        sum_data = list()
        for group in args:
            sum_data += group.time_list
        return list(set(sum_data))


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
    timestamp = db.Column(db.DATETIME, nullable=False)
    op = db.Column(db.INTEGER)
    hwsrc = db.Column(db.String(20))
    hwdst = db.Column(db.String(20))
    psrc = db.Column(db.String(20))
    pdst = db.Column(db.String(20))

    analysis_id = db.Column(db.INTEGER, db.ForeignKey('analysis.id'))

    def __init__(self, hwsrc, hwdst, psrc, pdst, timestamp, op=None):
        if op is not None:
            self.op = op
        self.hwsrc = hwsrc
        self.hwdst = hwdst
        self.psrc = psrc
        self.pdst = pdst
        self.timestamp = timestamp.replace(microsecond=0)

    def __repr__(self):
        return "<ARP %s>" % self.hwsrc


class HTTP(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    timestamp = db.Column(db.DATETIME, nullable=False)
    host = db.Column(db.String(150), nullable=False)
    uri = db.Column(db.String(30), nullable=False)
    kakao = db.Column(db.BOOLEAN, default=False, nullable=False)
    method = db.Column(db.String(20), nullable=False)
    analysis_id = db.Column(db.INTEGER, db.ForeignKey('analysis.id'))

    def __init__(self, host, uri, method, timestamp, kakao=False):
        self.host = host
        self.uri = uri
        self.method = method
        self.kakao = kakao
        self.timestamp = timestamp.replace(microsecond=0)

    def __repr__(self):
        return "<HTTP %s %s>" % (self.host, str(self.timestamp))


class DNSHost(db.Model):
    __tablename__ = 'dnshost'
    id = db.Column(db.INTEGER, primary_key=True)
    timestamp = db.Column(db.DATETIME, nullable=False)
    host = db.Column(db.String(100), nullable=False)
    analysis_id = db.Column(db.INTEGER, db.ForeignKey('analysis.id'))
    src_ip = db.Column(db.String(16), nullable=False)
    dst_ip = db.Column(db.String(16), nullable=False)

    def __init__(self, host, timestamp, src_ip, dst_ip):
        self.host = host
        self.timestamp = timestamp.replace(microsecond=0)
        self.src_ip = src_ip
        self.dst_ip = dst_ip

    def __repr__(self):
        return "<DNSHost %s>" % self.host


class OtherPkt(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    analysis_id = db.Column(db.INTEGER, db.ForeignKey('analysis.id'))
    timestamp = db.Column(db.DATETIME, nullable=False)

    def __init__(self, timestamp):
        self.timestamp = timestamp.replace(microsecond=0)

    def __repr__(self):
        return "<UnKnown at %s>" % str(self.timestamp)


class Analysis(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    pcap_id = db.Column(db.INTEGER, db.ForeignKey('pcap.id'))
    total_packet = db.Column(db.INTEGER)
    dns_packet = db.relationship(DNSHost, backref='analysis', order_by=DNSHost.timestamp)
    arp = db.relationship(ARP, backref='analysis', order_by=ARP.timestamp)
    http = db.relationship(HTTP, backref='analysis', order_by=HTTP.timestamp)
    other_pkt = db.relationship(OtherPkt, backref='analysis', order_by=OtherPkt.timestamp)
    when_analysis_started = db.Column(db.DATETIME)
    when_analysis_finished = db.Column(db.DATETIME)

    def __init__(self):
        self.when_analysis_started = datetime.now()

    def __repr__(self):
        return "<Analysis %s>" % self.pcap.filename

    @property
    def kakao_url(self):
        return HTTP.query.filter_by(analysis_id=self.id, kakao=True).all()

    @property
    def all_pkt(self):
        return self.dns_packet + self.arp + self.http + self.other_pkt


@event.listens_for(Analysis, 'after_insert')
def add_alarm_start_analysis(_, connection, target):
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

    @staticmethod
    def find_pcap(*args, **kwargs):
        # return Pcap.query.filter_by(*args, **kwargs).first_or_404()
        p = Pcap.query.filter_by(*args, **kwargs).first()
        if p is None:
            raise NoInfoException("No packet info!")
        else:
            return p


@event.listens_for(Pcap, 'after_insert')
def add_alarm_upload_pcap(_, connection, target):
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
