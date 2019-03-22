import json
import spotipy
import spotipy.util as util


class SpotifyController:
    def __init__(self):
        self.playlist_url_offset = 10
        with open('spotify-config.json') as json_file:
            config = json.load(json_file)
            self.client_id = config["spotify client id"]
            self.client_secret = config["spotify client secret"]
            self.redirect_url = config["spotify redirect url"]
            self.username = config["username"]

            self.scope = 'user-read-playback-state playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing user-modify-playback-state'
            auth_token = util.prompt_for_user_token(self.username, self.scope, self.client_id,
                                                    self.client_secret, self.redirect_url)
            self.client = spotipy.Spotify(auth_token)

    def next_track(self):
        if self.client:
            self.refresh_access_token()
            self.client.next_track()
            print("next")

    def previous_track(self):
        if self.client:
            self.refresh_access_token()
            self.client.previous_track()
            print("previous")

    def remove_current_track(self):
        if self.client:
            self.refresh_access_token()
            userID = self.client.me()['id']
            dict = self.client.current_playback()
            print("removing " + dict['item']['name'])
            songID = dict['item']['uri']
            href = dict['context']['href']
            playlistID = href[href.find(
                "playlists/") + self.playlist_url_offset:]
            self.client.user_playlist_remove_all_occurrences_of_tracks(
                userID, playlistID, {songID})
            self.client.next_track()

    def refresh_access_token(self):
        self.client._auth = util.prompt_for_user_token(self.username, self.scope, self.client_id,
                                                       self.client_secret, self.redirect_url)
