from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from flask import session, redirect, flash

# write (your_website)/redirectyoutube in redirect_uri
# creates an oauth flow based on the given api credentials
def youtube_oauth():
    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json',
                                                    redirect_uri='http://127.0.0.1:5000/redirectyoutube',
                                                    scopes=['https://www.googleapis.com/auth/youtubepartner',
                                                        'https://www.googleapis.com/auth/youtube',
                                                        'https://www.googleapis.com/auth/youtube.force-ssl'])
    return flow

# to be called before every function that requires youtube authorization
# check if user is logged into youtube and/or their credentials are valid.
def check_yt():
    credentials = session.get('yt_token_info', None)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flash('YouTube account authorization needed!')
            return redirect('/')
        
    session['yt_token_info'] = credentials

# return an api object based on current logged in user, that can be used to make api calls
def get_yt_user():
    return build('youtube', 'v3', credentials=session['yt_token_info'], cache_discovery=False)


 