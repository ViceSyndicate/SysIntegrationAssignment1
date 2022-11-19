import datetime
import webbrowser
import requests
from requests.exceptions import HTTPError
import re
import time


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
    print("1 - Play Station")
    print("2 - List Last Song")
    print("3 - Get Station Schedule")
    userInput = input()
    if userInput == "1":
        playStation(val, channels)
    if userInput == "2":
        listLastSong(val, channels)
    if userInput == "3":
        channelId = channels[(int(val))]['id']
        getDailyChannelSchedule(channelId)
    else:
        print("Invalid input")
    return


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


#WIP Might turn in to daily
def getDailyChannelSchedule(channelId):

    # scheduleList = []
    #milliSeconds = int(time.time() * 1000)

    #TODO error handling of GET request
    request = requests.get(f'http://api.sr.se/api/v2/scheduledepisodes?channelid={channelId}&format=json')
    requestJson = request.json()
    schedules = requestJson['schedule']
    for schedule in schedules:
        temp = schedule['starttimeutc']
        startTimeInMillis = re.findall(r'\d+', temp)
        startTime = datetime.datetime.fromtimestamp(int(startTimeInMillis[0])/1000)
        print(str(startTime)  + " - " +  schedule['title'])
        #scheduleList.append(startTimeInMillis[0])
    return

#Considering making a function for get requests that does try/catch.