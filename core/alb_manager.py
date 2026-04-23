import boto3
from config.config import *
from core.utils import logger

elbv2 = boto3.client("elbv2", region_name=REGION)
ec2 = boto3.client("ec2", region_name=REGION)


def get_default_vpc():
    vpcs = ec2.describe_vpcs(Filters=[{"Name": "isDefault", "Values": ["true"]}])
    return vpcs["Vpcs"][0]["VpcId"]


def get_subnets(vpc_id):
    subnets = ec2.describe_subnets(Filters=[{"Name": "vpc-id", "Values": [vpc_id]}])
    return [s["SubnetId"] for s in subnets["Subnets"]][:2]


def create_target_group(vpc_id):
    tg = elbv2.create_target_group(
    Name=TARGET_GROUP_NAME,
    Protocol="HTTP",
    Port=80,
    VpcId=vpc_id,
    TargetType="instance",
    Tags=[
        {'Key': PROJECT_TAG_KEY, 'Value': PROJECT_TAG_VALUE}
    ]
)
    return tg["TargetGroups"][0]["TargetGroupArn"]


def register_instance(tg_arn, instance_id):
    elbv2.register_targets(
        TargetGroupArn=tg_arn,
        Targets=[{"Id": instance_id}]
    )


def create_load_balancer(subnets, sg_id):
    lb = elbv2.create_load_balancer(
    Name=LOAD_BALANCER_NAME,
    Subnets=subnets,
    SecurityGroups=[sg_id],
    Scheme="internet-facing",
    Type="application",
    Tags=[
        {'Key': PROJECT_TAG_KEY, 'Value': PROJECT_TAG_VALUE}
    ]
)
    lb_data = lb["LoadBalancers"][0]
    return lb_data["LoadBalancerArn"], lb_data["DNSName"]


def create_listener(lb_arn, tg_arn):
    elbv2.create_listener(
        LoadBalancerArn=lb_arn,
        Protocol="HTTP",
        Port=80,
        DefaultActions=[{"Type": "forward", "TargetGroupArn": tg_arn}]
    )


def setup_alb(instance_id, alb_sg_id):
    vpc_id = get_default_vpc()
    subnets = get_subnets(vpc_id)

    tg_arn = create_target_group(vpc_id)
    register_instance(tg_arn, instance_id)

    lb_arn, dns = create_load_balancer(subnets, alb_sg_id)
    create_listener(lb_arn, tg_arn)

    logger.info(f"ALB ready: {dns}")
    return dns