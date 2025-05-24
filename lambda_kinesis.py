import json
import boto3
import base64


def lambda_handler(event, context):
    output = []
    for record in event['records']:
        payload = record['data']
        transformed_data = payload['Name'],payload['Price']
        payload = base64.b64decode(transformed_data.encode('utf-8'))

        output_record = {
            'recordId' : record['recordId'],
            'result' : 'Ok',
            'data' : transformed_data
        }

        output.append(output_record)
    print(output)
    return {'records' : output}
        # print("de_serialize_payload", de_serialize_payload, type(de_serialize_payload))
        # print(de_serialize_payload['Name'],de_serialize_payload['Price'])
