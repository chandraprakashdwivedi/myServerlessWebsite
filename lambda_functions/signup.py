import json
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    print("event", event)
    table = dynamodb.Table('sls-website-dev-table1')
    if 'body' in event and event['body'] is not None:
        body = json.loads(event['body'])
    item = {
        "user_name": body['user_name'],
        "password": body['password']
        }
    table.put_item(Item=item)
    
    resp = {
        "statusCode": 200,
        "body":json.dumps('Item Inserted successfully')

    }
    
    return resp
