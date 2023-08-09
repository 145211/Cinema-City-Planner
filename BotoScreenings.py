import json
import os
import boto3

bucket_name = 'bucket-ccg'
s3_client = boto3.client('s3')

cinemas = json.load(open("cinemas.json", encoding='utf-8'))
local_folder = os.path.dirname(os.path.abspath(__file__))

for x in cinemas:
    s3_client.download_file(bucket_name, f'{x}.json', f'{local_folder}/screenings/{x}.json')

