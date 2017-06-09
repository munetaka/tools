import click


@click.group()
def cmd():
    pass


@cmd.command()
@click.option('--text', default='', help='option test')
def sub(text):
    msg = 'sub command.' + text
    click.echo(msg)


@cmd.command()
def hoge():
    click.echo('hoge command')


def main():
    cmd()


if __name__ == '__main__':
    main()
