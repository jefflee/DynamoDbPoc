import boto3
import os
import json
import uuid

from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

TABLE_NAME = os.environ['DYNAMODB_TABLE']
table = dynamodb.Table(TABLE_NAME)


def create(event, context):
    body = json.loads(event['body'])
    customer_id = body['customer_id']
    survey_id = str(uuid.uuid4())
    survey_data = body['survey_data']
    table.put_item(
        Item={
            'pk': 'CUSTOMER#' + customer_id,
            'sk': 'SURVEY#' + survey_id,
            'survey_data': survey_data
        }
    )
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"survey_id": survey_id})
    }


def get(event, context):
    survey_id = event['pathParameters']['id']
    index_pk = Key('sk').eq('SURVEY#' + survey_id)
    response = table.query(
        IndexName='sk-pk-index',
        KeyConditionExpression=index_pk
    )
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(response['Items'][0])
    }


def get_all(event, context):
    customer_id = event['pathParameters']['id']
    pk = Key('pk').eq('CUSTOMER#' + customer_id)
    sk = Key('sk').begins_with('SURVEY#')
    expression = pk & sk
    response = table.query(
        KeyConditionExpression=expression
    )
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(response['Items'])
    }
