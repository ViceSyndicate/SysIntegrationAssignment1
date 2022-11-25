import requests

from main import menu_options


def traffic_menue():
    val = input("Press 1 traffic information, Press 2 to Back to menue options \n")

    while val:
        if val == '1':
            get_message()
        elif val == '2':
            menu_options()
        else:
            print(f"Don't know what to do with {val}.")
        val = input("Press 1 traffic information, Press 2 to Back to menue options \n")


def get_message():
    url = 'http://api.sr.se/api/v2/traffic/messages?format=json'
    r = requests.get(url)
    responce_dict = r.json()
    messages_ids = responce_dict['messages']
    print("\n...........")
    for message_id in messages_ids:
        print(f"Title: {message_id['title']}")
        print(f"Exactlocation: {message_id['exactlocation']}")
        print(f"Description: {message_id['description']}")
        print("\n...........")