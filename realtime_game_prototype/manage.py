# -*- coding: utf-8 -*-

import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('-t', '--host', default='127.0.0.1',
              help='host')
@click.option('-p', '--port', type=int, help='port')
def runserver(host, port):
    """
    启动服务器
    """
    from server.server import app

    app.run(host, port)


@cli.command()
def runclient():
    """
    启动客户端
    """
    pass


if __name__ == '__main__':
    cli()
