import boto3
from pprint import pprint

TABLE_NAME = 'voting'

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
table = dynamodb.Table(TABLE_NAME)


client = boto3.client('dynamodb', endpoint_url='http://localhost:8000')

def put(): 
    response = table.put_item (
        TableName = TABLE_NAME,
        Item = {
            'uid': 31,
            'name': 'Jammy',
            'age': 25,
            'details': {
                'height': '6ft 2inch',
                'likes': ['Skyrim', 'Mass Effect']
            }
        },
        ConditionExpression = "attribute_not_exists(uid)"
    )
    print(response)

def update():
    response = table.update_item(
        Key={'uid': 31},
        UpdateExpression='SET details.height = :newName',
        ExpressionAttributeValues={
            ':newName': "Gdam"
        },
    )
    print(response)


def delete():
    response = table.delete_item(
        Key={
            'uid': 30 
        }
    )
    print(response)


def get():
    response = table.get_item(
        Key={
            "uid": 18605,
        }
    )
    pprint(response['Item'])

def scan():
    pprint(table.scan()['Items'])

#put()
#update()
#delete()
#scan()
#pprint(client.list_tables()['TableNames'])
get()