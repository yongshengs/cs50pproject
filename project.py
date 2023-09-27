import requests
import urllib.parse

from datetime import datetime, timedelta
from flask import Flask, redirect, request, jsonify, session, render_template


app = Flask(__name__)
app.secret_key = ''

# Define a custom Jinja2 filter
def format_number(value):
    return "{:,}".format(value)
# Add the filter to Jinja2 environment
app.jinja_env.filters['format_number'] = format_number

CLIENT_ID=''
CLIENT_SECRET=''
REDIRECT_URI='http://localhost:5000/callback'

AUTH_URL='https://accounts.spotify.com/authorize/'
TOKEN_URL='https://accounts.spotify.com/api/token/'
API_BASE_URL='https://api.spotify.com/v1/'


# landing page
@app.route('/')
def index():
    return render_template('home.html')


# Spotify login page
@app.route('/login')
def login():
    scope = 'user-read-private user-read-email user-library-read playlist-read-private user-top-read user-follow-read'
    
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True #by default this is False, but for testing purpose, we want to login every time we reach this page
    }

    # Spotify docs state that we need to make a GET request to an authorization URL with these params, we can use the requests lib to do that 
    # But, in Spotify docs JavaScript example, they redirect to a URL (which in itself is a GET request) to pass the params
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return render_template('login.html', auth_url=auth_url)


@app.route('/callback')
def callback():
    # check if Spotify returns an error
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    
    # if user login is successful, Spotify will return the auth code which we need to include in another request to Spotify to get the acccess, refresh tokens
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    response = requests.post(TOKEN_URL, data=req_body)
    token_info = response.json()

    # storing the tokens and expiry value in session
    session['access_token'] = token_info['access_token'] # to use to access Spotify Web API, lasts for 1h
    session['refresh_token'] = token_info['refresh_token'] # use this to refresh access token when it expires
    session['expires_at'] = datetime.now().timestamp() + token_info['expires_in'] # number of seconds the access token is valid for
    return redirect('/playlists')


@app.route('/playlists')
def get_playlists():
    # check if access token is in session
    if 'access_token' not in session:
        return redirect('/login')
    
    # if access token is in session,  check if it has expired
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    response = requests.get(API_BASE_URL + 'me/playlists?limit=24', headers=headers)
    playlists_data = response.json()
    playlists = playlists_data.get('items', [])
    return render_template('playlists.html', playlists=playlists)


@app.route('/refresh-token')
def refresh_token():
    # check if refresh token is in session
    if 'refresh_token' not in session:
        return redirect('/login')
    
    # if refresh token in session, check if access is expired
    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()

        # update session information
        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in'] 
        return redirect('/playlists')


@app.route('/followed-artists')
def followed_artists():
    if 'refresh_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    response = requests.get(API_BASE_URL + 'me/following?type=artist&limit=30', headers=headers)
    followed_artists_data = response.json()
    followed_artists = followed_artists_data.get('artists', {}).get('items', [])
    return render_template('followed-artists.html', followed_artists=followed_artists)


@app.route('/top-tracks')
def top_tracks():
    if 'refresh_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')   
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    response = requests.get(API_BASE_URL + 'me/top/tracks?time_range=medium_term&limit=48', headers=headers)
    top_tracks_data = response.json()
    top_tracks = top_tracks_data.get('items', [])
    return render_template('top-tracks.html', top_tracks=top_tracks)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)