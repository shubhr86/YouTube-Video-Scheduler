import os
import pickle
import datetime
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Load credentials
def get_authenticated_service():
    with open("token.pickle", "rb") as token:
        creds = pickle.load(token)
    return build("youtube", "v3", credentials=creds)

# Load default description from a file
def load_default_description():
    """Reads the default description from a text file."""
    if os.path.exists("default_description.txt"):
        with open("default_description.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

# Folder paths
VIDEO_FOLDER = "E:\\Youtube\\shorts" # here the videos directory change according to yours
LOG_FILE = "uploaded_videos.txt"  # Track uploaded videos

# Playlist links or Other link you want to share , can change according to yours
PLAYLIST_LINKS = """
https://www.youtube.com/watch?v=TidrSMPNKlA&list=PLZi1rrttirMnEmncSGfQ7kmk-3J20IPLj
https://youtu.be/fnoEJ_nDRco
https://youtube.com/shorts/Ab_Vbdg9w4c?feature=share
"""

# Scheduling parameters

IST_TO_UTC_OFFSET = datetime.timedelta(hours=-5, minutes=-30)
START_DATE = datetime.datetime(2025, 3, 29, 18, 0) - IST_TO_UTC_OFFSET #can change the date and time from here
START_DATE = START_DATE.replace(tzinfo=datetime.timezone.utc)
TIME_GAP_DAYS = 2 # gap between the videos to schedule

# Load default description
DEFAULT_DESCRIPTION = load_default_description()

def get_next_schedule_time():
    now = datetime.datetime.now(datetime.timezone.utc)
    schedule_time = START_DATE
    while schedule_time < now:
        schedule_time += datetime.timedelta(days=TIME_GAP_DAYS)
    return schedule_time

def load_uploaded_videos():
    """Load uploaded video names from the log file."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_uploaded_video(video_name):
    """Save uploaded video name to the log file."""
    with open(LOG_FILE, "a") as f:
        f.write(video_name + "\n")

def get_video_size(file_path):
    """Get file size in MB."""
    return os.path.getsize(file_path) / (1024 * 1024)

def get_sleep_time(video_size):
    """Determine sleep time based on file size."""
    if video_size < 100:
        return 120  # 2 minutes
    elif video_size < 500:
        return 300  # 5 minutes
    elif video_size < 1000:
        return 600  # 10 minutes
    elif video_size < 2000:
        return 900  # 15 minutes
    else:
        return 1200  # 20 minutes

def upload_video(file_path, title, schedule_time):
    """Uploads a video to YouTube."""
    youtube = get_authenticated_service()
    
    # Append the default description
    description = f"{PLAYLIST_LINKS}\n\n{DEFAULT_DESCRIPTION}"

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": "22",
            "tags": ["Shorts", "Viral", "Trending"]
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": schedule_time.isoformat()
        }
    }
    
    try:
        print(f"Uploading: {file_path} at {schedule_time} UTC")
        media = MediaFileUpload(file_path, resumable=True)
        response = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media
        ).execute()
        print(f"Uploaded successfully: {response['id']}")
        save_uploaded_video(os.path.basename(file_path))
        
        # Sleep based on file size
        sleep_time = get_sleep_time(get_video_size(file_path))
        print(f"Sleeping for {sleep_time // 60} minutes before next upload...")
        time.sleep(sleep_time)
    except HttpError as e:
        print(f"An error occurred: {e}")

def main():
    if not os.path.exists(VIDEO_FOLDER):
        print("Video folder does not exist!")
        return
    
    video_files = [f for f in os.listdir(VIDEO_FOLDER) if f.lower().endswith((".mp4", ".mkv", ".avi", ".mov"))] # check to upload only videos
    if not video_files:
        print("No videos available for scheduling.")
        return
    
    uploaded_videos = load_uploaded_videos()
    next_schedule_time = get_next_schedule_time()
    
    for video in sorted(video_files):
        if video in uploaded_videos:
            print(f"Skipping already uploaded video: {video}")
            continue
        
        video_path = os.path.join(VIDEO_FOLDER, video)
        title = os.path.splitext(video)[0]
        upload_video(video_path, title, next_schedule_time)
        next_schedule_time += datetime.timedelta(days=TIME_GAP_DAYS)

if __name__ == "__main__":
    main()
