import click

@click.command()
@click.pass_context
def gc(ctx):
    """ get configuration information for patten_email class"""
    senders = ctx.invoke(gs)
    click.echo(senders)
    asm = ctx.invoke(ga)
    click.echo(asm)
    templates = ctx.invoke(gt)
    click.echo(templates)


@click.command()
@click.pass_context
def gs(ctx):
    """ get sendgird senders """
    response = ctx.obj['sg_client'].senders.get()
    return response.body


@click.command()
@click.pass_context
def ga(ctx):
    """ get sendgird asms """
    response = ctx.obj['sg_client'].asm.suppressions.get()
    click.echo(response.body)

@click.command()
@click.pass_context
def gt(ctx):
    """ get sendgird templates """
    response = ctx.obj['sg_client'].templates.get()
    click.echo(response.body)
