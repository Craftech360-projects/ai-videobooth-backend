import logging
from supabase import create_client, Client
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import websocket
import uuid
import json
import urllib.request
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto3
# from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
from contextlib import asynccontextmanager
from threading import Thread
import os
from dotenv import load_dotenv
import time
from websocket._core import create_connection

# from websocket import create_connection
from datetime import datetime, timezone
from dateutil import parser
 
AWS_ACCESS_KEY_ID = 'AKIAXKPUZWFKHMHT5V4Z'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION = 'ap-southeast-2'
 
SUPABASE_URL = "https://vebsyinnadyvgmwbegel.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZlYnN5aW5uYWR5dmdtd2JlZ2VsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk2MDU2OTcsImV4cCI6MjA1NTE4MTY5N30._mX93lTANurl3POYaMYngGaGl71326BP4DXv9TbVp2w"
 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
 
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)
s3_bucket_name = "comfyui123"
 
# Email Configuration
SMTP_SERVER = "smtp.gmail.com"  # Change if using another provider
SMTP_PORT = 587
EMAIL_SENDER = "yamuna@craftech360.com"
EMAIL_PASSWORD = "tzufheddnviaylzo"
 
 
# Initialize the S3 client
s3 = boto3.client('s3', 
                  aws_access_key_id=AWS_ACCESS_KEY_ID, 
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
                  region_name=AWS_REGION)
 
s3_bucket_name = "comfyui123"
 
def upload_to_s3(file_data, file_name):
    try:
        s3.put_object(Bucket=s3_bucket_name, Key=file_name, Body=file_data)
        s3_url = f"https://{s3_bucket_name}.s3.amazonaws.com/{file_name}"
        print(f"Successfully uploaded to S3: {s3_url}")
        return s3_url
    except Exception as e:
        print(f"S3 upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload to S3: {e}")
 
# Initialize FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle function for FastAPI.
    Runs before the application starts and after it stops.
    """
    print("Starting up the API...")
 
    # Start background processing in a separate thread
    processor_thread = Thread(target=background_processor, daemon=True)
    processor_thread.start()
 
    print("Startup complete! Background processor running...")
 
    # Yield control back to FastAPI app
    yield
 
    print("Shutting down API...")
 
 
# Initialize FastAPI app with the lifespan handler
app = FastAPI(lifespan=lifespan)
@app.get("/")
def read_root():
    return {"message": "Welcomeeeee to my API"}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
server_address = "69.48.159.12:22569"
client_id = str(uuid.uuid4())
 
 
# Helper functions for ComfyUI interaction
def queue_prompt(prompt, client_id, server_address):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    url = f"http://{server_address}/prompt"
 
    print(f"DEBUG: Sending request to {url}")
    print(f"DEBUG: Request payload: {p}")
 
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
 
    try:
        response = urllib.request.urlopen(req)
        response_data = json.loads(response.read())
        print(f"DEBUG: Response received: {response_data}")
        return response_data
    except urllib.error.HTTPError as e:
        print(f"ERROR: HTTPError {e.code} - {e.reason}")
        print(f"ERROR: Response content: {e.read().decode()}")
        raise
    except urllib.error.URLError as e:
        print(f"ERROR: URLError - {e.reason}")
        raise
 
 
 
def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"http://{server_address}/view?{url_values}") as response:
        return response.read()
 
def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{server_address}/history/{prompt_id}") as response:
        return json.loads(response.read())
 
def get_video(ws, workflow, unique_number, username, email):
    print("get_video section")
    prompt_id = queue_prompt(workflow, client_id=client_id, server_address=server_address)['prompt_id']
    print("prompt id is", prompt_id)
    output_gifs = {}
 
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break
 
    history = get_history(prompt_id)[prompt_id]
    for node_id, node_output in history['outputs'].items():
        print("node outputs are", node_output)
 
        # Update Supabase status column to 2 for the unique_number
        supabase.table("video_queue").update({"status": 2}).eq("unique_number", unique_number).execute()
        print(f"Updated status to 2 for unique number {unique_number} in Supabase.")
 
        # Retrieve the latest file link from S3
        response = s3.list_objects_v2(Bucket=s3_bucket_name, Prefix=f"videos/{unique_number}/")
        if 'Contents' in response:
            latest_file = max(response['Contents'], key=lambda x: x['LastModified'])['Key']
            video_link = f"https://{s3_bucket_name}.s3.amazonaws.com/{latest_file}"
            print("Latest video link:", video_link)
 
            # Send email with the video link
            send_email(email, username, video_link)
        else:
            print("No video found for the given unique number.")
 
    return output_gifs
 
 
import time
 
def process_video_task(unique_number):
    print(f"Starting processing: {unique_number}")
 
    try:
        # Update status to "processing" (1) and store the start time
        start_time = time.time()
        print(f"Updating status to 'processing' for unique number: {unique_number}")
        supabase.table("video_queue").update({"status": 1}).eq("unique_number", unique_number).execute()
 
        # Retrieve workflow JSON & user details from Supabase
        print(f"Retrieving workflow JSON and user details for unique number: {unique_number}")
        response = (
            supabase.table("video_queue")
            .select("username, email, workflow_json")
            .eq("unique_number", unique_number)
            .execute()
        )
 
        data = response.data
        if not data or len(data) == 0:
            raise Exception(f"No workflow found for unique number {unique_number}")
 
        username = data[0]["username"]
        email = data[0]["email"]
        workflow = json.loads(data[0]["workflow_json"])  # Parse JSON string to dict
        print(f"Retrieved workflow for user: {username}, email: {email}")
 
 
        # ws = websocket.WebSocket()
        try:
            ws = create_connection(f"ws://{server_address}/ws?clientId={client_id}")
            print("WebSocket connected successfully")
        except Exception as e:
            print(f"WebSocket connection failed: {e}")
            return  # Prevent further execution
        gifs = get_video(ws, workflow,unique_number,username,email)
        ws.close()
 
        # # Check time elapsed while processing
        # while True:
        #     print("Processing workflow with ComfyUI")
        #     gifs = get_gifs(ws, workflow)
 
        #     elapsed_time = time.time() - start_time
        #     if elapsed_time > 900:  # 15 minutes = 900 seconds
        #         print(f"Processing time exceeded 15 minutes. Marking {unique_number} as failed.")
        #         supabase.table("video_queue").update({"status": 3}).eq("unique_number", unique_number).execute()
        #         ws.close()
        #         return  # Exit the function so the background processor can pick the next job
 
        #     if gifs:
        #         print("Processing successful, GIFs generated")
        #         break  # Exit loop when processing is successful
 
        ws.close()
 
        # Get the first S3 URL as the final path (modify as needed)
        final_path = next(iter(gifs.values()))[0]["s3Url"] if gifs else ""
        print(f"Final path for processed video: {final_path}")
 
        # Update database with results (status = 2 for processed)
        print(f"Updating database with results for unique number: {unique_number}")
        update_response = (
            supabase.table("video_queue")
            .update({
                "is_processed": True,
                "final_path": final_path,
                "status": 2  # 2 = processed
            })
            .eq("unique_number", unique_number)
            .execute()
        )
 
        if update_response.get("error"):
            raise Exception(f"Error updating Supabase: {update_response['error']}")
 
        print(f"Successfully processed unique number {unique_number}")
 
        # Send email to user
        # if final_path:
        #     send_email(email, username, final_path)
 
    except Exception as e:
        print(f"Error processing unique_number {unique_number}: {str(e)}")
 
        # Update status to "failed" (3) in case of an error
        print(f"Marking unique number {unique_number} as failed due to error")
        supabase.table("video_queue").update({"status": 3}).eq("unique_number", unique_number).execute()
        return
 
 
def background_processor():
    while True:
        try:
            print("Checking for stuck jobs...")
 
            # Step 1: Check for stuck jobs (status = 1)
            stuck_jobs_response = (
                supabase.table("video_queue")
                .select("unique_number, created_at")
                .eq("status", 1)  # Status 1 = Processing
                .execute()
            )
 
            stuck_jobs = stuck_jobs_response.data
 
            if stuck_jobs:
                print(f"Found {len(stuck_jobs)} stuck jobs")
                current_time = datetime.now(timezone.utc)
 
                for job in stuck_jobs:
                    unique_number = job["unique_number"]
                    created_at_str = job.get("created_at")
 
                    if created_at_str:
                        created_at = parser.isoparse(created_at_str)
                        elapsed_time = (current_time - created_at).total_seconds()
 
 
                        if elapsed_time > 900:  # More than 15 minutes
                            print(f"Job {unique_number} stuck for over 15 minutes. Marking as failed.")
                            supabase.table("video_queue").update({"status": 3}).eq("unique_number", unique_number).execute()
 
            else:
                print("No stuck jobs found. Checking for unprocessed videos...")
 
                # Step 2: Fetch the oldest unprocessed video (status = 0)
                response = (
                    supabase.table("video_queue")
                    .select("unique_number")
                    .eq("status", 0)  # Status 0 = Not Processed
                    .order("created_at", desc=False)  # Fetch the oldest entry first
                    .limit(1)
                    .execute()
                )
 
                data = response.data
 
                if data:
                    unique_number = data[0]["unique_number"]
                    print(f"Processing new video with unique number: {unique_number}")
                    process_video_task(unique_number)
                else:
                    print("No unprocessed videos found.")
 
            time.sleep(30)  # Wait before checking again
 
        except Exception as e:
            print(f"Error in background processor: {str(e)}")
            time.sleep(30)  # Wait before retrying
 
 
# Request schema
class WorkflowRequest(BaseModel):
    username: str
    email: str
    workflow: dict
 
 
# API endpoints
# @app.on_event("startup")
# async def startup_event():
#     init_db()
#     # Start background processor in a separate thread
#     processor_thread = Thread(target=background_processor, daemon=True)
#     processor_thread.start()
import random
 
 
@app.post("/process-video")
def process_video(request: WorkflowRequest):
    try:
        workflow = request.workflow
        username = request.username
        email = request.email
        unique_number = f"{random.randint(10000, 99999)}"  # Generate a unique number
 
        # Save to Supabase
        data = {
            "unique_number": unique_number,
            "username": username,
            "email": email,
            "workflow_json": json.dumps(workflow),
            "is_processed": False,
            "final_path": "",
            "status": 0,  # 0 = not processed
        }
 
        response = supabase.table("video_queue").insert(data).execute()
 
        if response.data is None or len(response.data) == 0:
            raise HTTPException(status_code=500, detail=f"Error saving to Supabase: {response}")
 
 
        print(f"Saved workflow for {username} ({email}) with unique number {unique_number}")
        return {"unique_number": unique_number}
 
    except Exception as e:
        print(f"Error saving workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_api():
    return {"message": "Test API is working!"}


@app.get("/check-status/{unique_number}")
def check_status(unique_number: str):
    print("checkprocess called")
    try:
        response = (
            supabase.table("video_queue")
            .select("username, email, is_processed, final_path, status")
            .eq("unique_number", unique_number)
            .execute()
        )
 
        data = response.data
 
        if not data or len(data) == 0:
            raise HTTPException(status_code=404, detail="Invalid ID: Video not found.")
 
        username = data[0]["username"]
        email = data[0]["email"]
        is_processed = data[0]["is_processed"]
        final_path = data[0]["final_path"]
        status = data[0]["status"]  # Returns integer status
 
        return {
            "username": username,
            "email": email,
            "is_processed": bool(is_processed),
            "final_path": final_path,
            "status": status,  # Status is now an integer
            "message": "Video is ready for download and streaming." if status == 2 else "Video is still processing.",
        }
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
 
 
 
def send_email(to_email, username, video_link):
    """Sends an email with the video link."""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = to_email
        msg["Subject"] = "Your Video is Ready!"
 
        body = f"""
        Hi {username},
 
        Your video has been processed successfully. You can download it using the link below:
 
        {video_link}
 
        Best,
        Your Team
        """
        msg.attach(MIMEText(body, "plain"))
 
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
        server.quit()
 
        print(f"Email sent to {to_email}")
 
    except Exception as e:
        print(f"Failed to send email: {e}")