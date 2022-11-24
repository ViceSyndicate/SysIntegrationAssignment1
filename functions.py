import datetime
import webbrowser
import requests
from requests.exceptions import HTTPError
import re


# NOTE We can replace Size=50 with pagination=false in our url's to avoid limiting our results
def get_channels():
    api_url = "https://api.sr.se/api/v2/channels/?format=json"
    dictionary = get_request_return_json_or_none(api_url)
    if dictionary is not None:
        channels = dictionary["channels"]
        choose_station(channels)


def choose_station(channels):
    # List Channels
    station_counter = 0
    for channel in channels:
        print(f'{station_counter} - {channel["name"]}')
        station_counter = station_counter + 1
    val = input("Pick a station: ")
    try:
        val = int(val)
    except Exception as err:
        print(f'Invalid station option: {err}')
        return
    if val < 0 or val > station_counter:
        print("Invalid station option")
        return
    station_options(val, channels)


# WIP
def station_options(val, channels):
    # add other options or data you'd like from chosen station.
    print("1 - Play Station")
    print("2 - List Last Song")
    print("3 - Get Station Schedule")
    user_input = input()
    if user_input == "1":
        play_station(val, channels)
    elif user_input == "2":
        list_last_song(val, channels)
    elif user_input == "3":
        channel_id = channels[(int(val))]['id']
        get_daily_channel_schedule(channel_id)
    else:
        print("Invalid input")


def play_station(stationVal, channels):
    channel_url = channels[(int(stationVal))]['liveaudio']['url']
    webbrowser.open_new_tab(channel_url)


def list_last_song(stationVal, channels):
    channel_id = channels[(int(stationVal))]['id']
    song_data = get_request_return_json_or_none(
        f'https://api.sr.se/api/v2/playlists/rightnow?channelid={channel_id}&format=json')
    if song_data is not None:
        print(f"Previous Song: {song_data['playlist']['previoussong']['artist']}"
              f" - {song_data['playlist']['previoussong']['title']}")


def get_daily_channel_schedule(channelId):
    json_data = get_request_return_json_or_none(
        f'https://api.sr.se/api/v2/scheduledepisodes?channelid={channelId}&format=json&pagination=false')
    if json_data is not None:
        schedules = json_data['schedule']
        for schedule in schedules:
            temp = schedule['starttimeutc']
            start_time_in_millis = re.findall(r'\d+', temp)
            start_time = datetime.datetime.fromtimestamp(int(start_time_in_millis[0]) / 1000)
            start_time = start_time.strftime('%H:%M')
            print(start_time + " - " + schedule['title'])


# Could use improvement
def search_for_program():
    user_input = input("Search Query: ")
    json_data = get_request_return_json_or_none(
        f'https://api.sr.se/api/v2/episodes/search/?query={user_input}&format=json&Size=50')
    if json_data is not None:
        results = json_data['episodes']
        result_counter = 0
        for result in results:
            played_date = result['broadcasttime']['starttimeutc']
            start_time_in_millis = re.findall(r'\d+', played_date)
            start_time = datetime.datetime.fromtimestamp(int(start_time_in_millis[0]) / 1000)
            # start_time = start_time.strftime('%D - %H:%M')
            print(f"{result_counter}. {start_time}: {result['title']}")
            print(result['url'])
            result_counter = result_counter + 1


# WIP
def check_for_alerts():
    json_data = get_request_return_json_or_none("https://vmaapi.sr.se/testapi/v2/alerts")
    alerts = json_data['alerts']
    if json_data is not None:
        for alert in alerts:
            # status = 'actual' makes sure we only list real alerts and not tests.
            # status = 'Test' can be used for test data
            if alert['status'] == "actual" and alert['msgType'] != "Cancel":
                print(f"{alert['msgType']}. ID: {alert['incidents']}")
                if alert['info'] is not None:
                    for infoInAlert in alert['info']:
                        print(f"Category: {infoInAlert['category']}")
                        print(f"Urgency: {infoInAlert['urgency']}")
                        print(f"Event: {infoInAlert['event']}")
                        print(f"Description: {infoInAlert['description']}")
                        print(f"Affected Areas", end=': ')
                        for area in infoInAlert['area']:
                            print(f"{area['areaDesc']}", end=', ')


# Returns None if exception occurred. Do "if != None" check before using returned data.
def get_request_return_json_or_none(url):
    try:
        request = requests.get(url)
        request.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error: {http_err}')
    except Exception as err:
        print(f'Other error: {err}')
    else:
        return request.json()
