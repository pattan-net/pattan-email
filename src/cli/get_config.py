import click
import json

@click.command()
@click.pass_context
def gc(ctx):
    """ get configuration information for patten_email class"""
    senders = ctx.invoke(gs)
    asm = ctx.invoke(ga)
    templates = ctx.invoke(gt)
    ip_pools= ctx.invoke(gi)

    auto_generated_config_dict = {}
    auto_generated_config_dict['api_key'] = ctx.obj.get('api_key')
    auto_generated_config_dict['senders'] = json.loads(senders.decode('utf-8'))
    auto_generated_config_dict['ip_pools'] = json.loads(ip_pools.decode('utf-8'))
    auto_generated_config_dict['unsubscribe_groups'] = json.loads(asm.decode('utf-8'))
    auto_generated_config_dict['email_templates'] = json.loads(templates.decode('utf-8'))

    click.echo(json.dumps(auto_generated_config_dict))




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
    params = {}
    response = ctx.obj['sg_client'].asm.groups.get(query_params=params)
    return response.body

@click.command()
@click.pass_context
def gt(ctx):
    """ get sendgird templates """
    response = ctx.obj['sg_client'].templates.get()
    return response.body


@click.command()
@click.pass_context
def gi(ctx):
    """ get sendgird ip pools """
    response = ctx.obj['sg_client'].ips.pools.get()
    return response.body

@click.command()
@click.argument('template_id')
@click.pass_context
def gtd(ctx, template_id):
    """ get all info about a specific template """
    response = ctx.obj['sg_client'].templates._(template_id).get()
    click.echo(response.body)
    click.echo(template_id)
    return response.body