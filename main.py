# -*- coding: utf-8 -*-
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2_client = boto3.client("ec2")

def handle(event,context):

    if event.has_key("instanceids"):
        instance_ids = event["instanceids"]
    else:
        instance_ids = [
        ]
    
    if len(instance_ids) <= 0:
        return "Target is empty."

    for instance_id in instance_ids:
        ec2_instance_state = ec2_client.describe_instances(
            Filters=[
                {
                    'Name': 'instance-id',
                    'Values': [
                        instance_id
                    ]
                }
            ]
        )["Reservations"][0]["Instances"][0]["State"]["Name"]
        print instance_id + " : " + ec2_instance_state

        if ec2_instance_state == "stopped":
            response = start_instance(instance_id)
        else:
            response = stop_instance(instance_id)

        current_state = response["CurrentState"]["Name"]
        logger.info("Instance %s status was turned into %s." % (instance_id, current_state))

def start_instance(instance_id):
    response = ec2_client.start_instances(InstanceIds=[instance_id])
    return response["StartingInstances"][0]

def stop_instance(instance_id):
    response = ec2_client.stop_instances(InstanceIds=[instance_id])
    return response["StoppingInstances"][0]

if __name__ == "__main__":
    handle({}, {})
