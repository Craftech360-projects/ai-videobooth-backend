import boto3
import requests
import os
from supabase import create_client, Client
import cv2
import numpy as np

# AWS S3 credentials and bucket details
AWS_ACCESS_KEY = 'AKIAXKPUZWFKHMHT5V4Z'
AWS_SECRET_KEY = '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'
BUCKET_NAME = 'comfyui123'

# Supabase credentials
SUPABASE_URL = "https://fuhqxfbyvrklxggecynt.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ1aHF4ZmJ5dnJrbHhnZ2VjeW50Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzc4ODk0MzcsImV4cCI6MjA1MzQ2NTQzN30.0r2cHr8g6nNwjaVaVGuXjo9MXNFu9_rx40j5Bb3Ib2Q"
BUCKET_NAME_SUPABASE = '360video'

# Initialize S3 client
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def download_from_s3(url, local_path):
    """Download a file from S3 given its URL."""
    response = requests.get(url, stream=True)
    with open(local_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def download_from_supabase_url(url, local_path):
    """Download a file from a Supabase public URL."""
    response = requests.get(url)
    with open(local_path, 'wb') as file:
        file.write(response.content)

def upload_to_s3(local_path, s3_key):
    """Upload a file to S3."""
    s3_client.upload_file(local_path, BUCKET_NAME, s3_key)

def overlay_logo(video_path, logo_path, output_path):
    # Load the logo with an alpha channel (if available)
    logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)

    # Check if the logo has an alpha channel (transparency)
    if logo.shape[2] == 4:
        logo_bgr = logo[:, :, :3]  # Extract BGR channels
        logo_mask = logo[:, :, 3]  # Extract alpha channel
    else:
        logo_bgr = logo
        logo_mask = np.ones(logo_bgr.shape[:2], dtype=np.uint8) * 255  # Create a white mask

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define output video writer
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Stop when video ends

        # Get the logo position (top-center)
        l_h, l_w = logo_bgr.shape[:2]
        x_offset = (width - l_w) // 2  # Center horizontally
        y_offset = 10  # 10px margin from top

        # Get the region of interest (ROI) in the frame
        roi = frame[y_offset:y_offset+l_h, x_offset:x_offset+l_w]

        # Blend the logo with the frame using the mask
        roi_bg = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(logo_mask))
        logo_fg = cv2.bitwise_and(logo_bgr, logo_bgr, mask=logo_mask)
        combined = cv2.add(roi_bg, logo_fg)

        # Place the combined logo in the frame
        frame[y_offset:y_offset+l_h, x_offset:x_offset+l_w] = combined

        # Write the frame to output video
        out.write(frame)

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def main(video_url, logo_supabase_url, output_s3_key, local_save_path):
    # Temporary file paths
    video_path = 'temp_video.mp4'
    logo_path = 'temp_logo.png'

    # Download video from S3
    download_from_s3(video_url, video_path)

    # Download logo from Supabase (using public URL)
    download_from_supabase_url(logo_supabase_url, logo_path)

    # Process video
    output_video_path = 'output_video.mp4'
    overlay_logo(video_path, logo_path, output_video_path)

    # Upload to S3
    upload_to_s3(output_video_path, output_s3_key)

    # Save a copy locally
    os.rename(output_video_path, local_save_path)

    # Clean up
    os.remove(video_path)
    os.remove(logo_path)

if __name__ == "__main__":
    video_url = "https://comfyui123.s3.ap-southeast-2.amazonaws.com/s3://comfyui123/comfyui-outputs/abilashs003@gmail.com_00002_.mp4"
    logo_supabase_url = "https://fuhqxfbyvrklxggecynt.supabase.co/storage/v1/object/public/360video/photos/tesco.png"  # URL to the logo in Supabase Storage
    output_s3_key = "path/in/s3/for/new-video.mp4"
    local_save_path = "final-video.mp4"

    main(video_url, logo_supabase_url, output_s3_key, local_save_path)



# curl -X 'POST' \
#   'http://127.0.0.1:8000/process-video/' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "video_url": "https://your-s3-bucket-url/video.mp4",
#   "logo_url": "https://fuhqxfbyvrklxggecynt.supabase.co/storage/v1/object/public/360video/photos/tesco.png"
# }'
