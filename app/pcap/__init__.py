from flask import Blueprint

pcap_blueprint = Blueprint('pcap', __name__)


def get_valid_timestamp(all_pkt_data, pkt_time):
    for i in range(3):
        try:
            return all_pkt_data[i][pkt_time][0].timestamp.isoformat(sep=' ')
        except KeyError:
            continue
    else:
        return ""

pcap_blueprint.add_app_template_filter(get_valid_timestamp, 'get_valid_timestamp')

from . import views
