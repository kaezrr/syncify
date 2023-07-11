from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from flask import session, redirect, flash

# Write (your_website)/redirectyoutube in redirect_uri

def youtube_oauth():
    """
    Handles OAuth2 flow for YouTube API. If you don't know what a OAuth2 flow is, check out this link: https://frontegg.com/blog/oauth-flows
    """
    flow = InstalledAppFlow.from_client_secrets_file('apiinfo.json',
                                                    redirect_uri='http://127.0.0.1:5000/redirectyoutube',
                                                    scopes=['https://www.googleapis.com/auth/youtubepartner',
                                                        'https://www.googleapis.com/auth/youtube',
                                                        'https://www.googleapis.com/auth/youtube.force-ssl'])
    return flow

def check_yt():
    """
    Checks if the user is logged in with Youtube. If not, redirects them to the home page (to be used in yt login only pages)
    """
    credentials = session.get('yt_token_info', None)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flash('YouTube account authorization needed!')
            return redirect('/')
        
    session['yt_token_info'] = credentials

def get_yt_user():
    """
    Gets the current youtube user API object based on the session token.
    """
    return build('youtube', 'v3', credentials=session['yt_token_info'], cache_discovery=False)


 