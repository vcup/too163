from data_sousa import lyric_tools
from data_sousa.path import KeyPath, IndexPath

from data_sousa.lyric import Lyric
from data_sousa.song import Song
from data_sousa.playlist import Playlist
from data_sousa.user_playlist import UserPlaylist
from data_sousa.album import Album
from data_sousa.artist import Artist


def lyric(data: dict) -> Lyric:
    return Lyric(data)


def song(data: dict) -> Song:
    return Song(data)


def playlist(data: dict) -> Playlist:
    return Playlist(data)


def user_playlist(data: dict) -> UserPlaylist:
    return UserPlaylist(data)


def album(data: dict) -> Album:
    return Album(data)


def artist(data: dict) -> Artist:
    return Artist(data)
