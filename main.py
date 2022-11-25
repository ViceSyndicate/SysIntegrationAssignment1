#https://api.sr.se/api/documentation/v2/index.html
#https://api.sr.se/api/documentation/v2/generella_parametrar.html
#https://api.sr.se/api/documentation/v2/metoder/kanaler.html
#https://api.sr.se/api/documentation/v2/metoder/kanaler.html
import functions
import functions1



def menu_options():
    print("----------")
    print("0 - Exit")
    print("1 - List Stations")
    print("2 - Search for Program")
    print("3 - Extra Programs")
    print("4 - list traffic messages")
    print("----------")

    user_input = input()
    if user_input == "0":
        print("Exiting Program")
        exit()
    elif user_input == "1":
        functions.get_channels()
    elif user_input == "2":
        functions.search_for_program()
    elif user_input == "3":
        functions1.my_menu()
    elif user_input == "4":
        functions1.traffic_menue()
    # Other function options
    return user_input


if __name__ == '__main__':
    print("Checking for Important Public Announcements...")
   # functions.check_for_alerts()
    user_input = menu_options()
    while user_input != '0' and user_input.upper() != 'EXIT':
        user_input = menu_options()
    print("Exiting Program")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

