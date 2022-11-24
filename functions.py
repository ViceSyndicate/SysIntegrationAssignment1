import datetime
import webbrowser
import requests
from requests.exceptions import HTTPError
import re

# NOTE We can replace Size=50 with pagination=false in our url's to avoid limiting our results
def getChannels():
    api_url = "http://api.sr.se/api/v2/channels/?format=json"
    dictionary = getRequestReturnJsonOrNone(api_url)
    if dictionary != None:
        channels = dictionary["channels"]
        chooseStation(channels)


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
    elif userInput == "2":
        listLastSong(val, channels)
    elif userInput == "3":
        channelId = channels[(int(val))]['id']
        getDailyChannelSchedule(channelId)
    else:
        print("Invalid input")


def playStation(stationVal, channels):
    channelUrl = channels[(int(stationVal))]['liveaudio']['url']
    webbrowser.open_new_tab(channelUrl)


def listLastSong(stationVal, channels):
    channelId = channels[(int(stationVal))]['id']
    songData = getRequestReturnJsonOrNone(f'http://api.sr.se/api/v2/playlists/rightnow?channelid={channelId}&format=json')
    if songData != None:
        print(f"Previous Song: {songData['playlist']['previoussong']['artist']} - {songData['playlist']['previoussong']['title']}")


def getDailyChannelSchedule(channelId):
    jsonData = getRequestReturnJsonOrNone(f'http://api.sr.se/api/v2/scheduledepisodes?channelid={channelId}&format=json&Size=50')
    if jsonData != None:
        schedules = jsonData['schedule']
        for schedule in schedules:
            temp = schedule['starttimeutc']
            startTimeInMillis = re.findall(r'\d+', temp)
            startTime = datetime.datetime.fromtimestamp(int(startTimeInMillis[0]) / 1000)
            startTime = startTime.strftime('%H:%M')
            print(startTime + " - " + schedule['title'])


#Could use improvement
def searchForProgram():
    userInput = input("Search Query: ")
    jsonData = getRequestReturnJsonOrNone(f'http://api.sr.se/api/v2/episodes/search/?query={userInput}&format=json&Size=50')
    if jsonData != None:
        tenFirstResults = jsonData['episodes']
        resultCounter = 0
        for result in tenFirstResults:
            playedDate = result['broadcasttime']['starttimeutc']
            startTimeInMillis = re.findall(r'\d+', playedDate)
            startTime = datetime.datetime.fromtimestamp(int(startTimeInMillis[0]) / 1000)
            #Leftover formatting example for Adora
            #startTime = startTime.strftime('%D - %H:%M')
            print(f"{resultCounter}. {startTime}: {result['title']}")
            print(result['url'])
            resultCounter = resultCounter + 1


#WIP
def checkForAlerts():
    jsonData = getRequestReturnJsonOrNone("https://vmaapi.sr.se/testapi/v2/alerts")
    alerts = jsonData['alerts']
    if jsonData != None:
        for alert in alerts:
            #status = "actual" makes sure we only list real alerts and not tests.
            if alert['status'] == "Test" and alert['msgType'] != "Cancel" :# Remember to change this to 'actual'
                print(f"{alert['msgType']}. ID: {alert['incidents']}")

                if alert['info'] != None:
                    affectedAreas = []
                    for infoInAlert in alert['info']:
                        print(f"Category: {infoInAlert['category']}")
                        print(f"Urgency: {infoInAlert['urgency']}")
                        print(f"Event: {infoInAlert['event']}")
                        print(f"Description: {infoInAlert['description']}")
                        for area in infoInAlert['area']:
                            affectedAreas.append(area['areaDesc'])
                        print(f"Affected Areas: {affectedAreas}")


# Returns None if exception occurred. Do "if != None" check before using returned data.
def getRequestReturnJsonOrNone(url):
    try:
        request = requests.get(url)
        request.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error: {http_err}')
    except Exception as err:
        print(f'Other error: {err}')
    else:
        return request.json()
