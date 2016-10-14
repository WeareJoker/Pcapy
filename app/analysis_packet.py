from .models import *


def analysis_dns(eth, analysis):
    hostname = eth[3].qd.qname.decode()
    d = DNSHost(hostname)
    db.session.add(d)
    analysis.dns_packet.append(d)

    db.session.commit()


def analysis_http(eth, analysis):
    if "M-SEARCH" in repr(eth[3]) or b"200 OK" in eth[3].load:
        pass
    else:
        try:
            data = eth[3].load.decode().split()
        except UnicodeDecodeError:
            raw_data = eth[3].load
            data = raw_data[:raw_data.find(b'\r\n\r\n')].decode().split()
        if data[0] == 'HTTP/1.1':
            pass
        else:
            host = data[data.index('Host:') + 1]
            h = HTTP(host, data[1], data[0])
            db.session.add(h)

            analysis.http.append(h)

            db.session.commit()


def analysis_arp(eth, analysis):
    arp = eth[1]

    try:
        a = ARP(arp.hwsrc, arp.hwdst, arp.psrc, arp.pdst, arp.op)
    except AttributeError:
        pass
    else:
        db.session.add(a)
        analysis.arp.append(a)
        db.session.commit()
