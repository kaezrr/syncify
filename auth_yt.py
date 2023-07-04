from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json',
                                                 redirect_uri='http://127.0.0.1:5000/redirectyoutube',
                                                  scopes=['https://www.googleapis.com/auth/youtubepartner',
                                                    'https://www.googleapis.com/auth/youtube',
                                                    'https://www.googleapis.com/auth/youtube.force-ssl'])

def youtube_oauth():
    return flow
 