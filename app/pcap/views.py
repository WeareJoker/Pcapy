import os

from flask import render_template, request
from sqlalchemy import extract
from sqlalchemy import func
from werkzeug.exceptions import BadRequestKeyError

from app.config import randomkey, PCAP_FILE_PATH
from app.models import *
from app.user.login_manager import *
from . import pcap_blueprint
from .analyser import analysis_pcap


def pcap_required(need_pcap_func):
    @wraps(need_pcap_func)
    def check_pcap_select(*args, **kwargs):
        try:
            assert session['pcap'] != 'error'
        except (KeyError, AssertionError):
            return "<script>alert('분석할 패킷 파일을 선택해주세요!');history.go(-1);</script>"
        else:
            return need_pcap_func(*args, **kwargs)

    return check_pcap_select


def make_param_by_graph_type(got_type):
    data_set = {
        'minute': dict(second=0),
        'hour': dict(minute=0, second=0)
    }
    try:
        return data_set[got_type]
    except KeyError:
        return data_set['minute']


@pcap_blueprint.route('/result/<pcap_name>')
@login_required
def result(pcap_name):
    try:
        p = Pcap.find_pcap(user=current_user(), fake_filename=pcap_name)
    except NoInfoException:
        return "<script>alert('잘못된 접근입니다!');history.go(-1);</script>"

    try:
        graph_type = request.args['graph_type']

    except BadRequestKeyError:
        return redirect(url_for('pcap.result', pcap_name=pcap_name, graph_type='second'))

    session['pcap'] = pcap_name
    dns_data = db.session.query(DNSHost.host, func.count(DNSHost.host)).filter_by(
        analysis_id=p.analysis.id).group_by(DNSHost.host).all()

    if graph_type == 'second':
        convert_type = None
        all_time = sorted(set(map(lambda x: x.timestamp, p.analysis.all_pkt)))
    else:
        convert_type = make_param_by_graph_type(graph_type)
        all_time = sorted(set(map(lambda x: x.timestamp.replace(**convert_type),
                                  p.analysis.all_pkt)))

    http_set = dict(
        db.session.query(HTTP.timestamp, func.count(HTTP.host)).filter_by(
            analysis_id=p.analysis.id).group_by(extract(graph_type, HTTP.timestamp)).all()
    )

    dns_set = dict(
        db.session.query(DNSHost.timestamp, func.count(DNSHost.host)).filter_by(
            analysis_id=p.analysis.id).group_by(extract(graph_type, DNSHost.timestamp)).all()
    )

    arp_set = dict(
        db.session.query(ARP.timestamp, func.count(ARP.hwsrc)).filter_by(
            analysis_id=p.analysis.id).group_by(extract(graph_type, ARP.timestamp)).all()
    )

    other_set = dict(
        db.session.query(OtherPkt.timestamp, func.count(OtherPkt.id)).filter_by(
            analysis_id=p.analysis.id).group_by(extract(graph_type, OtherPkt.timestamp)).all()
    )
    if convert_type is not None:  # Have to Change datetime form
        for data_set in [http_set, dns_set, arp_set, other_set]:
            for data_set_key in data_set:
                data_set[data_set_key.replace(**convert_type)] = data_set.pop(data_set_key)

    return render_template(
        'pcap/index.html',
        pcap=p,
        all_pkt_time=all_time,
        http_data=http_set,
        dns_data=dns_set,
        arp_data=arp_set,
        other_data=other_set,
        dns_count_list=dns_data,
        graph_type=graph_type
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
