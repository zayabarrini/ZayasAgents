# incident_remediation.py
import boto3
import os
import logging
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """
    Lambda function for automatic incident remediation
    """
    alarm_name = event['detail']['alarmName']
    region = event['region']
    
    ec2 = boto3.client('ec2', region_name=region)
    autoscaling = boto3.client('autoscaling', region_name=region)
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    
    logger.info(f"Processing alarm: {alarm_name}")
    
    if "high-cpu" in alarm_name:
        return handle_high_cpu(autoscaling, cloudwatch)
    elif "5xx-errors" in alarm_name:
        return handle_5xx_errors(autoscaling, ec2)
    else:
        logger.warning(f"No specific handler for alarm: {alarm_name}")
        return {"status": "no_action_taken"}

def handle_high_cpu(autoscaling, cloudwatch):
    """Remediate high CPU incidents"""
    try:
        # Get the auto scaling group
        asg_name = os.environ['ASG_NAME']
        
        # Check if we're already at max capacity
        response = autoscaling.describe_auto_scaling_groups(
            AutoScalingGroupNames=[asg_name]
        )
        
        asg = response['AutoScalingGroups'][0]
        current_capacity = asg['DesiredCapacity']
        max_capacity = asg['MaxSize']
        
        if current_capacity < max_capacity:
            # Scale out by 1 instance
            new_capacity = current_capacity + 1
            autoscaling.set_desired_capacity(
                AutoScalingGroupName=asg_name,
                DesiredCapacity=new_capacity,
                HonorCooldown=False
            )
            logger.info(f"Scaled out ASG {asg_name} to {new_capacity}")
            return {"status": "scaled_out", "new_capacity": new_capacity}
        else:
            logger.warning(f"ASG {asg_name} already at max capacity")
            return {"status": "at_max_capacity"}
            
    except Exception as e:
        logger.error(f"Error handling high CPU: {str(e)}")
        return {"status": "error", "error": str(e)}

def handle_5xx_errors(autoscaling, ec2):
    """Remediate 5XX errors by replacing unhealthy instances"""
    try:
        asg_name = os.environ['ASG_NAME']
        
        # Get unhealthy instances
        response = autoscaling.describe_auto_scaling_groups(
            AutoScalingGroupNames=[asg_name]
        )
        
        asg = response['AutoScalingGroups'][0]
        unhealthy_instances = [
            instance for instance in asg['Instances'] 
            if instance['HealthStatus'] != 'Healthy'
        ]
        
        if unhealthy_instances:
            instance_ids = [inst['InstanceId'] for inst in unhealthy_instances]
            
            # Terminate unhealthy instances (ASG will launch replacements)
            autoscaling.terminate_instance_in_auto_scaling_group(
                InstanceId=instance_ids[0],
                ShouldDecrementDesiredCapacity=False
            )
            logger.info(f"Terminated unhealthy instance: {instance_ids[0]}")
            return {"status": "instance_replaced", "instance_id": instance_ids[0]}
        else:
            logger.info("No unhealthy instances found")
            return {"status": "no_unhealthy_instances"}
            
    except Exception as e:
        logger.error(f"Error handling 5XX errors: {str(e)}")
        return {"status": "error", "error": str(e)}