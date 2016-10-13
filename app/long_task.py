from . import celery
from . import dpkt
from .config import *
from .login_manager import current_user
from .models import *
from scapy.all import *
from .analysis_packet import *

from datetime import datetime


@celery.task(bind=True)
def db_test(self):
    self.update_state(state='START')
    import time
    time.sleep(3)
    self.update_state(state='Finish')
    print(self)
    print(Pcap.query.all())
    return True


packet_info_table = {
    'DNS': analysis_dns,
    'HTTP': analysis_http,
    'ARP': analysis_arp,
}


def analysis_pcap(pcap_path, user):
    u = current_user(user)

    pcap_filename = os.path.basename(pcap_path)

    db_pcap = Pcap.query.filter_by(fake_filename=pcap_filename).first()
    db_pcap.when_analysis_started = datetime.now()

    db_pcap.analysis = Analysis()

    # db.session.commit()

    pcap_reader = dpkt.pcap.Reader(open(pcap_path, 'rb'))

    packet_count = 0
    """
    for _, buf in pcap_reader:
        packet_count += 1
        eth = Ether(buf)

        for proto in packet_info_table.keys():
            if proto in repr(eth):
                packet_info_table[proto](eth, db_pcap.analysis)
    """

    db_pcap.analysis.total_packet = packet_count
    db_pcap.is_done = True
    db_pcap.when_analysis_finished = datetime.now()
    u.alarm.append(Alarm("Success", "Finish Analysis %s" % db_pcap.fake_filename, simple_content="Finish Analysis"))

    db.session.commit()
