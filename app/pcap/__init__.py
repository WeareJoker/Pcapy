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


def get_packet_length(pkt_data, pkt_time):
    pkt_list = pkt_data.get(pkt_time)

    if pkt_list is None:
        return 0
    else:
        return len(pkt_list)


pcap_blueprint.add_app_template_filter(get_valid_timestamp, 'get_valid_timestamp')
pcap_blueprint.add_app_template_filter(get_packet_length, 'get_packet_length')

from . import views
