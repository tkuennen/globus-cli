import click

from globus_cli.parsing import common_options, endpoint_id_arg, role_id_arg
from globus_cli.safeio import formatted_print, FORMAT_TEXT_RECORD

from globus_cli.services.auth import lookup_identity_name

from globus_cli.services.transfer import get_client


def lookup_principal(role):
    return lookup_identity_name(role['principal'])


@click.command('show', help='Show full info for a role on an endpoint')
@common_options
@endpoint_id_arg
@role_id_arg
def role_show(endpoint_id, role_id):
    """
    Executor for `globus endpoint role show`
    """
    client = get_client()

    role = client.get_endpoint_role(endpoint_id, role_id)
    formatted_print(role, text_format=FORMAT_TEXT_RECORD,
                    fields=(('Principal Type', 'principal_type'),
                            ('Principal', lookup_principal), ('Role', 'role'))
                    )
