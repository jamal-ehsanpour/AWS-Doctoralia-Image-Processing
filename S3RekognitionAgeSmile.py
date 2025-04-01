import boto3
import pandas as pd
import requests

aws_access_key_id=input('Your aws access key')   # Insert your aws access key id 
aws_secret_access_key=input('Your aws secret access key')  # Insert your aws secret access key

# Initialize AWS clients
s3_client = boto3.client('s3' , aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
rekognition_client = boto3.client('rekognition' , aws_access_key_id=aws_access_key_id ,aws_secret_access_key=aws_secret_access_key )

# S3 bucket and folder details
BUCKET_NAME = 'doctoralia'
IMAGE_FOLDER = 'Images/'  # Folder in your S3 bucket

def upload_image_to_s3_from_url(image_url, bucket, s3_key):
    """Upload an image directly from a URL to an S3 bucket."""
    try:
        response = requests.get(image_url, stream=True)
        
        # Upload image to S3
        s3_client.put_object(
            Bucket=bucket,
            Key=s3_key,
            Body=response.content
        )
        return True
    except:
        return "Not Available"

def analyze_image_with_rekognition(bucket, image_key):
    """Analyze an image using AWS Rekognition to detect Faces and its attributes (age, smiling)."""
    try:

        response = rekognition_client.detect_faces(
        Image={'S3Object': {'Bucket': bucket, 'Name': image_key}},
        Attributes=['ALL'] 
        )
    
        attributes = response["FaceDetails"]

        age_range=attributes[0]['AgeRange']
        smiling=attributes[0]['Smile']
        eyeglasses=attributes[0]['Eyeglasses']
        sunglassses=attributes[0]['Sunglasses']
        gender=attributes[0]['Gender']
        beard=attributes[0]['Beard']
        mustache=attributes[0]['Mustache']
        eyesopen=attributes[0]['EyesOpen']
        mouthopen=attributes[0]['MouthOpen']
        emotions=attributes[0]['Emotions']
        landmarks=attributes[0]['Landmarks']
        pose=attributes[0]['Pose']
        quality=attributes[0]['Quality']
        confidence=attributes[0]['Confidence']
    
        return [age_range , smiling, eyeglasses, sunglassses,
                 gender, beard, mustache, eyesopen, mouthopen,
                 emotions, landmarks, pose, quality, confidence]
   
    except:
        return "Not available"
    

def process_images_from_csv(csv_file_path):
    """Main process to upload images from URLs, analyze them, and save the results."""
    # Read the CSV file containing image URLs
    df = pd.read_csv(csv_file_path)
    
    results_columns=['Age', 'Smiling', 'Eyeglasses', 'Sunglasses',
                     'Gender_', 'Beard', 'Mustache', 'Eyesopen', 'Mouthopen',
                      'Emotions', 'Landmarks', 'Pose', 'Quality', 'Confidence' ]
    
    for col in results_columns:
        df[col]=None
    
    for index, row in df.iterrows():
        try:

            image_url = row['Image Url']
            image_name = row['Doctor Name'] + '.jpg' if pd.notna(row['Doctor Name']) else f"image_{index}.jpg"
            s3_key = IMAGE_FOLDER + image_name

            # 1. Upload the image to S3 from the URL
            uploaded = upload_image_to_s3_from_url(image_url, BUCKET_NAME, s3_key)
            if not uploaded:
                continue
            print(f"Uploaded {image_name} to S3")

            # 2. Analyze the image using AWS Rekognition
            results = analyze_image_with_rekognition(BUCKET_NAME, s3_key)

            # 3. Append the result for the current image
            if results!="Not available":
                for col, result in zip(results_columns, results):
                    df.at[index, col]=result
            else:
                for col, result in zip(results_columns, results):
                    df.at[index, col]="Nan"
        except:
            return "Not Available"

    # 4. Save the results to a CSV file
    df.to_csv('Doctoralia_Italy_image_analysis_results.csv', index=False)
    print("Saved analysis results to image_analysis_results.csv")

# Path to the CSV file containing the image URLs
csv_file_path = 'DoctraliaData-Italy.csv'

# Start the process
process_images_from_csv(csv_file_path)
