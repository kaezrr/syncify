from flask import Flask, request, session, redirect, render_template, flash
from flask_session import Session
from auth_spot import create_spotify_oauth, get_spotify_user, check_spot
from auth_yt import youtube_oauth, check_yt, get_yt_user
from helpers import time_play, time_track
import isodate

app = Flask(__name__)
app.jinja_env.filters["track_time"] = time_track
app.jinja_env.filters["play_time"] = time_play

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auth', methods=['POST', 'GET'])
def authorize():
    if request.method == 'POST':
        service = request.form.get('connect')
        if service == 'spotify':
            sp_oauth = create_spotify_oauth()
            auth_url = sp_oauth.get_authorize_url()
            
            return redirect(auth_url)
        elif service == 'youtube':
            yt_oauth = youtube_oauth()
            auth_url = yt_oauth.authorization_url()
            
            return redirect(auth_url[0])
    else:
        spot_auth = session.get('spot_token_info', None) != None
        yt_auth = session.get('yt_token_info', None) != None

        return render_template('auth.html', spot_auth=spot_auth, yt_auth=yt_auth)
    

@app.route('/playlists_spotify', methods=['GET', 'POST'])
def sp_playlist():
    check = check_spot()
    if check:
        return check
    
    sp = get_spotify_user()  
    playlists = []       

    for list in sp.current_user_playlists()['items']:
        playlist = {'type':'sp', 'id': list['id'], 'name': list['name'] ,'image': sp.playlist_cover_image(list['id'])[0]['url'],
                     'count': list['tracks']['total']}
        playlists.append(playlist)

    return render_template('playlist.html', playlists=playlists)


@app.route('/playlists_youtube')
def yt_playlist():
    check = check_yt()
    if check:
        return check
    
    yt = get_yt_user()
    response = yt.playlists().list(part='contentDetails,snippet', mine=True).execute()

    video_ids = response['items']

    while response.get('nextPageToken', None) != None:
        response = yt.playlists().list(part='contentDetails,snippet', mine=True, pageToken=response['nextPageToken']).execute()
        for item in response['items']:
            video_ids.append(item)

    playlists = []
    for item in video_ids:
        playlist = {'type':'yt', 'id':item['id'], 'name':item['snippet']['title'], 'image':item['snippet']['thumbnails']['standard']['url'],
                    'count':item['contentDetails']['itemCount']}
        playlists.append(playlist)


    return render_template('playlist.html', playlists=playlists)


@app.route('/redirectspotify')
def redirectSpotify():
    sp_oauth = create_spotify_oauth()
    session['spot_token_info'] = sp_oauth.get_access_token(request.args.get('code'))
    username = get_spotify_user().current_user()['display_name']

    flash(f'Successfully connected to Spotify as {username}!')
    return redirect('/')


@app.route('/redirectyoutube')
def redirectYoutube():
    yt_oauth = youtube_oauth()
    yt_oauth.fetch_token(code=request.args.get('code'))
    session['yt_token_info'] = yt_oauth.credentials

    yt=get_yt_user()
    response = yt.channels().list(part='snippet', mine=True).execute()
    username = response['items'][0]['snippet']['title']

    flash(f'Successfully connected to YouTube as {username}!')
    return redirect('/')
    

@app.route('/viewsp')
def viewsp():
    sp = get_spotify_user()  
    
    playlist_id =  request.args.get('playlist_id')
    name = request.args.get('name')
    playlist = []
    time = 0
    req = sp.playlist_tracks(playlist_id=playlist_id, fields='items.track(name, duration_ms, preview_url, artists.name)')['items']
    for item in req:
        track = item['track']
        time += track['duration_ms']
        song = {'name': track['name'], 'duration': track['duration_ms'], 'url': track['preview_url']}
        song['artists'] = ', '.join(artist['name'] for artist in track['artists'])
        playlist.append(song)

    return render_template("view.html", playlist=playlist, name=name, time=time)


@app.route('/viewyt')
def viewyt():
    yt = get_yt_user()
    id = request.args.get('playlist_id')
    name = request.args.get('name')
    time = 0

    response = yt.playlistItems().list(part='contentDetails', playlistId=id, maxResults=50).execute()
    video_ids = []
    playlist = []
    while True:
        temp = []
        for item in response['items']:
           temp.append(item['contentDetails']['videoId'])
        video_ids.append(temp)
        if response.get('nextPageToken', None) == None:
            break
        response = yt.playlistItems().list(part='contentDetails', playlistId=id, pageToken=response['nextPageToken'], maxResults=50).execute()

    for part in video_ids:
        response = yt.videos().list(part='snippet,contentDetails', id=','.join(part)).execute()
        while True:
            for item in response['items']:
                dur = isodate.parse_duration(item['contentDetails']['duration']).total_seconds() * 1000
                song = {'name': item['snippet']['title'], 'artists': item['snippet']['channelTitle'],
                        'duration': dur,
                        'url':f"https://youtu.be/{item['id']}"}
                time += dur
                playlist.append(song)
            if response.get('nextPageToken', None) == None:
                break
            response = yt.videos().list(part='snippet,contentDetails', id=','.join(part), pageToken=response['nextPageToken']).execute()
            
    return render_template("view.html", playlist=playlist, name=name, time=time)


@app.route('/deletesp')
def deletesp():   
    sp = get_spotify_user()  
    playlist_id = request.args.get('playlist_id')
    try:
        sp.current_user_unfollow_playlist(playlist_id=playlist_id)
    except:
        flash('Error!')
        return redirect('/playlists_spotify')

    flash('Playlist successfully deleted!')
    return redirect('/playlists_spotify')


@app.route('/deleteyt')
def deleteyt():
    yt = get_yt_user()
    id = request.args.get('playlist_id')
    try:
        yt.playlists().delete(id=id).execute()
    except:
        flash('Error!')
        return redirect('/playlists_youtube')
    
    flash('Playlist successfully deleted!')
    return redirect('/playlists_youtube')


@app.route('/disconnect', methods=['POST', 'GET'])
def disconnect():
    dis = request.form.get('disconnect')
    if dis == 'Spotify':
        session['spot_token_info'] = None
    elif dis == 'YouTube':
        session['yt_token_info'] = None

    flash(f'Successfully disconnected from {dis}!')
    return redirect('/')


@app.route('/convert', methods=['GET', 'POST'])
def convert():
    yt = get_yt_user()
    sp = get_spotify_user()
    if request.method == 'GET':
        id = request.args.get('playlist_id')
        name = request.args.get('name')
        queries = []
        playlist = []

        for item in sp.playlist_tracks(playlist_id=id, fields='items.track(name, artists.name)')['items']:
            track = item['track']
            query = [track['name']]
            query.extend(artist['name'] for artist in track['artists'])
            queries.append(' '.join(query)) 

        for query in queries:
            rep = yt.search().list(part='snippet,id', q=query, type='video', maxResults=1).execute()['items'][0]
            video = {'id': rep['id']['videoId'], 'name': rep['snippet']['title'],
                    'channel': rep['snippet']['channelTitle'], 'url': f"https://youtu.be/{rep['id']['videoId']}"}
            playlist.append(video)

        return render_template('convert.html', playlist=playlist, name=name)
    else:
        name = request.form.get('name')
        video_ids = request.form.getlist('videoId')
        response = yt.playlists().insert(part='snippet,status',
            body={
                'snippet': {
                    'title': name,
                    'description': 'This playlist was created via Spotube!.'
                },
                'status': {
                    'privacyStatus': 'private'
                }
            }).execute()
        
        playlist_id = response['id']
        for video_id in video_ids:
            yt.playlistItems().insert(
                part='snippet',
                body={
                    'snippet': {
                        'playlistId': playlist_id,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': video_id
                        }
                    }
                }
            ).execute()

        flash('Playlist successfully converted!')
        return redirect('/playlists_youtube')


