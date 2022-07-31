from urllib import response
import boto3

client = boto3.client('dynamodb', endpoint_url='http://localhost:8000')


response = client.delete_table (
    TableName = 'voting',       
    )
print(response)