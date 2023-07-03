from flask import Flask, request, session, redirect, render_template
from flask_session import Session
from auth_spot import time_form, create_spotify_oauth, get_spotify_user

app = Flask(__name__)
app.jinja_env.filters["time"] = time_form

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def index():
    return redirect('/playlists')


@app.route('/authspotify')
def authspotify():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear
    code = request.args.get('code')
    session['token_info'] = sp_oauth.get_access_token(code)
    return redirect('/')


@app.route('/playlists')
def showPlaylists():
    sp = get_spotify_user()  
    if not sp:
        return redirect('/authspotify')
     
    playlists = []

    for list in sp.current_user_playlists()['items']:
        playlist = {'id': list['id'], 'name': list['name'],'description': list['description'] 
                    ,'image': sp.playlist_cover_image(list['id'])[0]['url'], 'count': list['tracks']['total']}
        playlists.append(playlist)

    return render_template('playlists.html', playlists=playlists)

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/view')
def view():
    sp = get_spotify_user()
    if not sp:
        return redirect('/authspotify')

    playlist_id =  request.args.get('playlist_id')
    name = request.args.get('name')
    req = sp.playlist_items(playlist_id=playlist_id, fields='items.track(name, duration_ms, preview_url, artists(name))')['items']
    playlist = []
    for item in req:
        track = item.get('track')
        if not track:
            continue

        song = {'name': track['name'], 'duration': track['duration_ms'], 'url': track['preview_url']}

        artists = []
        for artist in track['artists']:
            artists.append(artist['name'])
            
        song['artists'] = ', '.join(artists)
        playlist.append(song)

    return render_template("view.html", playlist=playlist, name=name)


@app.route('/delete')
def delete():
    sp = get_spotify_user()
    if not sp:
        return redirect('/authspotify')
    
    playlist_id = request.args.get('playlist_id')
    sp.current_user_unfollow_playlist(playlist_id=playlist_id)

    return redirect('/')





