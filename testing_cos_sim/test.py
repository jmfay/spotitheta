import spotipy
from spotipy.oauth2 import SpotifyOAuth


 
sp = spotipy.Spotify(auth_manager=
SpotifyOAuth(client_id="042f6a5ce691471d8e4da836ae43db97", client_secret="aebc2f4fcdc54410b4aedb10f8bb3f5d", redirect_uri="http://localhost:8001#", scope="user-library-read user-read-recently-played")
)


results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])