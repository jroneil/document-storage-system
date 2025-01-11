import boto3
import os
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
)

def upload_file_to_s3(file_path: str, bucket_name: str, s3_key: str) -> str:
    try:
        s3_client.upload_file(file_path, bucket_name, s3_key)
        return f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
    except NoCredentialsError:
        raise Exception("AWS credentials not found")
    except Exception as e:
        raise Exception(f"Failed to upload file to S3: {str(e)}")

def delete_file_from_s3(bucket_name: str, s3_key: str) -> bool:
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=s3_key)
        return True
    except Exception as e:
        raise Exception(f"Failed to delete file from S3: {str(e)}")