import boto3
from botocore.exceptions import ClientError

def list_ebs_volumes():
    """List all EBS volumes in the region."""
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_volumes()
        volumes = response['Volumes']
        print(f"Found {len(volumes)} EBS volumes:")
        for vol in volumes:
            print(f"Volume ID: {vol['VolumeId']}, State: {vol['State']}, Size: {vol['Size']} GB")
    except ClientError as e:
        print(f"Error listing volumes: {e}")

def create_ebs_volume(availability_zone, size=1):
    """Create a new EBS volume."""
    ec2 = boto3.client('ec2')
    try:
        response = ec2.create_volume(
            AvailabilityZone=availability_zone,
            Size=size
        )
        volume_id = response['VolumeId']
        print(f"Created EBS volume: {volume_id}")
        return volume_id
    except ClientError as e:
        print(f"Error creating volume: {e}")
        return None

def delete_ebs_volume(volume_id):
    """Delete an EBS volume."""
    ec2 = boto3.client('ec2')
    try:
        ec2.delete_volume(VolumeId=volume_id)
        print(f"Deleted EBS volume: {volume_id}")
    except ClientError as e:
        print(f"Error deleting volume: {e}")

def main():
    """Main function to run basic EBS tests."""
    print("Starting EBS testing app...")

    # List existing volumes
    list_ebs_volumes()

    # Create a test volume (change AZ as needed)
    test_volume_id = create_ebs_volume('us-east-1a', size=1)

    if test_volume_id:
        # List volumes again to confirm creation
        list_ebs_volumes()

        # Optionally delete the test volume (uncomment to enable)
        # delete_ebs_volume(test_volume_id)

if __name__ == "__main__":
    main()
