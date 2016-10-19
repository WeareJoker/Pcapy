import time

from flask import stream_with_context, request, Response

from app.user.login_manager import *
from . import main_blueprint


@main_blueprint.route('/stream')
def streamed_response():
    def generate():
        yield 'Hello '
        time.sleep(2)
        yield request.args['name']
        time.sleep(3)
        yield '!'

    return Response(stream_with_context(generate()))


@main_blueprint.route('/')
def index():
    return redirect(url_for('pcap.upload_pcap'))


from .static_view import *
