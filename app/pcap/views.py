import os
from app.config import randomkey, PCAP_FILE_PATH
from flask import render_template, request
from app import app
from app.user.login_manager import *
from app.models import *
from .analyser import analysis_pcap


@app.route('/result/<pcap_name>')
@login_required
def result(pcap_name):
    u = current_user()
    p = Pcap.query.filter_by(fake_filename=pcap_name, user=u).first()
    if p is None:
        return "<script>alert('잘못된 접근입니다!');history.go(-1);</script>"
    else:
        return render_template('main/index.html',
                               pcap=p,
                               user_pcap=u.pcap)


def make_file_info(filename):
    file_type = filename.split('.')[-1]
    fake_filename = randomkey(len(filename)) + '.' + file_type
    filepath = os.path.join(PCAP_FILE_PATH, fake_filename)
    return fake_filename, filepath


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_pcap():
    if request.method == 'GET':
        u = current_user()
        return render_template('main/upload_pcap.html',
                               pcap_id=randomkey(30),
                               user_pcap=u.pcap)

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
