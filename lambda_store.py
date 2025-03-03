import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("RaspberryPi4-SensorData")

def lambda_handler(event, context):
    for record in event["Records"]:
        payload = json.loads(record["body"])
        table.put_item(Item=payload)
    
    return {"statusCode": 200, "body": "Data Stored Successfully"}
