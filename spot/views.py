from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import redirect
import spotipy
import spotipy.util as util
from spotipy import oauth2
from django.views.generic.base import RedirectView


scope = " ".join(
    [
        'user-read-email user-top-read user-read-recently-played'
    ]
)
print(scope)
SPOTIPY_CLIENT_ID = 'CLIENT_ID'
SPOTIPY_CLIENT_SECRET = 'CLIENT_SECRET'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/dashboard'
username=''

def next_offset(n):
    try:
        return int(n['next'].split('?')[1].split('&')[0].split('=')[1])
    except ValueError:
        return None
    except AttributeError:
        return None
    except TypeError:
        return None


posts = [
    {
        'author':'JMFay',
        'title':'Blog Post 1',
        'content':'First post content',
        'date_posted':'August 27,2018'
    },
    {
        'author':'TomArner',
        'title':'Blog Post 2',
        'content':'I love dried mangos and my dogs so much!',
        'date_posted':'August 28,2018'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request,'spot/home.html',context)

def about(request):
    return render(request,'spot/about.html',{'title': 'About'})

def login(request):
    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                   scope=scope, cache_path=".cache-" + username)
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        return HttpResponseRedirect(auth_url)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    total = []
    results = sp.current_user_top_artists(time_range = 'medium_term', limit=50)
    for i, item in enumerate(results['items']):
        print(i,item['name'])
    total.append(results)
    """
    next = next_offset(results)

    total.append(results)
    while next and next < int(results['total']):
        next_50 = sp.current_user_recently_played(limit=50)
        next = next_offset(next_50)
        total.append(next_50)
        print(next)
    """
    
    tracks = []
    for track in results['items']:
        tracks.append(track)
    """
    for r in total:
        for track in r['items']:
            tracks.append(track)
    """

    return render(request, 'spot/dashboard.html', {'results': tracks, 'title':'Spotitheta - Dashboard'})

def dashboard(request):
    results = {}
    token = 'http://localhost:8000/dashboard/?{}'.format(request.GET.urlencode())
    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                   scope=scope, cache_path=".cache-" + username)
    code = sp_oauth.parse_response_code(token)
    token_info = sp_oauth.get_access_token(code)
    if token_info:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        results = sp.current_user_top_tracks()
    return render(request, 'spot/dashboard.html', {'results': results['items']})
