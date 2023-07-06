import os
import spotipy, time
from flask import session, url_for, flash, redirect
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_SECRET')


def get_spotify_user():
    token_info = session['spot_token_info']
    return  spotipy.Spotify(auth=token_info['access_token'])


def check_spot():
    token_info = session.get('spot_token_info', None)
    if token_info:
        if token_info['expires_at'] - int(time.time()) < 60:
            sp_oauth =  create_spotify_oauth()
            token_info = sp_oauth.refresh_access_token(token_info['refresh-token'])
    else:
        flash('Spotify account authorization needed!')
        return redirect('/')
    
    session['spot_token_info'] = token_info
     

def create_spotify_oauth():
    return SpotifyOAuth(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri=url_for('redirectSpotify', _external=True),
                scope='playlist-read-private playlist-modify-private playlist-modify-public user-library-read')