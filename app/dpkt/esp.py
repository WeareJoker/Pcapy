# $Id: esp.py 23 2006-11-08 15:45:33Z dugsong $
# -*- coding: utf-8 -*-
"""Encapsulated Security Protocol."""

from . import dpkt


class ESP(dpkt.Packet):
    __hdr__ = (
        ('spi', 'I', 0),
        ('seq', 'I', 0)
    )
