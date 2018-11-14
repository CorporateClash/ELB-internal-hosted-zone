import os

import boto3

vpc_id = os.environ.get('vpc_id')
hosted_zone_id = os.environ.get('hosted_zone_id')
hosted_zone_record_name = os.environ.get('hosted_zone_record_name')

def update(event, context):
    ec2Client = boto3.client('ec2')
    r53Client = boto3.client('route53')
    interfaces = ec2Client.describe_network_interfaces(
        Filters=[
            {
                'Name': 'vpc-id',
                'Values': [vpc_id]
            }
        ]
    )
    privateips = []
    for interface in interfaces["NetworkInterfaces"]:
        try:
            if interface["PrivateIpAddresses"][0]["Association"]["IpOwnerId"] == "amazon-elb":
                privateips.append(interface["PrivateIpAddress"])
        except KeyError:
            continue

    route = r53Client.list_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        StartRecordName=hosted_zone_record_name,
        StartRecordType='A',
        MaxItems='1'
    )["ResourceRecordSets"][0]

    record_ip = route["ResourceRecords"][0]["Value"]
    if record_ip in privateips:
        return 'No update needed'
    r53Client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Comment': 'Update with new ELB internal ip',
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': hosted_zone_record_name,
                        'Type': 'A',
                        'TTL': 300,
                        'ResourceRecords': [{'Value': privateips[0]}]
                    }
                }
            ]
        }
    )
    return 'updated'
