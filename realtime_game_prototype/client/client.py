# -*- coding: utf-8 -*-

import click
import time
import gevent
from gevent.queue import Queue

from netkit.box import Box
from netkit.contrib.tcp_client import TcpClient

from share import cmds


class Client(object):

    tcp_client = None

    # 网络层->核心层
    net_msg_queue = None

    def __init__(self, host, port):
        self.net_msg_queue = Queue()
        self.tcp_client = TcpClient(Box, host, port)

    def net_loop(self):
        # 这里将网络层作为一个单独的线程来处理了
        # 实际也可以移到核心层里去，每帧去尝试read一次
        # 先这么写吧
        while True:
            if self.tcp_client.closed():
                try:
                    self.tcp_client.connect()
                except:
                    # 重连
                    time.sleep(0.1)
                    continue

            # 到这里就一定连接成功了
            box = self.tcp_client.read()

            self.net_msg_queue.put(box)

    # 核心层
    def kernel_loop(self):
        # 每一帧，从 net_msg_queue 将数据取出来
        while True:
            while not self.net_msg_queue.empty():
                # 会自己返回
                msg = self.net_msg_queue.get_nowait()

                click.secho('msg: %r' % msg, fg='green')

            # TODO 帧检测

    # 表现层
    def show_loop(self):
        pass

    def run(self):
        gevent.spawn(self.net_loop)
        gevent.spawn(self.kernel_loop)
        gevent.spawn(self.show_loop)

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                return


def create_app(host, port):
    return Client(host, port)
