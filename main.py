import functions


def menu_options():
    print("----------")
    print("1 - List Stations")
    print("2 - Search for Program")
    print("0 - Exit")
    print("----------")
    user_input = input()
    if user_input == "1":
        functions.get_channels()
    if user_input == "2":
        functions.search_for_program()
    # Other function options
    return user_input


if __name__ == '__main__':
    print("Checking for Important Public Announcements...")
    functions.check_for_alerts()
    user_input = menu_options()
    while user_input != '0' and user_input.upper() != 'EXIT':
        user_input = menu_options()
    print("Exiting Program")
