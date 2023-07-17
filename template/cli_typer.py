import typer


app = typer.Typer()


@app.command()
def test1(name: str):
    typer.echo(f"Hello {name} !")


@app.command()
def test2(name: str, number: int, formal: bool = False):
    typer.echo(f'{name} is number {number}. formal = {formal}')
    typer.echo(
        typer.style(
            f'{name} is number {number}. formal = {formal}',
            fg=typer.colors.GREEN,
            bold=True,
        )
    )
    typer.echo(
        typer.style(
            f'{name} is number {number}. formal = {formal}',
            fg=typer.colors.WHITE,
            bg=typer.colors.RED,
            underline=True,
        )
    )


@app.command()
def test3(
    name: str,
    lastname: str = typer.Option("", help="Last name of person to greet."),
    formal: bool = typer.Option(False, help="Say hi formally."),
):
    """
    Say hi to NAME, optionally with a --lastname.

    If --formal is used, say hi very formally.
    """
    if formal:
        typer.echo(f"Good day Ms. {name} {lastname}.")
    else:
        typer.echo(f"Hello {name} {lastname}")


if __name__ == '__main__':
    app()
