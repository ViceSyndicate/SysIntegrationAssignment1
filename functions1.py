from datetime import datetime
from requests.exceptions import HTTPError
import requests
import re
from main import menu_options


def my_menu():
    choice = input("[P]rogram details, [l]atest Published Programs or [m]enu Options? ")
    while choice:
        if choice.lower().strip() == 'p':
            program_details()
        elif choice.lower().strip() == 'l':
            latest_published_programs()
        elif choice.lower().strip() == 'm':
            menu_options()
        else:
            print(f"Don't know what to do with {choice}.")
        choice = input("[P]rogram details, [l]atest Published Programs or [m]enu Options? ")


def program_details():
    url = 'http://api.sr.se/api/v2/programs?format=json'
    headers = {'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    print(f"Status_code: {r.status_code}")
    response_dict = r.json()
    print(response_dict.keys())
    prog_ids = response_dict['programs']
    print(f"Programs returned: {len(prog_ids)}")
    print("\n---------------------------")
    prog_id = prog_ids[0]
    print(f"\nKeys: {len(prog_id)}")
    for key in sorted(prog_id.keys()):
        print(key)
    print("\n--------------------------------------")
    print("\nSelected information about each program:")
    print("\n--------------------------------------")
    for prog_id in prog_ids:
        print(f"Id:{prog_id['id']}")
        print(f"Name: {prog_id['name']}")
        print(f"Programs lug: {prog_id['programslug']}")
        print(f"Description:{prog_id['description']}")
        print(f"Url:{prog_id['programurl']}")
        print(f"Has ondemand:{prog_id['hasondemand']}")
        print(f"Has pod:{prog_id['haspod']}")
        print(f"Responsible editor:{prog_id['responsibleeditor']}")
        print("\n--------------------------------------")


def latest_published_programs():
    url = 'http://api.sr.se/api/v2/lastpublished?format=json'
    headers = {'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    print(f"Status_code: {r.status_code}")
    print("\n--------------------------------------")
    response_dict = r.json()
    print(response_dict.keys())
    shows_ids = response_dict['shows']
    print(f"Programs returned: {len(shows_ids)}")
    print("\n----------------------------------")
    show_id = shows_ids[0]
    print(f"\nKeys: {len(show_id)}")
    for key in sorted(show_id.keys()):
        print(key)
    print("\n--------------------------------------")
    for show_id in shows_ids:
        print(f"Id:{show_id['id']}")
        print(f"Title: {show_id['title']}")
        print(f"Description:{show_id['description']}")
        end_time = show_id['endtimeutc']
        end_time = re.findall(r'\d+', end_time)
        end_time = datetime.fromtimestamp(int(end_time[0]) / 1000)
        print(end_time  .strftime('%Y-%m-%d - %H:%M:%S'))
        print(f"Type:{show_id['type']}")
        print("\n--------------------------------------")

