# cli.py
import click


@click.command()
@click.option('--name', default='World', help='Name to greet')
def greet(name):
    """Simple program that greets NAME."""
    click.echo(f'Hello, {name}!')


if __name__ == '__main__':
    greet()