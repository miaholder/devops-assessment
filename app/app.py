import os
import uuid
import logging
from datetime import datetime
from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION', 'us-east-1'))
table = dynamodb.Table('feedback')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'OK'}), 200

@app.route('/submit', methods=['POST'])
def submit_feedback():
    """Submit feedback to DynamoDB"""
    try:
        # Get JSON data from request
        feedback_data = request.get_json()
        
        if not feedback_data:
            logger.warning('Received empty feedback submission')
            return jsonify({'error': 'No data provided'}), 400
        
        # Generate UUID for primary key
        feedback_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Prepare item for DynamoDB
        item = {
            'id': feedback_id,
            'timestamp': timestamp,
            **feedback_data
        }
        
        # Save to DynamoDB
        table.put_item(Item=item)
        
        logger.info(f'Feedback submitted successfully: {feedback_id}')
        
        return jsonify({
            'message': 'Feedback submitted successfully',
            'id': feedback_id
        }), 201
        
    except ClientError as e:
        logger.error(f'DynamoDB error: {e.response["Error"]["Message"]}')
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Use environment variables for production configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
