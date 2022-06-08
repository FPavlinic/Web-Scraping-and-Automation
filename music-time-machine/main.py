# used libraries
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv


# look for .env file
load_dotenv("C:/Users/pavli/PycharmProjects/PORTFOLIO/.env.txt")

# url to the hottest 100 songs by specific date
URL = "https://www.billboard.com/charts/hot-100"

# authenticate Python project with Spotify
CLIENT_ID = os.getenv("API_SPOTIFY_ID")
CLIENT_SECRET = os.getenv("API_SPOTIFY_SECRET")

# where to be send to by authorization server to get access token
REDIRECT_URI = "http://example.com"

# input the date for which you want list of hot 100 songs
wanted_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

# go to url with list of hot 100 songs for specified date
response = requests.get(url=f"{URL}/{wanted_date}")
# get HTML from url
soup = BeautifulSoup(response.text, "html.parser")
# get list of songs from HTML
song_list = [song.getText().strip() for song in soup.select(selector="main li h3")]

# authenticate with Spotify
auth_manager = SpotifyOAuth(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            redirect_uri=REDIRECT_URI,
                            scope="playlist-modify-private",
                            cache_path="token.txt")
spotify = spotipy.Spotify(auth_manager=auth_manager)

# get access token
auth_manager.get_authorize_url()
auth_manager.get_cached_token()

# get your user id
user_id = spotify.current_user()["id"]

# empty list for all uris to songs on Spotify
songs_uri_list = []

# go through the list of hot 100 songs
for song in song_list:
    # try to find uri to song by name and year of release
    try:
        song_uri = spotify.search(q=f"track: {song} year: {wanted_date[:4]}", type="track", limit=1)
        songs_uri_list.append(song_uri['tracks']['items'][0]['uri'])
    # print message if song is not found
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


# create playlist on Spotify
playlist_info = spotify.user_playlist_create(user=user_id,
                             name=f"{wanted_date} Billboard 100",
                             public=False,
                             collaborative=False,
                             description=f"The Hot 100 songs on Billboard charts on {wanted_date}.")
# get created playlist id
playlist_id = playlist_info["id"]

# add songs with found uris to Spotify playlist by playlist id
spotify.playlist_add_items(playlist_id=playlist_id, items=songs_uri_list)

