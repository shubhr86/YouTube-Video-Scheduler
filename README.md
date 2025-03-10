# YouTube Video Scheduler

## 📌 Project Overview

This project automates the process of uploading and scheduling YouTube Shorts videos using the **YouTube Data API v3**. It allows users to:

✅ Authenticate with YouTube using OAuth 2.0 ✅ Upload videos from a specified folder ✅ Schedule video uploads every alternate day at 6 PM IST ✅ Prevent duplicate uploads ✅ Automatically append a default description and playlist links

## 🚀 Features

- **Automated Uploads**: Uploads videos from a designated folder.
- **Scheduled Publishing**: Automatically schedules videos at 6 PM IST every two days.
- **Duplicate Prevention**: Keeps track of uploaded videos to avoid re-uploading.
- **Custom Description & Tags**: Fetches the default description from the channel and appends playlist links.
- **File Size-Based Sleep Time**: Adjusts sleep time between uploads based on file size.
- **Error Handling & Logging**: Handles authentication errors, API rate limits, and logs uploaded videos.

---

## 📜 YouTube API Setup

### Step 1: Get YouTube API Credentials

### You must use the same email to create the Google Console account that is linked to YouTube. 

1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Create a new project.
3. Enable the **YouTube Data API v3**.
4. Go to **Credentials** and create a new **OAuth 2.0 Client ID**:
   - Select **Desktop App** as the application type.
   - Download the `client_secrets.json` file and place it in the project directory. In case the downloaded file name is something else then please change it to 'client_secrets'

---

## 🛠️ Installation & Setup

### Step 2: Install Required Dependencies

Make sure you have **Python 3.7+** installed. Then, install the required dependencies:

```sh
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 3: Authenticate with YouTube

Before running the script, authenticate your Google account:

```sh
python auth.py
```

- This will open a browser for authentication.
- After login, it will generate a `token.pickle` file to store authentication details.

---

## 📂 Folder Structure

```
📁 YouTube Video Scheduler
│── auth.py                 # Handles YouTube OAuth authentication
│── YT.py                   # Main script to upload and schedule videos
│── client_secrets.json      # YouTube API credentials (DO NOT SHARE!)
│── token.pickle             # Stores OAuth tokens after authentication
│── uploaded_videos.txt      # Logs uploaded videos to prevent duplicates
│── default_description.txt  # Contains the default description for videos
│── 📁 Youtube
│    ├── 📁 shorts           # Folder containing videos to be uploaded, you can change it directly in the YT.py file
```

---

## 🎬 How to Use

### Step 4: Add Videos to Upload

Place your **short videos** in the `Youtube/shorts/` folder.

### Step 5: Run the Scheduler

Run the script to start uploading videos:

```sh
python YT.py
```

The script will:

- Pick the first available video.
- Upload and schedule it at **6 PM IST (every 2 days)**.
- Save the uploaded video name in `uploaded_videos.txt`.
- Sleep for a calculated time before processing the next video.

---

## 🖥️ Technologies Used

- **Python**: Core scripting language.
- **YouTube Data API v3**: Handles video uploads and scheduling.
- **OAuth 2.0**: For secure authentication.
- **Google API Client**: Interacts with YouTube services.
- **Pickle**: Stores authentication tokens.

---

## 🔥 Additional Notes

- Ensure your **Google account is verified** to avoid API quota limits.
- You can customize the default description by editing `default_description.txt`.
- Modify `PLAYLIST_LINKS` inside `YT.py` to include your custom links.
- To reset authentication, **delete** `token.pickle` and re-run `auth.py`.

---

## ❓ Troubleshooting

### 1. `invalid_grant` Error

- Delete `token.pickle` and run `auth.py` again.

### 2. No Videos Uploaded

- Ensure videos are placed in `Youtube/shorts/`.
- Check if videos were already uploaded (see `uploaded_videos.txt`).

### 3. API Quota Exceeded

- Wait 24 hours or upgrade your Google Cloud project quota.

---

## 📜 License

This project is licensed under the MIT License.

💡 **Contributions & feedback are welcome!** If you find any issues or want to improve the script, feel free to submit a pull request. 😊

