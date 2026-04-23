from core.ec2_manager import launch_instance, get_my_ip
from core.security_manager import create_alb_security_group, create_ec2_security_group

ip = get_my_ip()

alb_sg = create_alb_security_group()
ec2_sg = create_ec2_security_group(ip, alb_sg)

instance_id = launch_instance(ec2_sg)

print("Instance ID:", instance_id)