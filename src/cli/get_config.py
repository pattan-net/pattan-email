import click

@click.command()
def gc():
    """ get configuration information for patten_email class"""
    click.echo('Im in get config')