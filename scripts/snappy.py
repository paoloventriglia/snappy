import boto3
import click

session = boto3.Session(profile_name='snappy')
ec2 = session.resource('ec2')


@click.group()
def cli():
    """Snappy the snapshot manager"""


@cli.group('volumes')
def volumes():
    """Commands for volumes"""


@volumes.command('list')
@click.option('--nametag', default=None,
              help="Only instances for project (tag Project:<name>")
def list_volumes(nametag):
    """List EC2 volumes"""

    instances = filter_instances(nametag)

    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))

    return        




@cli.group('instances')
def instances():
    """Commands for instances"""


def filter_instances(nametag):
    instances = []

    if nametag:
        filters = [{'Name': 'tag:Name', 'Values': [nametag]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances


@instances.command('list')
@click.option('--nametag', default=None,
              help="Only instances for project (tag Project:<name>")
def list_instances(nametag):
    """List EC2 instances"""

    instances = filter_instances(nametag)

    for i in instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Name', '<notag>')
        )))
    return

@instances.command('stop')
@click.option('--nametag', default=None,
              help="Only instances for project (tag Project:<name>")
def stop_instances(nametag):
    """Stop EC2 Instances"""

    instances = filter_instances(nametag)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--nametag', default=None,
              help="Only instances for project (tag Project:<name>")
def stop_instances(nametag):
    """Start EC2 Instances"""

    instances = filter_instances(nametag)

    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()

    return


if __name__ == '__main__':
    cli()
