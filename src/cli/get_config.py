import click
import json
import re

# PaTTAN's preferred defaults, used when the matching option is not given on the
# command line. When the preferred name is absent from the SendGrid account the
# first item found is used instead.
PREFERRED_SENDER = 'no-reply@PaTTAN'
PREFERRED_IP_POOL = 'Pattan_Transactional'
PREFERRED_UNSUBSCRIBE_GROUP = 'PaTTAN Events'


def pick_default(requested, preferred, available, param_hint):
    """ Work out which key should become the DEFAULT entry for a config section.

    :param requested: name given on the command line, or None when the option was omitted
    :param preferred: PaTTAN's preferred name for this section
    :param available: the section built from the SendGrid account, keyed by name
    :param param_hint: option name, used when reporting a bad value
    :return: the key to copy to DEFAULT, or None when the section is empty
    :raises click.BadParameter: the requested name is not in the SendGrid account
    """
    if requested is not None:
        if requested not in available:
            known = ', '.join(available) if available else 'none'
            raise click.BadParameter(
                f'"{requested}" was not found in your SendGrid account. Available: {known}',
                param_hint=param_hint)
        return requested
    if preferred in available:
        return preferred
    if available:
        # whatever the SendGrid API listed first
        return next(iter(available))
    return None


@click.command()
@click.option('--default-sender', help=f'Sender label as defined in sendgrid. If left unset "{PREFERRED_SENDER}" is used when present, otherwise the first one found ')
@click.option('--default-ip-pool', help=f'Sendgird -> settings -> ip addresses . If left unset "{PREFERRED_IP_POOL}" is used when present, otherwise the first one found ')
@click.option('--default-unsubscribe_group', help=f'Sendgrid -> marketing -> unsubscribe group . If left unset "{PREFERRED_UNSUBSCRIBE_GROUP}" is used when present, otherwise the first one found ')
@click.pass_context
def gc(ctx, default_sender, default_ip_pool, default_unsubscribe_group):
    """ Get and format configuration for PattanEmail class"""
    senders = ctx.invoke(gs, dump_std=False)
    ip_pools = ctx.invoke(gi, dump_std=False)
    asm = ctx.invoke(ga, dump_std=False)
    templates = ctx.invoke(gt, dump_std=False)

    auto_generated_config_dict = {}
    auto_generated_config_dict['api_key'] = ctx.obj.get('api_key')


    sender_config = {}
    for sender in senders:
        del sender['updated_at']
        del sender['created_at']
        del sender['locked']
        del sender['id']
        del sender['verified']
        del sender['country']
        sender_config[sender['nickname']] = sender
        sender_config[sender['nickname']]['from_address'] = sender.pop('from')

    default_sender_key = pick_default(
        default_sender, PREFERRED_SENDER, sender_config, '--default-sender')
    if default_sender_key is not None:
        sender_config['DEFAULT'] = sender_config[default_sender_key]

    auto_generated_config_dict['senders'] = sender_config


    ip_pool_config = {}
    for ip_pool in ip_pools:
        ip_pool_config[ip_pool['name']] = ip_pool

    default_ip_pool_key = pick_default(
        default_ip_pool, PREFERRED_IP_POOL, ip_pool_config, '--default-ip-pool')
    if default_ip_pool_key is not None:
        ip_pool_config['DEFAULT'] = ip_pool_config[default_ip_pool_key]

    auto_generated_config_dict['ip_pools'] = ip_pool_config


    unsubscribe_groups_config = {}
    for unsubscribe_group in asm:
        unsubscribe_groups_config[unsubscribe_group['name']] = {}
        unsubscribe_groups_config[unsubscribe_group['name']]['id'] = unsubscribe_group['id']

    default_unsubscribe_group_key = pick_default(
        default_unsubscribe_group, PREFERRED_UNSUBSCRIBE_GROUP,
        unsubscribe_groups_config, '--default-unsubscribe_group')
    if default_unsubscribe_group_key is not None:
        unsubscribe_groups_config['DEFAULT'] = \
            unsubscribe_groups_config[default_unsubscribe_group_key]

    auto_generated_config_dict['unsubscribe_groups'] = unsubscribe_groups_config

    templates_config = {}
    for template in templates:
        templates_config[template['name']]= {}
        templates_config[template['name']]['id'] = template['id']
        templates_config[template['name']]['name'] = template['name']
        isolated_template_variables = ctx.invoke(gtv, template_id = template['id'], dump_std=False)
        templates_config[template['name']]['variables'] = isolated_template_variables

    auto_generated_config_dict['email_templates'] = templates_config

    click.echo(json.dumps(auto_generated_config_dict))




@click.command()
@click.option('--dump-std', default=True )
@click.pass_context
def gs(ctx, dump_std):
    """ Get approved senders """
    response = ctx.obj['sg_client'].senders.get()
    body = response.body.decode('utf-8')
    if dump_std:
        click.echo(body)
    return json.loads(body)


@click.command()
@click.option('--dump-std', default=True )
@click.pass_context
def ga(ctx, dump_std):
    """ Get SendGrid ASMs (unsubscribe groups)"""
    params = {}
    response = ctx.obj['sg_client'].asm.groups.get(query_params=params)
    body = response.body.decode('utf-8')
    if dump_std:
        click.echo(body)
    return json.loads(body)

@click.command()
@click.option('--dump-std', default=True )
@click.pass_context
def gt(ctx, dump_std):
    """ Get SendGrid dynamic templates"""
    params = {'generations': 'dynamic'}
    response = ctx.obj['sg_client'].templates.get(query_params=params)
    body = response.body.decode('utf-8')
    if dump_std:
        click.echo(body)
    return json.loads(body)['templates']
    # return json.loads(response.body.decode('utf-8'))['templates']


@click.command()
@click.option('--dump-std', default=True )
@click.pass_context
def gi(ctx, dump_std):
    """ Get SendGrid IP pools """
    response = ctx.obj['sg_client'].ips.pools.get()
    body = response.body.decode('utf-8')
    if dump_std:
        click.echo(body)
    return json.loads(body)

@click.command()
@click.argument('template_id')
@click.option('--dump-std', default=True )
@click.pass_context
def gtd(ctx, template_id, dump_std):
    """ Get details for a specific template"""
    response = ctx.obj['sg_client'].templates._(template_id).get()
    body = json.loads(response.body.decode('utf-8'))
    # get the active version of the template
    template = None
    for version in body['versions']:
        if version['active'] == 1:
            template = version
            break
    if not template:
        # @todo convert logger
        pass
    del(body['versions'])
    body['template'] = template

    if dump_std:
        click.echo(body)
    return body

@click.command()
@click.argument('template_id')
@click.option('--dump-std', default=True )
@click.pass_context
def gtv(ctx, template_id, dump_std):
    """ Get the variables defined in a specific template"""

    body = ctx.invoke(gtd, template_id = template_id, dump_std=False)
    if not body['template']:
        return []
    # Regular expression to find all Mustache variables
    # @todo the parsing could be better also variables in the subject line are not detected.
    content_variables = re.findall(r'{{\s*([^}]+)\s*}}', body['template']['plain_content'])
    subject_variables = []
    if 'subject' in body['template'].keys():
        subject_variables = re.findall(r'{{\s*([^}]+)\s*}}', body['template']['subject'])

    try:
        # these are defined with the asm config, @todo find a better mustache pattern the extra '{' is weird
        content_variables.remove('{unsubscribe')
        content_variables.remove('{unsubscribe_preferences')
    except:
        pass

    if dump_std:
        click.echo(f"content variables {content_variables}")
        click.echo(f"subject variables {subject_variables}")
    return content_variables + subject_variables