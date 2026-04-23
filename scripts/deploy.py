



from core.security_manager import create_alb_security_group, create_ec2_security_group
from core.ec2_manager import create_key_pair, launch_instance, get_my_ip
from core.alb_manager import setup_alb

print("Starting deployment...")

create_key_pair()

ip = get_my_ip()

alb_sg = create_alb_security_group()
ec2_sg = create_ec2_security_group(ip, alb_sg)

instance_id = launch_instance(ec2_sg)

dns = setup_alb(instance_id, alb_sg)

print("\n🚀 Deployment complete")
print(f"URL: http://{dns}")