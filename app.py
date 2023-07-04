from flask import Flask, request, session, redirect, render_template, flash
from flask_session import Session
from auth_spot import create_spotify_oauth, get_spotify_user, time_play, time_track
from auth_yt import youtube_oauth

app = Flask(__name__)
app.jinja_env.filters["track_time"] = time_track
app.jinja_env.filters["play_time"] = time_play

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spotify_playlists')
def sp_playlist():
    sp = get_spotify_user()  
    if not sp:
        flash('Spotify account authorization needed!')
        return redirect('/')
    
    playlists = []

    for list in sp.current_user_playlists()['items']:
        playlist = {'id': list['id'], 'name': list['name'],'description': list['description'] 
                    ,'image': sp.playlist_cover_image(list['id'])[0]['url'], 'count': list['tracks']['total']}
        playlists.append(playlist)

    return render_template('playlist.html', playlists=playlists)

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

    flash(f'Successfully connected to YouTube as username!')
    return redirect('/')
    

@app.route('/view')
def view():
    sp = get_spotify_user()
    if not sp:
        flash('Spotify account authorization needed')
        return redirect('/')
    
    playlist_id =  request.args.get('playlist_id')
    name = request.args.get('name')
    req = sp.playlist_items(playlist_id=playlist_id, fields='items.track(name, duration_ms, preview_url, artists(name))')['items']
    playlist = []
    time = 0
    for item in req:
        track = item.get('track')
        if not track:
            continue
        time += track['duration_ms']
        song = {'name': track['name'], 'duration': track['duration_ms'], 'url': track['preview_url']}
        artists = []
        for artist in track['artists']:
            artists.append(artist['name'])
            
        song['artists'] = ', '.join(artists)
        playlist.append(song)

    return render_template("view.html", playlist=playlist, name=name, time=time)


@app.route('/delete')
def delete():
    sp = get_spotify_user()
    if not sp:
        flash('Spotify account authorization needed')
        return redirect('/auth')
    
    playlist_id = request.args.get('playlist_id')
    sp.current_user_unfollow_playlist(playlist_id=playlist_id)

    return redirect('/')

@app.route('/disconnect', methods=['POST', 'GET'])
def disconnect():
    dis = request.form.get('disconnect')
    if dis == 'Spotify':
        session['spot_token_info'] = None
    elif dis == 'YouTube':
        session['yt_token_info'] = None

    flash(f'Successfully disconnected from {dis}!')
    return redirect('/')





