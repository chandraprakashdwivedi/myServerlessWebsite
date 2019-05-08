import json
import boto3

print("calling lambda fucntion")

dynamodb = boto3.resource('dynamodb')
table_name = 'sls-website-dev-table1'

bucket = 'sls-website-dev-uploads'


def lambda_handler(event, context):
    print("event", event)
    table = dynamodb.Table(table_name)
    requested_resource = event['resource']
    http_method = event['httpMethod']
    if http_method == 'POST':
      return post_call_method(requested_resource,table,event,bucket)
    else:
      return get_call_method(requested_resource,table,event,bucket)

def post_call_method(requested_resource,table,event):
    if '/lambda_functions/login' == requested_resource:
        return login_call(table, event)
    elif '/lambda_functions/signup' == requested_resource:
        return signin_call(table, event)
    else:
         return create_response(body='Not Found.', status_code=500)
        
def get_call_method(requested_resource,table,event,bucket):
    if '/lambda_functions/upload' == requested_resource:
        return sign_s3(event,bucket)
    else:
        return create_response(body='Not Found', status_code=500)
    
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
        return create_response(body='User name and password not matched.', status_code=500)
    return create_response(body='Succefully Logged in.')
  
  
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
        return create_response(body='User Registered Successfully')
    return create_response(body='Please choose different user name', status_code=500)



def sign_s3(event,bucket):
    if 'queryStringParameters' in event and event['queryStringParameters'] is not None:
        queryStringParameters = event['queryStringParameters']

    
    file_name = str(queryStringParameters['file-name'])
    file_type = str(queryStringParameters['file-type'])

    s3 = boto3.client('s3')
    
    print('your bucket type is: ',bucket)
    presigned_post = s3.generate_presigned_post(
      Bucket = bucket,  
      Key = file_name,
      Fields = {"acl": "public-read", "Content-Type": file_type},
      Conditions = [
         {"acl": "public-read"},
         {"Content-Type": file_type}
       ],
    ExpiresIn = 3600
    )
       
    signed_data = json.dumps({
        'data': presigned_post,
        'url': 'https://{}.s3.amazonaws.com/{}'.format(bucket, file_name)
      }) 
       
    
    print(signed_data)
    return  create_response(signed_data)

def create_response(body, status_code=200):
    body_json = {'message': body, 'status_code':status_code}
    return {
          "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body_json)
        }
