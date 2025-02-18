import os
import requests
import cv2
import numpy as np
import boto3

# AWS credentials
AWS_ACCESS_KEY = 'AKIAXKPUZWFKHMHT5V4Z'
AWS_SECRET_KEY = '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'
AWS_REGION = 'ap-southeast-2'
BUCKET_NAME = 'comfyui123'

# Supabase credentials
SUPABASE_URL = "https://fuhqxfbyvrklxggecynt.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ1aHF4ZmJ5dnJrbHhnZ2VjeW50Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzc4ODk0MzcsImV4cCI6MjA1MzQ2NTQzN30.0r2cHr8g6nNwjaVaVGuXjo9MXNFu9_rx40j5Bb3Ib2Q"
BUCKET_NAME_SUPABASE = '360video'

# Create the S3 client with AWS credentials
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# Function to get the latest video from the S3 bucket
def get_latest_video_from_s3(bucket_name):
    try:
        # List all objects in the S3 bucket
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            # Sort objects by the LastModified timestamp to get the latest video
            latest_video = max(response['Contents'], key=lambda x: x['LastModified'])
            return latest_video['Key']
        else:
            print("No objects found in the bucket.")
            return None
    except Exception as e:
        print(f"Error getting latest video: {e}")
        return None

# Function to process the video from S3
def process_video_from_s3(bucket_name, logo_url, output_folder):
    try:
        latest_video_key = get_latest_video_from_s3(bucket_name)
        if latest_video_key:
            # Extract the original file name from the S3 key
            video_file_name = os.path.basename(latest_video_key)

            # Download the latest video from S3 to local storage with the original file name
            output_video_path = os.path.join(output_folder, video_file_name)
            s3.download_file(bucket_name, latest_video_key, output_video_path)
            print(f"Downloaded video to: {output_video_path}")

            # Add logo to the video (you can call your video processing function here)
            add_logo_to_video(output_video_path, logo_url)
            print(f"Logo added to the video: {output_video_path}")

            return output_video_path
        else:
            print("No latest video found.")
            return None
    except Exception as e:
        print(f"Error processing video from S3: {e}")
        return None

# Function to add logo to the video (you can replace this with your actual implementation)
def add_logo_to_video(video_path, logo_url):
    print(f"Adding logo from {logo_url} to video at {video_path}")
    # Implement your video processing logic here (e.g., using ffmpeg)
    # This is just a placeholder for the actual logo-adding logic

# Example usage
if __name__ == "__main__":
    bucket_name = 'comfyui123'
    logo_url = 'https://fuhqxfbyvrklxggecynt.supabase.co/storage/v1/object/public/360video/photos/tesco.png'  # Replace with your logo URL
    output_folder = 'output'  # Folder where you want to save the processed video

    # Process the video from S3 and add the logo
    process_video_from_s3(bucket_name, logo_url, output_folder)
