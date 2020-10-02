import base64
import requests
import datetime
from urllib.parse import urlencode
import json

##TODO add lots of error checking

# preparing request info/encoding
class SpotifyAPI(object):
    access_token = None
    access_token_expires = None
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'

    def __init__(self, c_id,c_s, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.client_id = c_id
        self.client_secret = c_s
    
    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret

        if not(client_id) or not(client_secret):
            raise Exception("Must set client_id and client_secret")
        else:
            client_creds = f'{client_id}:{client_secret}'
            client_creds_b64 = base64.b64encode(client_creds.encode())
            return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64= self.get_client_credentials()
        token_headers = {'Authorization':f'Basic {client_creds_b64}'}
        return token_headers

    def get_token_data(self):
        token_data = {'grant_type':'client_credentials'}
        return token_data

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)

        # print(r.json())
        # valid request
        if r.status_code not in range(200,299):
            return False

        data = r.json()
        now = datetime.datetime.now()
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)

        self.access_token = data['access_token']
        self.access_token_expires = expires 
        self.access_token_did_expire = expires < now
        return True


    # takes json dict of recent songs and returns list of artist ids
    def extract_artist_ids(self,recents):
        artist_ids = []
        count = 0

        # iterate through songs and grab PRIMARY artist id
        # only grab primary because feature artists may be unrelated to genre
        # ex. Kanye West and Paul McCartney, FourFiveSeconds

        for song in recents['items']:
            count +=1
            ## ARTIST'S CODE
            artist_ids.append(song['track']['artists'][0]['id'])
        print(f"COUNT: {count}")
        
        return artist_ids

    # From original recent tracks json, get list of just artist objects
    def retrieve_artist_objects(self,json_tracks):
        # converting json_track input into a dictionary for indexing
        recents = json.load(json_tracks)

        # get ids as list, turn into string separated by comma
        # preparing to be entered into request URL
        data = ','.join(self.extract_artist_ids(recents))
        json_tracks.close()

        # more request prep
        header = {'Authorization':f'Bearer {self.access_token}'}
        endpoint = "https://api.spotify.com/v1/artists"
        lookup_url = f'{endpoint}?ids={data}'

        r = requests.get(lookup_url,headers=header)
        return r
    
    def extract_artist_names(self,artists):
        if "artists" in artists:
            print("COMPILED ARTISTS")
        if "items" in artists:
            print("TOP ARTISTS")

        r_dict=json.loads(artists.text)
        names = []
        for a in r_dict['artists']:
            names.append(a['name'])
        return names

    # returns a dictionary of genres user has recently listened to based off of
    # their recent artists tags
    def compile_genres(self, artists):
        # TODO add error check
        # convert response
        r_dict=json.loads(artists.text)
        gdict = {}
        for a in r_dict['artists']:
            #print(a['name'])
            #print(f"GENRES: {a['genres']}\n")
            for g in a['genres']:
                if g in gdict:
                    gdict[g] += 1
                else:
                    gdict[g] = 1
        return(gdict)




## FOR TESTING
def main():
    client_id = 'CLIENT_ID'
    client_secret = 'CLIENT_SECRET'
    spotify = SpotifyAPI(client_id,client_secret)
    spotify.perform_auth()

    ## response is original call of recently played
    json_file = open("response.json")
    data = json_file

    ## retrieve_artist_objects takes that json, and does another call
    ## to get full artist object, which has genre tags
    artists_json = spotify.retrieve_artist_objects(data)

    print(spotify.extract_artist_names(artists_json))
    ## get_genre_dict then returns combined dictionary of all of the user's recent artists genres
    #print(spotify.compile_genres(artists_json))
    

if __name__ == '__main__':
    main() 