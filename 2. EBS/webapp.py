from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
from botocore.exceptions import ClientError
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages

# Configure AWS region (can be changed via environment variable)
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')


def get_ec2_client():
    """Get EC2 client with configured region."""
    return boto3.client('ec2', region_name=AWS_REGION)


def list_ebs_volumes():
    """List all EBS volumes in the region."""
    ec2 = get_ec2_client()
    try:
        response = ec2.describe_volumes()
        volumes = response['Volumes']
        return [{
            'volume_id': vol['VolumeId'],
            'state': vol['State'],
            'size': vol['Size'],
            'volume_type': vol['VolumeType'],
            'availability_zone': vol['AvailabilityZone'],
            'create_time': vol['CreateTime'].strftime('%Y-%m-%d %H:%M:%S') if vol.get('CreateTime') else 'N/A'
        } for vol in volumes]
    except ClientError as e:
        flash(f'Error listing volumes: {e}', 'error')
        return []


def create_ebs_volume(availability_zone, size, volume_type='gp2'):
    """Create a new EBS volume."""
    ec2 = get_ec2_client()
    try:
        response = ec2.create_volume(
            AvailabilityZone=availability_zone,
            Size=int(size),
            VolumeType=volume_type
        )
        volume_id = response['VolumeId']
        flash(f'Successfully created EBS volume: {volume_id}', 'success')
        return volume_id
    except ClientError as e:
        flash(f'Error creating volume: {e}', 'error')
        return None


def delete_ebs_volume(volume_id):
    """Delete an EBS volume."""
    ec2 = get_ec2_client()
    try:
        ec2.delete_volume(VolumeId=volume_id)
        flash(f'Successfully deleted EBS volume: {volume_id}', 'success')
        return True
    except ClientError as e:
        flash(f'Error deleting volume: {e}', 'error')
        return False


def get_availability_zones():
    """Get list of availability zones in the current region."""
    ec2 = get_ec2_client()
    try:
        response = ec2.describe_availability_zones()
        return [az['ZoneName'] for az in response['AvailabilityZones']]
    except ClientError:
        return ['us-east-1a', 'us-east-1b', 'us-east-1c', 'us-east-1d', 'us-east-1e', 'us-east-1f']


@app.route('/')
def index():
    """Home page - list all EBS volumes."""
    volumes = list_ebs_volumes()
    return render_template('index.html', volumes=volumes, region=AWS_REGION)


@app.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new EBS volume."""
    if request.method == 'POST':
        availability_zone = request.form.get('availability_zone')
        size = request.form.get('size')
        volume_type = request.form.get('volume_type', 'gp2')
        
        if not availability_zone or not size:
            flash('Please provide both availability zone and size', 'error')
        else:
            create_ebs_volume(availability_zone, size, volume_type)
            return redirect(url_for('index'))
    
    availability_zones = get_availability_zones()
    return render_template('create.html', availability_zones=availability_zones)


@app.route('/delete/<volume_id>')
def delete(volume_id):
    """Delete an EBS volume."""
    delete_ebs_volume(volume_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

