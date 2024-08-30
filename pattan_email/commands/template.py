import click
import os


@click.group()
def template():
    """group to hold template specific commands"""
    pass


@click.command("ls")
@click.pass_context
def list_template(ctx):
    response = (ctx.parent.parent.sg_client).client.templates.get(verify=False)
    print(response.status_code)
    print(response.body)
    print(response.headers)
    """Prints a list of all sendgrid templates"""


template.add_command(list_template)