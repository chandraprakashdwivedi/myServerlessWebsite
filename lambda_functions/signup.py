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
      return create_reponse("Nothing for GET as of now")

def post_call_method(requested_resource, table,event):
    if '/lambda_functions/login' == requested_resource:
        return login_call(table, event)
    elif 'lambda_functions/signup' == requested_resource:
        return signin_call(table, event)
    else:
        return create_reposne('404 Not Found')
        

    
def login_call(table,event):
    if 'body' in event and event['body'] is not None:
        body = json.loads(event['body'])
    key = {
        "user_name": body['user_name'],
        "password": body['password']
        }
    data = table.get_item(TableName=table_name,Key=key)
    
    print('data', data)
    if not data:
        return create_response('User name and password not matched.')
    return create_response('Succefully Logged in.')
  
  
def signin_call(table,event):
    if 'body' in event and event['body'] is  not None:
        body = json.loads(event['body'])
    item = {
        "user_name": body['user_name'],
        "password": body['password']
        }
    data = table.get_item(TableName=table_name,Key=item(user_name))
    if not data:
        table.put_item(Item=item)
    return create_response('Please choose different user name')
        

def create_response(body):
    return {
        "statusCode": 200,
        "body": body
        }
