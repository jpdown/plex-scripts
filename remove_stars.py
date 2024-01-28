import sys
from plexapi.myplex import MyPlexAccount
from plexapi.exceptions import NotFound

USERNAME = ""
PASSWORD = ""
TWO_FA_CODE = ""
SERVER = ""
MUSIC_LIBRARY = ""

account = MyPlexAccount(USERNAME, PASSWORD, code=TWO_FA_CODE)
plex = account.resource(SERVER).connect()

music_section = plex.library.section(MUSIC_LIBRARY)

print("starting")

playlists = [None] * 10

for song in music_section.searchTracks(filters={"userRating>>": 0}):
#    print(song)
    playlist_name = f"previously rated {song.userRating / 2}"
    index = int(song.userRating) - 1

    if playlists[index] is None:
        try:
            playlists[index] = music_section.playlist(playlist_name)
        except NotFound:
            playlists[index] = music_section.createPlaylist(playlist_name, items=[song])
            continue

    if song not in playlists[index]:
        playlists[index].addItems([song])
    song.rate()

print("done")
