import sqlite3
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import websocket
import uuid
import json
import urllib.request
import random
import boto3
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
from contextlib import asynccontextmanager
from threading import Thread
import ssl

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('video_processing.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS video_queue (
            unique_number TEXT PRIMARY KEY,
            workflow_json TEXT NOT NULL,
            is_processed INTEGER DEFAULT 0,
            final_path TEXT DEFAULT ''
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the S3 client
s3 = boto3.client('s3', 
                  aws_access_key_id=AWS_ACCESS_KEY_ID, 
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
                  region_name=AWS_REGION)

s3_bucket_name = "cft-employee"

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
    # Code to run at startup (like DB initialization)
    init_db()  # Your database initialization function
    # Start background processing in a separate thread
    processor_thread = Thread(target=background_processor, daemon=True)
    processor_thread.start()
    print("Startup complete!")
    
    # Yield control back to the application
    yield
    
    # Code to run at shutdown (if needed)
    print("Shutdown complete!")

# Initialize FastAPI app with the lifespan handler
app = FastAPI(lifespan=lifespan)

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.set_ciphers('TLSv1.2')
context.load_cert_chain(certfile="server.crt", keyfile="server.key")


@app.get("/")
def read_root():
    return {"message": "Welcome to my API"}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ComfyUI server configuration
server_address = "209.170.80.132:14036"
client_id = str(uuid.uuid4())

# Helper functions for ComfyUI interaction
def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"https://{server_address}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"https://{server_address}/view?{url_values}") as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen(f"https://{server_address}/history/{prompt_id}") as response:
        return json.loads(response.read())

def get_gifs(ws, workflow):
    prompt_id = queue_prompt(workflow)['prompt_id']
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
        if 'gifs' in node_output:
            gifs_output = []
            for gif in node_output['gifs']:
                gif_data = get_image(gif['filename'], gif['subfolder'], gif['type'])
                s3_file_name = f"gifs/{uuid.uuid4()}/{gif['filename']}"
                s3_url = upload_to_s3(gif_data, s3_file_name)
                gifs_output.append({
                    'filename': gif['filename'],
                    'subfolder': gif['subfolder'],
                    'type': gif['type'],
                    'format': gif['format'],
                    'frame_rate': gif['frame_rate'],
                    's3Url': s3_url
                })
            output_gifs[node_id] = gifs_output

    return output_gifs

def process_video_task(unique_number):
    print(f"Starting processing: {unique_number}")
    try:
        # Load workflow JSON from the database
        conn = sqlite3.connect('video_processing.db')
        c = conn.cursor()

        c.execute('SELECT workflow_json FROM video_queue WHERE unique_number = ?', (unique_number,))
        result = c.fetchone()
        conn.close()

        if not result:
            raise Exception(f"No workflow found for unique number {unique_number}")

        workflow = json.loads(result[0])  # Parse the JSON string to a Python dictionary

        # Process with ComfyUI
        ws = websocket.WebSocket()
        ws.connect(f"wss://{server_address}/ws?clientId={client_id}")
        gifs = get_gifs(ws, workflow)
        ws.close()

        # Update database with results
        conn = sqlite3.connect('video_processing.db')
        c = conn.cursor()
        
        # Get the first S3 URL as the final path (modify as needed)
        final_path = next(iter(gifs.values()))[0]['s3Url'] if gifs else ''
        
        c.execute('''
            UPDATE video_queue 
            SET is_processed = 1, final_path = ? 
            WHERE unique_number = ?
        ''', (final_path, unique_number))
        
        conn.commit()
        conn.close()
        
        print(f"Successfully processed unique number {unique_number}")
        
    except Exception as e:
        print(f"Error processing unique_number {unique_number}: {str(e)}")
        raise

def background_processor():
    while True:
        try:
            conn = sqlite3.connect('video_processing.db')
            c = conn.cursor()
            
            # Get unprocessed video
            c.execute('SELECT unique_number FROM video_queue WHERE is_processed = 0 LIMIT 1')
            result = c.fetchone()
            conn.close()
            
            if result:
                unique_number = result[0]  # Extract unique_number from the result tuple
                process_video_task(unique_number)
            
            time.sleep(30)  # Wait before checking again
            
        except Exception as e:
            print(f"Error in background processor: {str(e)}")
            time.sleep(30)  # Wait before retrying


# Request schema
class WorkflowRequest(BaseModel):
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
        print(workflow)
        unique_number = f"{random.randint(10000, 99999)}"  # Generate a unique number

        # Save to database
        conn = sqlite3.connect("video_processing.db")
        c = conn.cursor()

        # Ensure the table exists
        c.execute('''
            CREATE TABLE IF NOT EXISTS video_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unique_number TEXT,
                workflow_json TEXT,
                is_processed INTEGER,
                final_path TEXT
            )
        ''')

        # Insert the workflow JSON into the database
        c.execute(
            '''
            INSERT INTO video_queue (unique_number, workflow_json, is_processed, final_path)
            VALUES (?, ?, 0, '')
            ''',
            (unique_number, json.dumps(workflow)),
        )
        conn.commit()
        conn.close()

        print(f"Saved workflow to queue with unique number {unique_number}")

        return {"unique_number": unique_number}
    except Exception as e:
        print(f"Error saving workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/check-status/{unique_number}")
def check_status(unique_number: str):
    try:
        conn = sqlite3.connect('video_processing.db')
        c = conn.cursor()
        c.execute('SELECT is_processed, final_path FROM video_queue WHERE unique_number = ?', (unique_number,))
        result = c.fetchone()
        conn.close()

        if result is None:
            raise HTTPException(status_code=404, detail="Invalid ID: Video not found.")

        is_processed, final_path = result

        # Handle empty or None final_path
        if not final_path or final_path.strip() == "":
            print("Video is still processing or not available yet.")
            return {
                "is_processed": bool(is_processed),
                "final_path": None,
                "message": "Video is still processing or not available yet."
            }

        return {
            "is_processed": bool(is_processed),
            "final_path": final_path,
            "message": "Video is ready for download and streaming."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
