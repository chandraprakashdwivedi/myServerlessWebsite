service: sls-website 

provider:
  name: aws
  runtime: python3.6
  versionFunctions: false
  stage: dev
  region: ap-south-1

  

  iamRoleStatements:
    - Effect: "Allow"
      Action:
        - "s3:*"
      Resource: { "Fn::Join" : ["", ["arn:aws:s3:::", { "Ref" : "uploadBucket" } ] ]  }
    - Effect: "Allow"
      Action:
        - "sns:publish"
      Resource: "*"
    - Effect: "Allow"
      Action:
        - "sqs:*"
      Resource: "*"
    - Effect: "Allow"
      Action:
        - "dynamodb:*"
      Resource: "*"



functions:         
  weblink2:
    handler: lambda_functions/signup.lambda_handler
    memorySize: 128
    description: My function
    events:
        - http:
            path: lambda_functions/signup
            method: POST          
        - http:
            path: lambda_functions/login
            method: GET
             

resources:
  Resources:
      uploadBucket:
          Type: AWS::S3::Bucket
          Properties:
              BucketName: ${self:service}-${self:provider.stage}-uploads
              WebsiteConfiguration:
                IndexDocument: signup.html
                ErrorDocument: error.html
      TestDynamoDbTable:
          Type: 'AWS::DynamoDB::Table'
          DeletionPolicy: Retain
          Properties:
            AttributeDefinitions:
              -
                AttributeName: password
                AttributeType: S
              -
                AttributeName: user_name
                AttributeType: S
            KeySchema:
              -
                AttributeName: password
                KeyType: HASH
              -
                AttributeName: user_name
                KeyType: RANGE
            ProvisionedThroughput:
              ReadCapacityUnits: 1
              WriteCapacityUnits: 1
            TableName: ${self:service}-${self:provider.stage}-table1


