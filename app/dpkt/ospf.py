# $Id: ospf.py 23 2006-11-08 15:45:33Z dugsong $
# -*- coding: utf-8 -*-
"""Open Shortest Path First."""

from . import dpkt

AUTH_NONE = 0
AUTH_PASSWORD = 1
AUTH_CRYPTO = 2


class OSPF(dpkt.Packet):
    __hdr__ = (
        ('v', 'B', 0),
        ('type', 'B', 0),
        ('len', 'H', 0),
        ('router', 'I', 0),
        ('area', 'I', 0),
        ('sum', 'H', 0),
        ('atype', 'H', 0),
        ('auth', '8s', '')
    )

    def __str__(self):
        return str(self.__bytes__())
    
    def __bytes__(self):
        if not self.sum:
            self.sum = dpkt.in_cksum(dpkt.Packet.__bytes__(self))
        return dpkt.Packet.__bytes__(self)
