from flask import Blueprint

pcap_blueprint = Blueprint('pcap', __name__)

from . import views
