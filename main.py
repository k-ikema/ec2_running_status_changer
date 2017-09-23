# -*- coding: utf-8 -*-
import boto3

REGION = "ap-northeast-1"
ec2_client = boto3.client("ec2")

def handle(event,context):

    instance_ids = event["instanceids"]
    for instance_id in instance_ids:
        ec2_instance_state = ec2_client.describe_instances(
            Filters = [
                {
                    'Name': 'instance-id',
                    'Values': [
                        instance_id
                    ]
                }
            ]
        )["Reservations"][0]["Instances"][0]["State"]["Name"]
        print instance_id + " : " + ec2_instance_state

if __name__ == "__main__":
    handle({},{})
