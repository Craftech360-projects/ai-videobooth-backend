import boto3
from datetime import datetime, timedelta
import time


# AWS credentials and configuration
AWS_ACCESS_KEY_ID = 'AKIAXKPUZWFKHMHT5V4Z'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION = 'ap-southeast-2'
S3_BUCKET_NAME = "comfyui123"

# Initialize the S3 client
s3 = boto3.client('s3', 
                  aws_access_key_id=AWS_ACCESS_KEY_ID, 
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
                  region_name=AWS_REGION)

def upload_test_files(unique_number):
    """
    Uploads test files to the S3 bucket with a specific prefix.
    """
    try:
        # Simulate uploading multiple files with different timestamps
        for i in range(3):
            file_name = f"videos/{unique_number}/test_file_{i}.txt"
            file_data = f"This is test file {i} for unique_number {unique_number}".encode('utf-8')
            s3.put_object(Bucket=S3_BUCKET_NAME, Key=file_name, Body=file_data)
            print(f"Uploaded {file_name} to S3.")

            # Simulate a delay to ensure different LastModified timestamps
            if i < 2:
                print("Waiting 5 seconds before uploading the next file...")
                time.sleep(5)

    except Exception as e:
        print(f"Error uploading test files: {str(e)}")
        raise

def get_latest_file(unique_number):
    """
    Retrieves the latest file from the S3 bucket based on the prefix.
    """
    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=f"videos/{unique_number}/")
        if 'Contents' in response:
            # Find the latest file based on LastModified timestamp
            latest_file = max(response['Contents'], key=lambda x: x['LastModified'])['Key']
            video_link = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{latest_file}"
            print("Latest video link:", video_link)
            return video_link
        else:
            print("No files found for the given prefix.")
            return None

    except Exception as e:
        print(f"Error retrieving latest file: {str(e)}")
        raise

def test_latest_file_retrieval():
    """
    Tests the retrieval of the latest file from the S3 bucket.
    """
    try:
        # Simulate a unique number (e.g., from a video processing job)
        unique_number = "12345"

        # Step 1: Upload test files to S3
        print("Uploading test files to S3...")
        upload_test_files(unique_number)

        # Step 2: Retrieve the latest file
        print("\nRetrieving the latest file from S3...")
        latest_file_link = get_latest_file(unique_number)

        if latest_file_link:
            print("Test passed: Latest file link retrieved successfully.")
        else:
            print("Test failed: No files found or error retrieving the latest file.")

    except Exception as e:
        print(f"Test failed with error: {str(e)}")

if __name__ == "__main__":
    # Run the test
    test_latest_file_retrieval()