import validators

from app.models import *


def analysis_dns(eth, analysis, pkt_time):
    hostname = eth[3].qd.qname.decode()
    d = DNSHost(hostname, pkt_time)
    db.session.add(d)
    analysis.dns_packet.append(d)

    db.session.commit()


KAKAO_URL = ["th-m4.talk.kakao.com", "th-p.talk.kakao.co.kr", "p.talk.kakao.co.kr"]


def analysis_http(eth, analysis, pkt_time):
    if "M-SEARCH" in repr(eth[3]) or b"200 OK" in eth[3].load:
        return

    try:
        load_data = eth[3].load
    except UnicodeDecodeError:
        raw_data = eth[3].load
        load_data = raw_data[:raw_data.find(b'\r\n\r\n')]
    try:
        data = load_data.decode().split('\r\n')
        method, uri, _ = data[0].split()
    except (ValueError, UnicodeDecodeError) as _:
        return

    host = data[1].split('Host: ')[-1]

    # check valid URL
    if validators.domain(host) is not True \
            or data[0] == 'HTTP/1.1':
        return

    h = HTTP(host, uri, method, pkt_time, kakao=(host in KAKAO_URL))
    db.session.add(h)

    analysis.http.append(h)

    db.session.commit()


def analysis_arp(eth, analysis, pkt_time):
    arp = eth[1]

    try:
        a = ARP(arp.hwsrc, arp.hwdst, arp.psrc, arp.pdst, pkt_time, arp.op)
    except AttributeError:
        pass
    else:
        db.session.add(a)
        analysis.arp.append(a)
        db.session.commit()
