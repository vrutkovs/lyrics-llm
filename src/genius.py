from re import L
import streamlit as st

import os
from dotenv import load_dotenv
import lyricsgenius

load_dotenv()
token = os.getenv("GENIUS_ACCESS_TOKEN")
if token is None:
    raise ValueError("GENIUS_ACCESS_TOKEN environment variable is not set")
genius = lyricsgenius.API(token)
publicgenius = lyricsgenius.Genius(token)

MAX_SONGS = os.getenv("MAX_SONGS") or 10


def get_artist_songs(artist_name):
    with st.spinner(text=f"Loading most popular {MAX_SONGS} songs by artist {artist_name}"):
        request = genius.search_songs(search_term=artist_name, per_page=10)
        # Grab first hit
        artist_id = request["hits"][0]["result"]["primary_artist"]["id"]
        request = genius.artist_songs(artist_id=artist_id, per_page=MAX_SONGS, sort="popularity")
        return [x["title"] for x in request.get('songs', [])]


def write_lyrics(song_names, artist, tmpdirname):
    for song_name in song_names:
        with st.spinner(text=f"Fetching lyrics for {artist} - {song_name}", show_time=True):
            song = publicgenius.search_song(title=song_name, artist=artist)
            if song is None:
                continue
            filename = f"{tmpdirname}/{song.id}.txt"
            song.save_lyrics(filename, extension="txt", overwrite=True, sanitize=False)
