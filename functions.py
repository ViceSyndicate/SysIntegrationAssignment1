import webbrowser
import urllib.request
import requests
import json
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
        dictionary = json.loads(response.content)
        channels = dictionary["channels"]
        return channels

def chooseStation(channels):
    # List Channels
    stationCounter = 0
    for channel in channels:
        print(f'{stationCounter} - {channel["name"]}')
        stationCounter = stationCounter + 1
    val = input("Pick a station: ")
    stationOptions(val, channels)

def stationOptions(val, channels):
    # add other options or data you'd like from chosen station.
    playStation(val, channels)

def playStation(stationVal, channels):
    channelUrl = channels[(int(stationVal))]['liveaudio']['url']
    webbrowser.open_new_tab(channelUrl)
    #list station options again?
