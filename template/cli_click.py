import click


@click.group()
@click.option('--verbose', is_flag=True)
def cli(verbose):
    if verbose:
        click.echo('[verbose mode now]')


@cli.command()
@click.option('--name', default='you', help='greet this name')
@click.option('--repeat', default=1, help='how many time you greet')
@click.argument('out', type=click.File('w'), default='-', required=False)
def say(name, repeat, out):
    '''say hellow to you.'''
    click.echo(out)
    for i in range(repeat):
        click.echo("Hello %s" % name, file=out)


def main():
    cli()


if __name__ == '__main__':
    main()
