# -*- coding: utf-8 -*-

import time
import gevent

from share import cmds


class Client(object):

    host = None
    port = None

    def __init__(self, host, port):
        self.host = host
        self.port = port

    # 核心层
    def kernel_loop(self):
        pass

    # 表现层
    def show_loop(self):
        pass

    def run(self):
        gevent.spawn(self.kernel_loop)
        gevent.spawn(self.show_loop)

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                return


def create_app(host, port):
    return Client(host, port)
