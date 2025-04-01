import boto3
import os
from datetime import datetime

rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['RESULTS_TABLE_NAME'])

def handler(event, context):
    # Get uploaded file info
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Call Rekognition
    response = rekognition.detect_faces(
        Image={'S3Object': {'Bucket': bucket, 'Name': key}},
        Attributes=['ALL']
    )
    
    # Extract desired attributes
    face_details = response['FaceDetails'][0]  # Assuming single face
    result = {
        'image_name': key.split('/')[-1],
        'timestamp': datetime.now().isoformat(),
        'age_range': f"{face_details['AgeRange']['Low']}-{face_details['AgeRange']['High']}",
        'smile': face_details['Smile']['Value'],
        'glasses': face_details['Eyeglasses']['Value'],
        'sunglasses': face_details['Sunglasses']['Value'],
        'gender': face_details['Gender']['Value'],
        'emotions': [e['Type'] for e in face_details['Emotions'] if e['Confidence'] > 50]
    }
    
    # Save to DynamoDB
    table.put_item(Item=result)
    
    return result