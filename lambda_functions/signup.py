import json
import boto3

print("calling lambda fucntion")

dynamodb = boto3.resource('dynamodb')
table_name = 'sls-website-dev-table1'


def lambda_handler(event, context):
    print("event", event)
    table = dynamodb.Table(table_name)
    requested_resource = event['resource']
    http_method = event['httpMethod']
    if http_method == 'POST':
      return post_call_method(requested_resource,table,event)
    else:
      return get_call_method(requested_resource, table,event)

def post_call_method(requested_resource, table,event):
    if '/lambda_functions/login' == requested_resource:
        return login_call(table, event)
    elif '/lambda_functions/signup' == requested_resource:
        return signin_call(table, event)
    else:
        return create_response('404 Not Found')
        
def get_call_method(requested_resource, table,event):
   
        return create_response('No Get request yet')
    
def login_call(table,event):
    if 'body' in event and event['body'] is not None:
        body = json.loads(event['body'])
    key = {
        "user_name": body['user_name'],
        "password": body['password']
        }
    data = table.get_item(Key=key)
    
    print('data', data)

    if 'Item' not in data:
        return create_response('User name and password not matched.')
    return create_response('Succefully Logged in.')
  
  
def signin_call(table,event):
    if 'body' in event and event['body'] is  not None:
        body = json.loads(event['body'])
    item = {
        "user_name": body['user_name'],
        "password": body['password']
        }
    data = table.get_item(Key=item)
    print('data', data)
    if 'Item' not in data:
        table.put_item(Item=item)
        return create_response('User Registered Successfully')
    return create_response('Please choose different user name')
        

def create_response(body):
    return {
          "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": body
        }
