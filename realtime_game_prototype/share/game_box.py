# -*- coding: utf-8 -*-

from collections import OrderedDict

from netkit.box import Box


class GameBox(Box):
    # 如果header字段变化，那么格式也会变化
    header_attrs = OrderedDict([
        ('magic', ('i', 2037952207)),
        ('version', ('h', 0)),
        ('flag', ('h', 0)),
        ('packet_len', ('i', 0)),
        ('cmd', ('i', 0)),
        ('ret', ('i', 0)),
        ('sn', ('i', 0)),
        ('frame_index', ('i', 0)),
    ])
