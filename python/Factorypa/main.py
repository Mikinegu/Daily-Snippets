import pygame
import time
import os
import schedule 
import threading
from datetime import datetime

#get playlist for appropriate day
def get_plalist_for_today():
    today = datetime.now().strftime("%A").lower()
    playlist_folder = os.path.join("python\Factorypa\Playlists", today)
    if not os.path.exists(playlist_folder):
        print(f"❌ Playlist for {today} not found.")
        print({playlist_folder})
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
schedule.every().day.at("12:39").do(start_music)
schedule.every().day.at("12:40").do(pause_music)
schedule.every().day.at("12:41").do(resume_music)
schedule.every().day.at("12:42").do(stop_music)

while True:
    schedule.run_pending()
    time.sleep(1)  # Sleep to prevent busy-waiting