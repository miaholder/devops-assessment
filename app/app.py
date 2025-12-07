from flask import Flask, request, jsonify
import boto3
import logging
import uuid


app = Flask(__name__)

# Enable logging
logging.basicConfig(level=logging.INFO)

# DynamoDB connection
dynamodb = boto3.resource("dynamodb", region_name="eu-west-2")
table = dynamodb.Table("feedback")


@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    data["id"] = str(uuid.uuid4())
    table.put_item(Item=data)
    logging.info("Saved feedback: %s", data)
    return jsonify({"message": "Feedback saved"}), 200


@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
