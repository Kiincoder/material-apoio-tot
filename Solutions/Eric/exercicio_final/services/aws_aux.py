import boto3
from config.config import (
  ENDPOINT_URL,
  AWS_ACCESS_KEY_ID,
  AWS_SECRET_ACCESS_KEY,
  AWS_REGION,
  SQS_MESSAGE_GROUP_ID
)

s3_client = boto3.client(
    "s3",
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

sqs_client = boto3.client(
    "sqs",
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def send_message(message_body, queue_url):
  sqs_client.send_message(
    QueueUrl=queue_url,
    MessageBody=message_body,
    MessageGroupId=SQS_MESSAGE_GROUP_ID
  )

def receive_message(queue_url):
  response = sqs_client.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=1,
    WaitTimeSeconds=10,
    VisibilityTimeout=30
  )
  messages = response.get("Messages", [])
  if len(messages) != 0:
    return messages
  return None

def delete_message(message, queue_url):
  sqs_client.delete_message(
    QueueUrl=queue_url,
    ReceiptHandle=message["ReceiptHandle"]
  )

def put_object_bucket(key, body, bucket_name):
  s3_client.put_object(
    Bucket=bucket_name,
    Key=key,
    Body=body
  )

def get_object_bucket(key, bucket_name):
  object = s3_client.get_object(
    Bucket=bucket_name,
    Key=key
  )
  return object
