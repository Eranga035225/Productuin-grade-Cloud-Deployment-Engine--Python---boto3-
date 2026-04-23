import boto3
import time
from config.config import *

ec2 = boto3.client("ec2", region_name=REGION)
elbv2 = boto3.client("elbv2", region_name=REGION)

print("🧹 Safe lifecycle cleanup starting...")

# -----------------------------
# 1. EC2 (TAG BASED)
# -----------------------------
res = ec2.describe_instances(
    Filters=[
        {"Name": f"tag:{PROJECT_TAG_KEY}", "Values": [PROJECT_TAG_VALUE]},
        {"Name": "instance-state-name", "Values": ["pending", "running", "stopping", "stopped"]}
    ]
)

instance_ids = [
    i["InstanceId"]
    for r in res["Reservations"]
    for i in r["Instances"]
]

if instance_ids:
    print("🔻 Terminating EC2:", instance_ids)
    ec2.terminate_instances(InstanceIds=instance_ids)
    ec2.get_waiter("instance_terminated").wait(InstanceIds=instance_ids)

# -----------------------------
# 2. ALB (TAG BASED)
# -----------------------------
lbs = elbv2.describe_load_balancers()["LoadBalancers"]

for lb in lbs:
    tags = elbv2.describe_tags(ResourceArns=[lb["LoadBalancerArn"]])["TagDescriptions"][0]["Tags"]

    if any(t["Key"] == PROJECT_TAG_KEY and t["Value"] == PROJECT_TAG_VALUE for t in tags):
        print("🔻 Deleting ALB:", lb["LoadBalancerName"])
        elbv2.delete_load_balancer(LoadBalancerArn=lb["LoadBalancerArn"])
        time.sleep(40)

# -----------------------------
# 3. TARGET GROUP (TAG BASED)
# -----------------------------
tgs = elbv2.describe_target_groups()["TargetGroups"]

for tg in tgs:
    tags = elbv2.describe_tags(ResourceArns=[tg["TargetGroupArn"]])["TagDescriptions"][0]["Tags"]

    if any(t["Key"] == PROJECT_TAG_KEY and t["Value"] == PROJECT_TAG_VALUE for t in tags):
        print("🔻 Deleting TG:", tg["TargetGroupName"])
        elbv2.delete_target_group(TargetGroupArn=tg["TargetGroupArn"])

# -----------------------------
# 4. SECURITY GROUPS (TAG BASED)
# -----------------------------
sgs = ec2.describe_security_groups()["SecurityGroups"]

for sg in sgs:
    tags = sg.get("Tags", [])

    if any(t["Key"] == PROJECT_TAG_KEY and t["Value"] == PROJECT_TAG_VALUE for t in tags):
        try:
            print("🔻 Deleting SG:", sg["GroupName"])
            ec2.delete_security_group(GroupId=sg["GroupId"])
        except Exception as e:
            print("⚠️ Skipping SG:", e)

print("🎉 Lifecycle cleanup complete")