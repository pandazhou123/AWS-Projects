# EBS Testing App

A simple Python script to test basic Elastic Block Store (EBS) operations using AWS SDK (boto3).

## Prerequisites

- Python 3.x
- AWS CLI configured with appropriate permissions (e.g., EC2FullAccess)
- boto3 library: `pip install boto3`

## Usage

Run the script to perform basic EBS tests:

```bash
python webapp.py
```

The script will:
1. List all existing EBS volumes in the current region
2. Create a new 1GB EBS volume in us-east-1a
3. List volumes again to confirm creation
4. Optionally delete the test volume (uncomment the line in main() if desired)

## Functions

- `list_ebs_volumes()`: Lists all EBS volumes with their ID, state, and size
- `create_ebs_volume(az, size)`: Creates a new EBS volume in the specified availability zone
- `delete_ebs_volume(volume_id)`: Deletes the specified EBS volume

## Note

This is a basic testing script. In a production environment, ensure proper error handling and security measures are in place.
