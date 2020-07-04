from flask import Flask
from flask import request
import requests
import base64
import json
app = Flask(__name__)

@app.route('/test')
def hello_world():
    
    r = requests.post(url='https://accounts.spotify.com/api/token', auth = ("8fd5853e144f4922a3b5143e69eee7bd", "7bd14afb8f3e4a468f0dc9d593fcbedb"), data={'grant_type':'client_credentials'})
    access_code = json.loads(r.text)['access_token']
    print(access_code)

    headers = {
        'Authorization':'Bearer ' + access_code
    }

    params = {
        'type':'artist',
        'q':request.args.get('artistName')
    } 
    searchResult = requests.get(url='https://api.spotify.com/v1/search', params=params, headers=headers)
    firstResult = json.loads(searchResult.text)['artists']['items'][0]
    print(firstResult['name'])
    artistId = firstResult['id']

    r = requests.get(url='https://api.spotify.com/v1/artists/' + artistId + '/related-artists', headers=headers)
    artists = json.loads(r.text)['artists']
    artistNames  = []

    for artist in artists:
        artistNames.append(artist['name'])

    return str(artistNames)