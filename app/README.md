# Feedback Web App Backend

A simple Flask backend for collecting feedback and storing it in AWS DynamoDB.

## Features

- POST `/submit` - Submit feedback (saves to DynamoDB)
- GET `/health` - Health check endpoint
- UUID-based primary keys
- Comprehensive logging
- Production-ready for AWS EC2

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure AWS Credentials

Ensure your AWS credentials are configured. On EC2, use an IAM role. Locally, use:

```bash
aws configure
```

### 3. Create DynamoDB Table

```bash
aws dynamodb create-table \
    --table-name feedback \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1
```

### 4. Run the Application

**Development:**
```bash
export FLASK_ENV=development
python app.py
```

**Production (EC2):**
```bash
export AWS_REGION=us-east-1
export PORT=5000
python app.py
```

## API Usage

### Health Check
```bash
curl http://localhost:5000/health
```

### Submit Feedback
```bash
curl -X POST http://localhost:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "message": "Great app!"}'
```

## Environment Variables

- `AWS_REGION` - AWS region (default: us-east-1)
- `PORT` - Server port (default: 5000)
- `FLASK_ENV` - Set to 'development' for debug mode

## IAM Permissions Required

Your EC2 instance role needs:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem"
      ],
      "Resource": "arn:aws:dynamodb:*:*:table/feedback"
    }
  ]
}
```
