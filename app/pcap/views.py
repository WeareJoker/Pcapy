import os
from app.config import randomkey, PCAP_FILE_PATH
from flask import render_template, request
from . import pcap_blueprint
from app.user.login_manager import *
from app.models import *
from .analyser import analysis_pcap

from sqlalchemy import func


@pcap_blueprint.route('/result/<pcap_name>')
@login_required
def result(pcap_name):
    try:
        p = Pcap.find_pcap(user=current_user(), fake_filename=pcap_name)
    except NoInfoException:
        return "<script>alert('잘못된 접근입니다!');history.go(-1);</script>"
    else:
        dns_data = db.session.query(DNSHost.host, func.count(DNSHost.host)).filter_by(
            analysis_id=p.analysis.id).group_by(DNSHost.host).all()
        return render_template('pcap/index.html',
                               pcap=p,
                               dns_data=dns_data)


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
