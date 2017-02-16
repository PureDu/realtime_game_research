# -*- coding: utf-8 -*-

"""
requirements: haven click

使用:

python manage.py runserver

python manage.py runclient
python manage.py runclient

然后在两个client分别输入 ready，使游戏启动。
之后输入 move/hit 等 action 命令，即可在client间同步


"""

import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('-t', '--host', default='127.0.0.1',
              help='host')
@click.option('-p', '--port', type=int, help='port', required=True)
def runserver(host, port):
    """
    启动服务器
    """
    from server.server import create_app

    app = create_app()
    app.run(host, port)


@cli.command()
@click.option('-t', '--host', default='127.0.0.1',
              help='host')
@click.option('-p', '--port', type=int, help='port', required=True)
def runclient(host, port):
    """
    启动客户端
    """
    from client.client import create_app

    app = create_app(host, port)
    app.run()


if __name__ == '__main__':
    cli()
