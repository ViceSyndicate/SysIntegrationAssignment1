import webbrowser
import requests
from requests.exceptions import HTTPError
import json


def getChannels():
    api_url = "http://api.sr.se/api/v2/channels/?format=json"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error: {http_err}')
    except Exception as err:
        print(f'Other error: {err}')
    else:
        dictionary = response.json()
        channels = dictionary["channels"]
        return channels


#WIP
def chooseStation(channels):
    # List Channels
    stationCounter = 0
    for channel in channels:
        print(f'{stationCounter} - {channel["name"]}')
        stationCounter = stationCounter + 1
    val = input("Pick a station: ")
    # accept only integers between 0 and stationCounter
    stationOptions(val, channels)


#WIP
def stationOptions(val, channels):
    # add other options or data you'd like from chosen station.
    playStation(val, channels)


def playStation(stationVal, channels):
    channelUrl = channels[(int(stationVal))]['liveaudio']['url']
    webbrowser.open_new_tab(channelUrl)
    listLastAndNextSong(stationVal, channels)


def listLastAndNextSong(stationVal, channels):
    channelId = channels[(int(stationVal))]['id']
    currentSongRequest = requests.get(f'http://api.sr.se/api/v2/playlists/rightnow?channelid={channelId}&format=json')
    songData = currentSongRequest.json()
    print(f"Previous Song \nArtist: {songData['playlist']['previoussong']['artist']} - Song: {songData['playlist']['previoussong']['title']}")
    print(f"Next Song \nArtist: {songData['playlist']['nextsong']['artist']} - Song: {songData['playlist']['nextsong']['title']}")
