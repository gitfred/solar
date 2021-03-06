import click
import sys
import time

from solar.core import signals
from solar.core.resource import virtual_resource as vr

from solar.interfaces.db import get_db


db = get_db()


def run():
    db.clear()

    resources = vr.create('nodes', 'templates/nodes_with_transports.yaml', {'count': 2})
    nodes = [x for x in resources if x.name.startswith('node')]
    node1, node2 = nodes

    hosts1 = vr.create('hosts_file1', 'resources/hosts_file', {})[0]
    hosts2 = vr.create('hosts_file2', 'resources/hosts_file', {})[0]
    node1.connect(hosts1, {
        'name': 'hosts:name',
        'ip': 'hosts:ip',
    })

    node2.connect(hosts1, {
        'name': 'hosts:name',
        'ip': 'hosts:ip',
    })

    node1.connect(hosts2, {
        'name': 'hosts:name',
        'ip': 'hosts:ip',
    })

    node2.connect(hosts2, {
        'name': 'hosts:name',
        'ip': 'hosts:ip',
    })


run()
