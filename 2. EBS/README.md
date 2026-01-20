# EBS Volume Manager Web App

A simple Python web application for managing AWS Elastic Block Store (EBS) volumes using Flask and boto3.

## Features

- 📦 **List EBS Volumes** - View all EBS volumes in your AWS account with their details
- ➕ **Create Volumes** - Create new EBS volumes with configurable size and type
- 🗑️ **Delete Volumes** - Delete available EBS volumes (with confirmation)
- 🎨 **Modern UI** - Clean Bootstrap-based interface with responsive design

## Prerequisites

- Python 3.8+
- AWS credentials configured (via AWS CLI, environment variables, or IAM roles)
- AWS permissions for EC2 operations (describe-volumes, create-volume, delete-volume)

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd EBS
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure AWS credentials:**
   
   Option A - AWS CLI (recommended):
   ```bash
   aws configure
   ```
   
   Option B - Environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_REGION=us-east-1
   ```

   Option C - IAM Role (if running on AWS):
   The application will automatically use the attached IAM role

## Usage

1. **Start the web server:**
   ```bash
   python webapp.py
   ```

2. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **The application will display:**
   - All EBS volumes in the configured region
   - Volume details (ID, state, size, type, availability zone, creation time)
   - Options to create new volumes or delete existing ones

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_REGION` | AWS region to use | `us-east-1` |
| `AWS_ACCESS_KEY_ID` | AWS access key | (from AWS CLI config) |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | (from AWS CLI config) |

### Changing the Region

Set the environment variable before running:
```bash
export AWS_REGION=us-west-2  # For Oregon region
python webapp.py
```

Or modify the default in `webapp.py`:
```python
AWS_REGION = os.environ.get('AWS_REGION', 'us-west-2')
```

## Volume Types

The application supports all standard EBS volume types:

| Type | Description | Best For |
|------|-------------|----------|
| `gp2` | General Purpose SSD | Boot volumes, dev/test, small-to-medium databases |
| `gp3` | General Purpose SSD (newer) | Modern workloads with flexible IOPS/throughput |
| `io1` | Provisioned IOPS SSD | I/O-intensive applications, large databases |
| `io2` | Provisioned IOPS SSD (newer) | Mission-critical, highest durability |
| `st1` | Throughput Optimized HDD | Big data, data warehouses, log processing |
| `sc1` | Cold HDD | Infrequently accessed data, lowest cost |

## Security Notes

⚠️ **Important Security Considerations:**

1. **IAM Permissions**: Use least-privilege IAM policies. Example:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "ec2:DescribeVolumes",
                   "ec2:CreateVolume",
                   "ec2:DeleteVolume"
               ],
               "Resource": "*"
           }
       ]
   }
   ```

2. **Network Security**: In production, run behind a reverse proxy with HTTPS
3. **Authentication**: Add authentication if deploying publicly (e.g., Flask-Login)
4. **Rate Limiting**: Implement rate limiting for production use

## Project Structure

```
EBS/
├── webapp.py           # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── templates/
    ├── base.html      # Base template with navigation
    ├── index.html     # Volume listing page
    └── create.html    # Create volume form
```

## Troubleshooting

### Common Issues

1. **"Unable to locate credentials"**
   - Ensure AWS credentials are properly configured
   - Run `aws configure` or set environment variables

2. **"Access Denied"**
   - Check IAM permissions for EC2 operations
   - Verify the IAM user/role has necessary access

3. **"Volume in use" error when deleting**
   - Volumes must be detached before deletion
   - Detach from any attached instances first

4. **Region not found**
   - Verify the region name is correct (e.g., `us-east-1`)
   - Check if the service is available in that region

### Enable Debug Mode

Edit `webapp.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Deployment

### Docker (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "webapp.py"]
```

Build and run:
```bash
docker build -t ebs-manager .
docker run -p 5000:5000 -e AWS_REGION=us-east-1 ebs-manager
```

### AWS Elastic Beanstalk

1. Create `application.py`:
   ```python
   from webapp import app as application
   if __name__ == "__main__":
       application.run()
   ```

2. Create `Procfile`:
   ```
   web: gunicorn application:app
   ```

3. Deploy using EB CLI

## License

This is a sample application for educational purposes. Use at your own risk.

## Contributing

Feel free to extend this application with additional features:
- Volume attach/detach functionality
- Snapshot management
- Volume tagging
- Cost estimation
- CloudWatch monitoring integration

