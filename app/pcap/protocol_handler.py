import validators

from app.models import *


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
        # matching = [s for s in data if "Cookie" in s]
        # if len(matching) != 0:
        #     matching[0].split()
        # check valid URL

        if validators.domain(host) is not True or data[0] == 'HTTP/1.1':
            return

        h = HTTP(host, uri, method)
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
