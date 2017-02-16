# -*- coding: utf-8 -*-

import logging
import time
import gevent
from gevent.queue import Queue

import colorlog
from netkit.contrib.tcp_client import TcpClient

from share.game_box import GameBox
from share import cmds
from share import constants


class Client(object):

    logger = None

    tcp_client = None

    # 网络层->核心层
    net_msg_queue = None

    # 核心层->表现层
    kernel_msg_queue = None

    # 核心层帧数index
    kernel_frame_index = 0

    def __init__(self, host, port):
        # 初始化log
        logger = logging.getLogger('main')
        logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(colorlog.ColoredFormatter(constants.COLOR_LOG_FORMAT, log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red',
        }))
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)

        self.logger = logger

        self.net_msg_queue = Queue()
        self.kernel_msg_queue = Queue()
        self.tcp_client = TcpClient(GameBox, host, port)

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
        while True:
            # 在游戏没有开始前，使用阻塞等待的方式
            # 这样可以确保核心层主循环在server-client同时启动
            box = self.net_msg_queue.get()

            if box.cmd == cmds.CMD_EVT_GAME_START:
                break

        self.kernel_frame_index = 0
        frame_interval = 1.0 / constants.KERNEL_FRAME_RATE
        # 每一帧，从 net_msg_queue 将数据取出来
        while True:
            self.kernel_frame_index += 1

            while not self.net_msg_queue.empty():
                # 会自己返回
                box = self.net_msg_queue.get_nowait()

                if box.cmd == cmds.CMD_USER_ACTION:
                    self.kernel_msg_queue.put('')

                self.logger.debug(
                    'kernel_frame_index: %s, box: %r', self.kernel_frame_index, box
                )

            # do something

            time.sleep(frame_interval)

    # 表现层
    def show_loop(self):
        frame_interval = 1.0 / constants.SHOW_FRAME_RATE

        while True:
            time.sleep(frame_interval)

    def run(self):
        gevent.spawn(self.net_loop)
        gevent.spawn(self.kernel_loop)
        gevent.spawn(self.show_loop)

        # 等待连接
        self.logger.info('waiting connect...')

        while self.tcp_client.closed():
            time.sleep(0.1)

        self.logger.info('connected')

        while True:
            try:
                text = raw_input('please input(ready/move/hit):')

                box = GameBox()

                if text == 'ready':
                    box.cmd = cmds.CMD_USER_READY
                    self.tcp_client.write(box)
                elif text in ('move', 'hit'):
                    box.cmd = cmds.CMD_USER_ACTION
                    box.set_json(dict(
                        action=text
                    ))
                    self.tcp_client.write(box)
                else:
                    self.logger.warn('invalid input: %s', text)

            except KeyboardInterrupt:
                break


def create_app(host, port):
    return Client(host, port)
