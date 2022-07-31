import boto3

client = boto3.client('dynamodb', endpoint_url='http://localhost:8000')


table = client.create_table (
    TableName = 'voting',
       KeySchema = [
           {
               'AttributeName': 'uid',
               'KeyType': 'HASH'
           },
           ],
           AttributeDefinitions = [
               {
                   'AttributeName': 'uid',
                   'AttributeType': 'N'
               }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits':10,
                'WriteCapacityUnits':10
            }
          
    )
print(table)