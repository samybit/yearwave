import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

#---------------------------------------------------
# Tester
#---------------------------------------------------
# # Authintication with Spotify (optional test)
# sp = spotipy.Spotify(
#     auth_manager=SpotifyOAuth(
#         scope="user-library-read"
#     )
# )
# # To test authentication and print user's saved tracks
# results = sp.current_user_saved_tracks(limit=10)
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(f"{idx+1}. {track['name']} — {track['artists'][0]['name']}")

#---------------------------------------------------
# Read local chart data
# Billboard Hot 100 CSV from rwd-billboard-data GitHub repo
# https://github.com/utdata/rwd-billboard-data
#---------------------------------------------------
df = pd.read_csv("hot-100-current.csv")

#---------------------------------------------------
# User input for year
#---------------------------------------------------
week_input = input("What year (or week) would you like to travel to?\n(YYYY-MM-DD or YYYY): ").strip() or ""

#---------------------------------------------------
# Extract and Filter chart data
#---------------------------------------------------
df["chart_week"] = pd.to_datetime(df["chart_week"])

try:
    if len(week_input) == 4:  # If input is a year-only
        filtered = df[df["chart_week"].dt.year == int(week_input)]
    else:
        filtered = df[df["chart_week"] == pd.to_datetime(week_input)]
except ValueError:
    print("Invalid date format. Use YYYY or YYYY-MM-DD.")
    exit()

filtered = filtered[["title", "performer"]].dropna().head(100)

if filtered.empty:
    print(f"No songs found for {week_input}. Check CSV content.")
    exit()

#---------------------------------------------------
# Spotify API credentials
#---------------------------------------------------
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

#---------------------------------------------------
# Spotify API authentication and user ID
#---------------------------------------------------
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt",
    )
)
user_id = sp.current_user()["id"]

#---------------------------------------------------
# Create playlist
#---------------------------------------------------
playlist = sp.user_playlist_create(user_id, f"Billboard Hot 100 - {week_input}", public=False)
playlist_id = playlist["id"]

#---------------------------------------------------
## Search and collect URIs
#---------------------------------------------------
track_uris = []
year = week_input[:4] # Get the year-only from the input

for _, row in filtered.iterrows():
    song = row['title']
    artist = row['performer']
    query = f"track:{song} artist:{artist} year:{year}"

    result = sp.search(q=query, type="track", limit=1)
    tracks = result["tracks"]["items"]
    
    try:
        uri = tracks[0]["uri"]
        track_uris.append(uri)
    except IndexError:
        print(f"{song} by {artist} doesn't exist on Spotify. Skipped.")

#---------------------------------------------------
# Add to playlist
#---------------------------------------------------
if track_uris:
    sp.playlist_add_items(playlist_id, track_uris)

#---------------------------------------------------
# Terminal output for user
#---------------------------------------------------
print("Logged in as:", user_id)
print(f"Found {len(track_uris)} tracks out of {len(filtered)}.")
print(f"Added {len(track_uris)} songs to the playlist for {week_input}.")
