# -*- coding: utf-8 -*-

# 核心层运行帧率。服务器与客户端相同
LOGIC_FRAME_RATE = 20

# 客户端表现层帧率。客户端可以自己调整，与服务器交互逻辑无关
RENDER_FRAME_RATE = 60

# 服务器与客户端之间帧差别的最大值
LOGIC_FRAME_MAX_DIFF = 10

# 日志
LOG_FORMAT = '\n'.join((
    '/' + '-' * 80,
    '[%(levelname)s][%(asctime)s][%(process)d:%(thread)d][%(filename)s:%(lineno)d %(funcName)s]:',
    '%(message)s',
    '-' * 80 + '/',
))
COLOR_LOG_FORMAT = '%(log_color)s' + LOG_FORMAT

