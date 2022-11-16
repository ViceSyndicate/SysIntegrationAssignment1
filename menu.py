import webbrowser

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
