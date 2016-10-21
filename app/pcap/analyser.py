from scapy.all import *

from app.user.login_manager import current_user
from app import celery
from app import dpkt
from .protocol_handler import *

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

    db_pcap.analysis = Analysis()

    # db.session.commit()
    try:
        pcap_reader = dpkt.pcap.Reader(open(pcap_path, 'rb'))
    except ValueError:
        db_pcap.is_done = 2
        db_pcap.error_info = "Invalid file. Is it right pcap file?"
        u.alarm.append(Alarm("Error", "Error Analysis %s" % db_pcap.fake_filename, simple_content="Error Analysis"))
    else:
        packet_count = 0

        for pkt_time, buf in pcap_reader:
            packet_count += 1
            eth = Ether(buf)

            for proto in packet_info_table.keys():
                if proto in repr(eth):
                    packet_info_table[proto](eth, db_pcap.analysis, datetime.fromtimestamp(pkt_time))
            else:
                db_pcap.analysis.other_pkt.append(OtherPkt(pkt_time))
                db.session.commit()

        db_pcap.analysis.total_packet = packet_count
        db_pcap.is_done = 1
        db_pcap.analysis.when_analysis_finished = datetime.now()
        u.alarm.append(Alarm("Success", "Finish Analysis %s" % db_pcap.fake_filename, simple_content="Finish Analysis"))

    db.session.commit()
    print("Complete Analysis %s" % db_pcap.filename)
