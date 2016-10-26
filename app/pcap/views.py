import os

from flask import render_template, request
from sqlalchemy import extract
from sqlalchemy import func

from app.config import randomkey, PCAP_FILE_PATH
from app.models import *
from app.user.login_manager import *
from . import pcap_blueprint
from .analyser import analysis_pcap


def pcap_required(func):
    @wraps(func)
    def check_pcap_select(*args, **kwargs):
        try:
            assert session['pcap'] != 'error'
        except (KeyError, AssertionError):
            return "<script>alert('분석할 패킷 파일을 선택해주세요!');history.go(-1);</script>"
        else:
            return func(*args, **kwargs)

    return check_pcap_select


@pcap_blueprint.route('/result/<pcap_name>')
@login_required
def result(pcap_name):
    try:
        p = Pcap.find_pcap(user=current_user(), fake_filename=pcap_name)
    except NoInfoException:
        return "<script>alert('잘못된 접근입니다!');history.go(-1);</script>"
    else:
        session['pcap'] = pcap_name
        dns_data = db.session.query(DNSHost.host, func.count(DNSHost.host)).filter_by(
            analysis_id=p.analysis.id).group_by(DNSHost.host).all()

        all_time = sorted(set(map(lambda x: x.timestamp, p.analysis.all_pkt)))

        http_set = dict(
            db.session.query(HTTP.timestamp, func.count(HTTP.host)).filter_by(
                analysis_id=p.analysis.id).group_by(extract('second', HTTP.timestamp)).all()
        )

        dns_set = dict(
            db.session.query(DNSHost.timestamp, func.count(DNSHost.host)).filter_by(
                analysis_id=p.analysis.id).group_by(extract('second', DNSHost.timestamp)).all()
        )

        arp_set = dict(
            db.session.query(ARP.timestamp, func.count(ARP.hwsrc)).filter_by(
                analysis_id=p.analysis.id).group_by(extract('second', ARP.timestamp)).all()
        )

        other_set = dict(
            db.session.query(OtherPkt.timestamp, func.count(OtherPkt.id)).filter_by(
                analysis_id=p.analysis.id).group_by(extract('second', OtherPkt.timestamp)).all()
        )

        return render_template(
            'pcap/index.html',
            pcap=p,
            all_pkt_time=all_time,
            http_data=http_set,
            dns_data=dns_set,
            arp_data=arp_set,
            other_data=other_set,
            dns_count_list=dns_data
        )


def make_file_info(filename):
    file_type = filename.split('.')[-1]
    fake_filename = randomkey(len(filename)) + '.' + file_type
    filepath = os.path.join(PCAP_FILE_PATH, fake_filename)
    return fake_filename, filepath


@pcap_blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_pcap():
    if request.method == 'GET':
        return render_template('pcap/upload_pcap.html',
                               pcap_id=randomkey(30),
                               user=current_user())

    elif request.method == 'POST':
        pcap_file = request.files['pcap']
        filename, filepath = make_file_info(pcap_file.filename)

        pcap_file.save(filepath)
        u = current_user()

        p = Pcap(filename, pcap_file.filename, u)

        add_and_commit(db.session, p)
        u.pcap.append(p)
        db.session.commit()

        analysis_pcap.delay(filepath, u.userid)

        return filename


@pcap_blueprint.route('/dns/<pcap_name>')
@login_required
@pcap_required
def result_dns(pcap_name):
    try:
        p = Pcap.find_pcap(user=current_user(), fake_filename=pcap_name)
    except NoInfoException:
        return "<script>alert('잘못된 접근입니다!');history.go(-1);</script>"
    else:
        dns_data = db.session.query(DNSHost.host, func.count(DNSHost.host)).filter_by(
            analysis_id=p.analysis.id).group_by(DNSHost.host).all()
        return render_template('pcap/dns.html',
                               pcap=p,
                               dns_data=dns_data)
