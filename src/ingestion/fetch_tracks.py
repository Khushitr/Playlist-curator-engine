import os, json
from datetime import datetime
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import boto3

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-top-read"
))

s3 = boto3.client("s3")
BUCKET_NAME = "your-bucket-name"  # Replace this with your S3 bucket name

def fetch_and_store():
    results = sp.current_user_top_tracks(limit=50, time_range='short_term')
    combined_data = []
    for item in results['items']:
        features = sp.audio_features([item['id']])[0]
        track_data = {
            "id": item["id"],
            "name": item["name"],
            "artist": item["artists"][0]["name"],
            "album": item["album"]["name"],
            "popularity": item["popularity"],
            "duration_ms": item["duration_ms"],
            "features": features
        }
        combined_data.append(track_data)

    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"spotify_tracks_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(combined_data, f, indent=4)
    print(f"[✓] Data saved to {filename}")

