# -*- coding: utf-8 -*-

import click


@click.group()
def cli():
    pass


@cli.command()
def runserver():
    """
    启动服务器
    """
    pass


@cli.command()
def runclient():
    """
    启动客户端
    """
    pass


if __name__ == '__main__':
    cli()
