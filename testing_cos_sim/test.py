import spotipy
from spotipy.oauth2 import SpotifyOAuth


 
sp = spotipy.Spotify(auth_manager=
SpotifyOAuth(client_id="CLIENT_ID", client_secret="CLIENT_SECRET", redirect_uri="http://localhost:8001#", scope="user-library-read user-read-recently-played")
)


results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])