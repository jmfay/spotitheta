import spotify_api
from numpy import dot
from numpy.linalg import norm

## takes two dictionaries and creates empty value keys for genres found in other dictionary. Used to properly calculate vectors
def equalize(dict1,dict2):
    for genre in dict1.keys():
        if genre not in dict2:
            dict2[genre] = 0
    
    for genre in dict2.keys():
        if genre not in dict1:
            dict1[genre] = 0
    return


def get_cosine_sim(dict1,dict2):
    equalize(dict1,dict2)
    vec1,vec2 = [j for i,j in sorted(dict1.items())], [j for i,j in sorted(dict2.items())]

    # vectors now set up for calculation
    cos_sim = dot(vec1,vec2)/(norm(vec1)*norm(vec2))
    print(cos_sim)
    return(cos_sim)


def main():
    client_id = '042f6a5ce691471d8e4da836ae43db97'
    client_secret = 'aebc2f4fcdc54410b4aedb10f8bb3f5d'
    spotify = spotify_api.SpotifyAPI(client_id,client_secret)
    spotify.perform_auth()

    ## FILES CONTAINING RESPONSE FROM API
    ## GET RECENTLY PLAYED ARTISTS
    json_file = open("response.json")
    data = json_file
    json_file2 = open("response2.json")
    data2 = json_file2

    # Files are closed in process of retrieve_artist_objects
    # retrieve_artist_objects makes second call to API get full artist objects

    
    artists1 = spotify.retrieve_artist_objects(data)
    artists2 = spotify.retrieve_artist_objects(data2)

    names1 = spotify.extract_artist_names(artists1)
    names2 = spotify.extract_artist_names(artists2)

    for i in range(0,len(names1)):
        print(f"USER 1: {names1[i]}")
        print(f"\t\t\t\tUSER 2: {names2[i]}")

    ## SUB IN GET TOP ARTISTS RESPONSE HERE
    json_file_top = open("top_response.json")
    data3 = json_file_top
    dict1 = spotify.compile_genres(data3)
    dict2 = spotify.compile_genres(artists2)
    get_cosine_sim(dict1,dict2)





if __name__ == '__main__':
    main()