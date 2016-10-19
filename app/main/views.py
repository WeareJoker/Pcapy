import time

from flask import stream_with_context, request, Response

from app.user.login_manager import *
from app import app


@app.route('/stream')
def streamed_response():
    def generate():
        yield 'Hello '
        time.sleep(2)
        yield request.args['name']
        time.sleep(3)
        yield '!'

    return Response(stream_with_context(generate()))


@app.route('/')
def index():
    return redirect(url_for('upload_pcap'))


