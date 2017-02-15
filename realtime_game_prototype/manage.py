# -*- coding: utf-8 -*-

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
def runclient():
    """
    启动客户端
    """
    from gevent import monkey; monkey.patch_all()
    pass


if __name__ == '__main__':
    cli()
