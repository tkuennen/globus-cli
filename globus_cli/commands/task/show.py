import click

from globus_cli.parsing import common_options, task_id_arg
from globus_cli.helpers import (
    outformat_is_json, print_json_response, colon_formatted_print, print_table)

from globus_cli.services.transfer import get_client, print_json_from_iterator


COMMON_FIELDS = [
    ('Label', 'label'),
    ('Task ID', 'task_id'),
    ('Type', 'type'),
    ('Directories', 'directories'),
    ('Files', 'files'),
    ('Status', 'status'),
    ('Request Time', 'request_time'),
]

ACTIVE_FIELDS = [
    ('Deadline', 'deadline'),
    ('Details', 'nice_status'),
]

COMPLETED_FIELDS = [
    ('Completion Time', 'completion_time'),
]

DELETE_FIELDS = [
    ('Endpoint', 'source_endpoint_display_name'),
]

TRANSFER_FIELDS = [
    ('Source Endpoint', 'source_endpoint_display_name'),
    ('Destination Endpoint', 'destination_endpoint_display_name'),
]

SUCCESSFULL_TRANSFER_FIELDS = [
    ('Source', 'source_path'),
    ('Destination', 'destination_path')
]


def print_successful_transfers(client, task_id):
    res = client.task_successful_transfers(task_id, num_results=None)

    if outformat_is_json():
        print_json_from_iterator(res)
    else:
        print_table(res, SUCCESSFULL_TRANSFER_FIELDS)


def print_task_detail(client, task_id):
    res = client.get_task(task_id)

    if outformat_is_json():
        print_json_response(res)
    else:
        fields = COMMON_FIELDS + \
            (COMPLETED_FIELDS if res['completion_time'] else ACTIVE_FIELDS) + \
            (DELETE_FIELDS if res['type'] == 'DELETE' else TRANSFER_FIELDS)
        colon_formatted_print(res, fields)


@click.command('show', help='Show detailed information about a specific Task')
@common_options
@task_id_arg
@click.option('--successful-transfers', '-t', is_flag=True, default=False,
              help='Show files that were transferred as result of this task.')
def show_task(successful_transfers, task_id):
    """
    Executor for `globus task show`
    """
    client = get_client()

    if successful_transfers:
        print_successful_transfers(client, task_id)
    else:
        print_task_detail(client, task_id)
