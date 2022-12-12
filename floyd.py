# Python version of Floyd Quotes bot

from csv import reader
from random import seed, randint
from datetime import datetime
from re import sub
from time import time, sleep
from mastodon import Mastodon
from os import environ

mastodon = Mastodon(api_base_url='https://botsin.space',
                    access_token=environ['MASTO_TOKEN'])
seed()


class Song():

    def __init__(self, rawSong):
        self.album = rawSong[0]
        self.title = rawSong[1]
        self.year = rawSong[2]
        self.lyrics = [
            line for line in rawSong[3].replace('\n\n', '\n').replace(
                '\\ n', ' ').split('\n') if len(line) > 20
        ]


def sanitize(quote):
    return sub("[` .,-?!'’()]", '', quote)


def loadSongs():
    with open('./pink_floyd_lyrics.csv', newline='', encoding='utf-8') as f:
        rawSongs = list(reader(f))

    songs = [Song(rawSong) for rawSong in rawSongs if rawSong[3].strip() != '']

    return songs


def doQuote(songs):
    songIndex = randint(0, len(songs) - 1)
    song = songs[songIndex]

    if len(song.lyrics) != 0:
        lineIndex = randint(0, len(song.lyrics) - 1)
        line = song.lyrics[lineIndex]

        toot = line + '\n\n' + '#' + sanitize(
            song.title) + ' ' + '#' + sanitize(song.album) + ' ' + '#PinkFloyd'
        print('\n' + datetime.now().strftime('%m/%d/%Y %H:%M') + ': ' + toot +
              '\n')
        mastodon.toot(toot)

        del song.lyrics[lineIndex]
        print('- ' + str(len(song.lyrics)) +
              ' lyric lines remains in this song\n')

    if len(song.lyrics) == 0:
        del songs[songIndex]
        print('- removing song with empty lyrics, ' + str(len(songs)) +
              ' songs remains\n')

        return len(songs)


songs = loadSongs()

interval = 60.0 * 60.0
startTime = time()

while True:
    songCount = doQuote(songs)
    if songCount == 0:
        print('- reloading songs\n')
        songs = loadSongs()

    sleep(interval - ((time() - startTime) % interval))

# Mastodon verification
# <a rel="me" href="https://botsin.space/@PinkFloydHourly">Mastodon</a>
