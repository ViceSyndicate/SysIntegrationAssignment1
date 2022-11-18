import webbrowser
import requests
from requests.exceptions import HTTPError


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


def chooseStation(channels):
    # List Channels
    stationCounter = 0
    for channel in channels:
        print(f'{stationCounter} - {channel["name"]}')
        stationCounter = stationCounter + 1
    val = input("Pick a station: ")
    try:
        val = int(val)
    except Exception as err:
        print(f'Invalid station option: {err}')
        return
    if val < 0 or val > stationCounter:
        print("Invalid station option")
        return
    stationOptions(val, channels)


#WIP
def stationOptions(val, channels):
    # add other options or data you'd like from chosen station.
    # TODO: Implement menu similar to main.menuOptions()
    listLastSong(val, channels)
    playStation(val, channels)


def playStation(stationVal, channels):
    channelUrl = channels[(int(stationVal))]['liveaudio']['url']
    webbrowser.open_new_tab(channelUrl)


def listLastSong(stationVal, channels):
    channelId = channels[(int(stationVal))]['id']
    try:
        currentSongRequest = requests.get(f'http://api.sr.se/api/v2/playlists/rightnow?channelid={channelId}&format=json')
        currentSongRequest.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error: {http_err}')
    except Exception as err:
        print(f'Other error: {err}')
    songData = currentSongRequest.json()
    print(f"Previous Song: {songData['playlist']['previoussong']['artist']} - {songData['playlist']['previoussong']['title']}")


#Considering making a function for get requests that does try/catch.