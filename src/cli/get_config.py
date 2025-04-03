import click

@click.command()
@click.pass_context
def gc(ctx):
    """ get configuration information for patten_email class"""
    response = ctx.obj['sg_client'].senders.get()
    # response = sg.client.senders.get()
    click.echo(response.body)
