from scapy.all import *

from . import celery
from . import dpkt
from .analysis_packet import *
from .login_manager import current_user

packet_info_table = {
    'DNS': analysis_dns,
    'HTTP': analysis_http,
    'ARP': analysis_arp,
}


@celery.task
def analysis_pcap(pcap_path, user):
    u = current_user(user)

    pcap_filename = os.path.basename(pcap_path)

    db_pcap = Pcap.query.filter_by(fake_filename=pcap_filename).first()
    db_pcap.when_analysis_started = datetime.now()

    db_pcap.analysis = Analysis()

    # db.session.commit()
    try:
        pcap_reader = dpkt.pcap.Reader(open(pcap_path, 'rb'))
    except ValueError:
        db_pcap.is_done = 3
        db_pcap.error_info = "Invalid file. Is it right pcap file?"
        u.alarm.append(Alarm("Error", "Error Analysis %s" % db_pcap.fake_filename, simple_content="Error Analysis"))
    else:
        packet_count = 0

        for _, buf in pcap_reader:
            packet_count += 1
            eth = Ether(buf)

            for proto in packet_info_table.keys():
                if proto in repr(eth):
                    packet_info_table[proto](eth, db_pcap.analysis)

        db_pcap.analysis.total_packet = packet_count
        db_pcap.is_done = 1
        db_pcap.when_analysis_finished = datetime.now()
        u.alarm.append(Alarm("Success", "Finish Analysis %s" % db_pcap.fake_filename, simple_content="Finish Analysis"))

    db.session.commit()
