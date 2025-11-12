# YearWave
## Billboard Hot 100 to Spotify Playlist

A Python tool that turns Billboard Hot 100 charts into Spotify playlists.

This Python script creates a **Spotify playlist** of Billboard Hot 100 songs for a specific chart week.  
It uses a Billboard chart dataset (CSV) and the **Spotipy** library to connect to your Spotify account.

---

## Features
- Loads Billboard chart data from a CSV file  (current is until 2025-10-25)
- Lets you choose a chart week (e.g., `2022-01-01`)  
- Searches each track on Spotify  
- Automatically creates a **private playlist** with the matching songs

---

## Requirements
- Python 3.8 or newer  
- Spotify Developer Account  
- A Spotify App created at [https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)  
- Environment variables stored in a `.env` file  

---

## Installation

1. **Clone or download** this repository.  
2. **Install dependencies:**
   ```bash
   pip install spotipy python-dotenv pandas
   ```
3. **Create a `.env` file** in the project directory with:
   ```bash
   SPOTIPY_CLIENT_ID=your_client_id
   SPOTIPY_CLIENT_SECRET=your_client_secret
   SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
   ```

4. **Add the redirect URI** (`http://127.0.0.1:8888/callback`) in your Spotify app settings.

---

## Usage

1. Place your Billboard CSV file (e.g., `hot-100-current.csv`) in the same directory.  
2. Run the script:
   ```bash
   python main.py
   ```
3. Enter a date like `2022-01-01` when prompted.  
4. The script creates a private playlist named:
   ```
   Billboard Hot 100 - 2022-01-01
   ```
   in your Spotify account.

---

## Notes
- The CSV file should follow this structure:
  ```
  chart_week,current_week,title,performer,last_week,peak_pos,wks_on_chart
  2022-01-01,1,All I Want For Christmas Is You,Mariah Carey,1,1,50
  ```
- Tracks that can’t be matched exactly on Spotify will be skipped.

---

## Example Output
```
What year (or week) would you like to travel to?
(YYYY-MM-DD or YYYY): 2001
Added 100 songs to the playlist for 2001.
```

---

Data source: [rwd-billboard-data](https://github.com/utdata/rwd-billboard-data) (CC BY license)
