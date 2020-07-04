from flask import Flask, redirect, url_for, request
from urllib.parse import urlencode, quote_plus
import requests
import base64
import json
from dotenv import load_dotenv
from os import environ
from random import randint
load_dotenv()

app = Flask(__name__)
app.debug = True

#lol its already time to refactor

CLIENT_ID = environ.get('CLIENT_ID')
CLIENT_SECRET = environ.get('CLIENT_SECRET')
REDIRECT_URI = "http://127.0.0.1:5000/callback"

@app.route("/login")
def login():
    scope = "user-top-read user-read-private"

    # add state to queries

    auth_queries = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": scope,
    }

    print(
        "https://accounts.spotify.com/authorize?"
        + urlencode(auth_queries, quote_via=quote_plus)
    )

    return redirect(
        "https://accounts.spotify.com/authorize?"
        + urlencode(auth_queries, quote_via=quote_plus)
    )


@app.route("/callback")
def callback():
    auth_code = request.args.get("code")
    # add state

    message = CLIENT_ID + ":" + CLIENT_SECRET
    message_bytes = message.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode("ascii")

    headers = {"Authorization": "Basic " + base64_message}

    body = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }

    res = requests.post(
        url="https://accounts.spotify.com/api/token", headers=headers, data=body
    )

    #just doing this to easily see stuff since we dont have a front end
    return getStartAndEndArtists(json.loads(res.text)['access_token'])


@app.route("/refresh_token")
def refreshToken():
    # req param will be the refresh token
    # send post req to api with refresh token to receive new access token
    pass


#right now this grabs the users top 50 artists, we can expand upon this later
#it could pull randomly from all their saved tracks
#it could force them to be above a certain popularity( we prob want this)
#it could make sure they dont share any (all?) genres
def getStartAndEndArtists(userAuth):
    headers = {
        'Authorization':'Bearer ' + userAuth
    }
    r = requests.get(url = 'https://api.spotify.com/v1/me/top/artists?limit=50', headers=headers)
    res = json.loads(r.text)
    artists = []
    for item in res['items']:
        artists.append({
            'id' : item['id'],
            'name' : item['name']
        })

    startArtist = artists[randint(0, len(artists)-1)]
    endArtist = artists[randint(0, len(artists)-1)]

    return 'startArtist: ' + startArtist['name'] + ', endArtist: ' + endArtist['name']

if __name__ == "__main__":
    app.run()
