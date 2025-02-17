import json
from websocket._core import create_connection
from main import get_video, queue_prompt, get_history, send_email, supabase, s3

def test_get_video():
    # Mock WebSocket connection
    ws = create_connection("ws://213.181.111.2:31096/ws?clientId=test_client_id")

    # Test data
    workflow = {
        "steps": [
            {"action": "start", "parameters": {}},
            {"action": "process", "parameters": {"effect": "grayscale"}},
            {"action": "end", "parameters": {}}
        ]
    }
    unique_number = "test_unique_number"
    username = "test_username"
    email = "test_email@example.com"

    # Call the get_video function
    output_gifs = get_video(ws, workflow, unique_number, username, email)

    # Print the result
    print("Output GIFs:", output_gifs)

    # Close the WebSocket connection
    ws.close()

if __name__ == "__main__":
    test_get_video()