import streamlit as st

import os
from dotenv import load_dotenv
import lyricsgenius

load_dotenv()
token = os.getenv("GENIUS_ACCESS_TOKEN")
if token is None:
    raise ValueError("GENIUS_ACCESS_TOKEN environment variable is not set")
genius = lyricsgenius.Genius(token, user_agent="Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0")

MAX_SONGS = os.getenv("MAX_SONGS") or 10


def get_artist_songs(artist_name):
    artist = None
    with st.spinner(text=f"Looking up artist {artist_name} on Genius"):
        artist = genius.search_artist(artist_name, max_songs=0, get_full_info=False)
        if artist is None:
            raise ValueError(f"Artist {artist_name} not found")
    with st.spinner(text=f"Loading most popular {MAX_SONGS} songs by artist {artist.name}"):
        request = genius.artist_songs(artist_id=artist.id, per_page=MAX_SONGS, sort="popularity")
        return [x["title"] for x in request.get('songs', [])]


def write_lyrics(song_names, artist, tmpdirname):
    for song_name in song_names:
        song = genius.search_song(title=song_name, artist=artist)
        if song is None:
            continue
        filename = f"{tmpdirname}/{song.id}.txt"
        song.save_lyrics(filename, extension="txt", overwrite=True, sanitize=False)
