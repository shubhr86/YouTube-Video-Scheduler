import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Updated SCOPES to include 'youtube.readonly' to fetch channel details
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]

def authenticate():
    creds = None

    print("Checking for existing token...")

    # Load saved credentials if they exist
    if os.path.exists("token.pickle"):
        print("Found existing token.pickle, loading credentials...")
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If credentials are invalid, authenticate again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing token...")
            creds.refresh(Request())
        else:
            print("No valid credentials found. Starting authentication process...")
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
            creds = flow.run_local_server(port=0)  # Opens browser for login

        # Save credentials for future use
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
        print("Authentication successful! Token saved.")

    return creds

def get_channel_info(creds):
    """Fetches the default description and tags from the user's YouTube channel."""
    youtube = build("youtube", "v3", credentials=creds)

    try:
        request = youtube.channels().list(
            part="snippet",
            mine=True  # Fetches data for the authenticated user's channel
        )
        response = request.execute()

        if "items" in response and len(response["items"]) > 0:
            channel_info = response["items"][0]["snippet"]
            channel_description = channel_info.get("description", "No description found.")
          #  channel_tags = channel_info.get("tags", [])

            print("\n✅ Channel Description:")
            print(channel_description)
            print("\n✅ Channel Tags:")
          #  print(channel_tags if channel_tags else "No tags found.")

            return channel_description
        else:
            print("❌ No channel information found.")
            return None, None

    except Exception as e:
        print(f"⚠️ Error fetching channel info: {e}")
        return None, None

if __name__ == "__main__":
    creds = authenticate()
    get_channel_info(creds)
