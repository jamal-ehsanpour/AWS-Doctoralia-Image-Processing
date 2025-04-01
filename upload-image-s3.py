import pandas as pd
import requests
import boto3
import io

df=pd.read_csv('SothebysData-London.csv')

aws_access_key_id=input('Your aws access key')
aws_secret_access_key=input('Your aws secret access key')
bucket_name='Doctralia'
s3_folder='Images/'

s3=boto3.client('s3' , aws_access_key_id=aws_access_key_id , aws_secret_access_key=aws_secret_access_key)

for index, row in df.iterrows():
    url=row['Image']
    try:
        response=requests.get(url, stream=True)
        if response.status_code==200:
            file_name=row['Title'] + '.jpg'
            s3_object_key=s3_folder + file_name
            file_stream=response.raw
            req_data=file_stream.read()
            s3.put_object(Body=req_data , Bucket=bucket_name , Key=s3_object_key)

            print(f'Uploaded {file_name} to  S3')
        else:
            print(f'Failed to download {url}')
    except Exception as e :
        print(f'Error processing {url}: {str(e)}')
