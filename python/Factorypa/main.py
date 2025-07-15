import pygame
import time
import os
import schedule 
import threading
from datetime import datetime
import json

# Load configuration
with open ("python\Factorypa\config.json", "r") as f:
    config = json.load(f)

# black out days
def is_blackout_day():
    today = datetime.now()
    day_name = today.strftime("%A").lower()
    date_str = today.strftime("%Y-%m-%d")

    blackout_days = config.get("blackout_days", [])
    holidays = config.get("holidays", {})

    if day_name in blackout_days or date_str in holidays:
        print(f"❌ Today is a blackout day: {day_name} or {date_str}.")
        return True
    
    return False


#get to days schedule 
def get_todays_schedule():
    today = datetime.now().strftime("%A").lower()
    return config.get(today, {})

#get playlist for appropriate day
def get_plalist_for_today():
    today = datetime.now().strftime("%A").lower()
    playlist_folder = os.path.join("python\Factorypa\Playlists", today)
    if not os.path.exists(playlist_folder):
        print(f"❌ Playlist for {today} not found.")
        return []
    songs = [f for f in os.listdir(playlist_folder) if f.endswith(".mp3")]
    songs.sort()
    full_path = [os.path.join(playlist_folder, s) for s in songs]
    return full_path

#initialize pygame
pygame.mixer.init()

is_playing = False
is_paused = False
music_thread = None

def play_playlist():
    global is_playing , is_paused
    print("🎵Starting music playback...")
    
    songs = get_plalist_for_today() 
    if not songs:
        print("❌ No songs found for today.")
        return
    
    for song_path in songs:
        if not is_playing:
            break
        
        print(f"Playing: {song_path}")
        # Load and play music
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()

        # Wait for the music to finish playing
        while pygame.mixer.music.get_busy() or is_paused:
            if not is_playing:
                pygame.mixer.music.stop()
                break
            if is_paused:
                time.sleep(1)
                continue
            time.sleep(1)  
    print("🎵Music playback finished.")

def start_music():
    global is_playing, music_thread
    if not is_playing:
        is_playing = True
        print("✅ Music scheduled to start.")
        music_thread = threading.Thread(target=play_playlist)
        music_thread.start()

def pause_music():
    global is_paused
    if is_playing:
        is_paused = True
    print("⏸️ Pausing music playback...")
    pygame.mixer.music.pause()

def resume_music():
    global is_paused
    if is_playing and is_paused:
        is_paused = False
    print("▶️ Resuming music playback...")
    pygame.mixer.music.unpause()

def stop_music():
    global is_playing , is_paused 
    if is_playing:
        is_playing = False
        is_paused = False
    pygame.mixer.music.stop()
    print("⏹️ Stopping music playback...")

# Schedule music playback

if not is_blackout_day():
    today_schedule = get_todays_schedule()
    if today_schedule:
        schedule.every().day.at(today_schedule["clock_in"]).do(start_music)
        schedule.every().day.at(today_schedule["lunch_break"]).do(pause_music)
        schedule.every().day.at(today_schedule["lunch_resume"]).do(resume_music)
        schedule.every().day.at(today_schedule["clock_out"]).do(stop_music)
    else:
        print("❌ No schedule found for today.")
else:
    print("❌ Skipping music playback due to blackout day.")
while True:
    schedule.run_pending()
    time.sleep(1)  # Sleep to prevent busy-waiting