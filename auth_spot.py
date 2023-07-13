import os
import spotipy, time
from flask import session, url_for, flash, redirect
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
# load the .env file and store the Spotify API credentials.
load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_SECRET')

# return an api object based on current logged in user, that can be used to make api calls
def get_spotify_user():
    token_info = session['spot_token_info']
    return  spotipy.Spotify(auth=token_info['access_token'])

# to be called before every function that requires spotify authorization
# check if user is logged into spotify and/or their credentials are valid.
def check_spot():
    token_info = session.get('spot_token_info', None)
    if token_info:
        if token_info['expires_at'] - int(time.time()) < 60:
            sp_oauth =  create_spotify_oauth()
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    else:
        flash('Spotify account authorization needed!')
        return redirect('/')
    
    session['spot_token_info'] = token_info
     
# return an oauth object with the required scopes and api credentials
def create_spotify_oauth():
    return SpotifyOAuth(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri=url_for('redirectSpotify', _external=True),
                scope='playlist-read-private playlist-modify-private playlist-modify-public user-library-read')