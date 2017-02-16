# -*- coding: utf-8 -*-

"""
requirements: haven click gevent
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
    from gevent import monkey; monkey.patch_all()
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
    from gevent import monkey; monkey.patch_all()
    from client.client import create_app

    app = create_app(host, port)
    app.run()


if __name__ == '__main__':
    cli()
