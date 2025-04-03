import click

@click.command()
@click.pass_context
def gc(ctx):
    """ get configuration information for patten_email class"""
    senders = ctx.invoke(gs)


@click.command()
@click.pass_context
def gs(ctx):
    """ get sendgird senders """
    response = ctx.obj['sg_client'].senders.get()
    click.echo(response.body)