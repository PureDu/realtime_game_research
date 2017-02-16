# -*- coding: utf-8 -*-

import logging
import weakref
import time
import gevent
from gevent.queue import Queue
from haven import GHaven
import colorlog

from share.game_box import GameBox
from share import cmds
from share import constants
from share import rets


def create_app():

    app = GHaven(GameBox)

    app.conn_id_inc = 0
    app.conn_dict = weakref.WeakValueDictionary()

    # 消息
    app.msg_queue = Queue()

    # 核心帧数index
    app.frame_index = 0

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

    app.logger = logger

    haven_logger = logging.getLogger('haven')
    haven_logger.setLevel(logging.ERROR)
    haven_logger.addHandler(console_handler)

    def game_loop():
        app.logger.debug('game loop start')
        app.frame_index = 0
        # 游戏帧循环
        frame_interval = 1.0 / constants.KERNEL_FRAME_RATE
        # 每一帧，从 net_msg_queue 将数据取出来
        while True:
            app.frame_index += 1
            # do something
            while not app.msg_queue.empty():
                box = app.msg_queue.get_nowait()
                # 广播
                broadcast(box)

            time.sleep(frame_interval)

    def broadcast(box):
        """
        广播
        :param box:
        :return:
        """
        data = box.pack()
        for conn in app.conn_dict.values():
            conn.write(data)

    @app.create_conn
    def create_conn(conn):
        # 自增
        app.conn_id_inc += 1
        conn.conn_id = app.conn_id_inc

        # 还没有准备好
        conn.user_ready = False

        # 析构会自动删除
        app.conn_dict[conn.conn_id] = conn
        app.logger.debug('conn created. conn_id: %s, conns: %s', conn.conn_id, app.conn_dict.keys())

    @app.close_conn
    def close_conn(conn):
        app.conn_dict.pop(conn.conn_id, None)
        app.logger.debug('conn closed. conn_id: %s, conns: %s', conn.conn_id, app.conn_dict.keys())

    @app.before_request
    def before_request(request):
        app.logger.debug('request: %r', request)

    @app.before_response
    def before_response(conn, response):
        app.logger.debug('conn: %s, response: %r', conn, response)

    @app.route(cmds.CMD_USER_READY)
    def user_ready(request):
        # 设置为True
        request.conn.user_ready = True

        request.write(dict(
            ret=0
        ))

        if len(app.conn_dict) < 2 or filter(lambda x: not x.user_ready, app.conn_dict.values()):
            return

        # 人数大于等于2，并且所有人都已经准备好了
        # 就可以下发游戏开始通知了

        # 启动游戏主循环
        gevent.spawn(game_loop)

        box = GameBox()
        box.cmd = cmds.CMD_EVT_GAME_START

        broadcast(box)

    @app.route(cmds.CMD_USER_ACTION)
    def user_action(request):
        if request.box.frame_index == app.frame_index:
            # 广播
            box = GameBox()
            box.cmd = cmds.CMD_EVT_USER_ACTION

            payload = request.box.get_json()
            payload['conn_id'] = request.conn.conn_id
            box.set_json(payload)

            app.msg_queue.put(box)

            request.write(dict(
                ret=0
            ))
        else:
            app.logger.error(
                'invalid frame_index. frame_index: %s, box: %r, conn_id: %s',
                app.frame_index,
                request.box,
                request.conn.conn_id
            )

            request.write(dict(
                ret=rets.RET_INVALID_FRAME_INDEX
            ))

    return app
