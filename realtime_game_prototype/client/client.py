# -*- coding: utf-8 -*-

import gevent

from share import cmds


class Client(object):

    # 核心层
    def kernel_loop(self):
        pass


    # 表现层
    def show_loop(self):
        pass

    def run(self, host, port):
