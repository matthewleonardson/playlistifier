import sys
import spotipy
import spotipy.util as util
import dotenv
from dotenv import load_dotenv

dotenv_path = ".env"
current_user = ""

def get_all_saved_tracks(client):
    '''
    Returns a list of URIs of all tracks in the user's liked songs
    '''

    tracks = []
    while len(tracks) % 50 == 0:
        next_tracks = client.current_user_saved_tracks(limit=50, offset=len(tracks))
        for track in next_tracks['items']:
            tracks.append(track['track']['uri'])
    return tracks

def playlist_exists(client, playlist_id):
    '''
    Returns whether the playlist associated with playlist_id exists,
    (slight abuse of notation, it actually returns  whether the user
    still follows the playlist, as playlists dont ever get "deleted")
    '''

    return client.playlist_is_following(playlist_id, [client.current_user()['id']])[0]

def create_playlist(client):
    '''
    Creates a new playlist for the user and sets the environment variable accordingly
    '''

    response = client.user_playlist_create(current_user, name="Liked Songs (Playlistifier)", public=False)
    dotenv.set_key(dotenv_path, "{}_PLAYLISTIFIER_PLAYLIST_ID".format(current_user).upper(), response['id'])
    load_dotenv()    

def update_playlist(client, tracks):
    '''
    Appends tracks to the existing playlist_id that is currently in environment variables
    '''

    for n in range(0, len(tracks), 100):
        client.playlist_add_items(dotenv.get_key(dotenv_path, "{}_PLAYLISTIFIER_PLAYLIST_ID".format(current_user).upper()), tracks[n:min(n + 100, len(tracks))])

def post_to_playlist(client, tracks):
    '''
    This function will handle whether a new playlist needs to be created 
    or whether we can just update an existing playlist for the user
    '''
    
    playlist_id = dotenv.get_key(dotenv_path, "{}_PLAYLISTIFIER_PLAYLIST_ID".format(current_user).upper())
    if playlist_id != None and playlist_exists(client, playlist_id):
        update_playlist(client, tracks)
    else:
        create_playlist(client) 
        update_playlist(client, tracks)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    load_dotenv()
    scope = 'user-library-read, playlist-modify-private, playlist-read-private'
    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        current_user = sp.current_user()['id']
        tracks = get_all_saved_tracks(sp) 
        post_to_playlist(sp, tracks)
    else:
        print("Couldn't get token for", username)

