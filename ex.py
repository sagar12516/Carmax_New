# import json
# import boto3
# import base64
#
#
# def lambda_handler(event, context):
#     for record in event['Records']:
#         payload = base64.b64decode(record['kinesis']['data'])
#         de_serialize_payload = json.loads(payload)
#         # print("de_serialize_payload", de_serialize_payload, type(de_serialize_payload))
#         print(de_serialize_payload['Name'],de_serialize_payload['Price'])

import pandas as pd
from fontTools.subset.svg import xpath
from pyspark.sql.functions import column

df = pd.read_parquet("/Users/venkatsagar/Downloads/five.parquet",engine='pyarrow')


df['model'] = df['name'].map(lambda x : x.split(' ')[0])

val_cts = df['model'].value_counts()

print(df.info)

# print(sorted(list(val_cts.index)))
# print(list(map(int,val_cts.values)))
# b = {}
# a = {'name':['sagar'], 'age' : [1]}
#
# for k,v in a.items():
#     if k in b:
#         b[k]+=v
#     else:
#         b[k]=v
#
# a = {'name':['vs'], 'age' : [2]}
# for k,v in a.items():
#     if k in b:
#         b[k]+=v
#     else:
#         b[k]=v
#
# df = pd.DataFrame.from_dict(b)
# print(type(int(df['name'].count())))
