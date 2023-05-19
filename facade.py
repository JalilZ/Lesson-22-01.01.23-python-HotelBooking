from Rooms import Rooms as Rooms
from Customers import Customers as Customers
from Bookings import Bookings as Bookings
import functools
import re
import datetime
import string
import json
import csv


def my_decorator(func):
    @functools.wraps(func)
    def wrap_func(*args, **kwargs):
        print('        _______________________________________________'
              '_______________________________________________________')
        func(*args, **kwargs)
        print('        _______________________________________________'
              '_______________________________________________________')
    return wrap_func


@my_decorator
def load_and_read_json():
    """
    Info: a function that loads data from an existing room database
    and dumps it to json file, then displays the data from the json file.
    """

    try:
        open(Rooms.get_rdb_filename(), 'r')

    except FileNotFoundError:
        print('There is no room database in the directory, please add rooms from the main menu.')

    else:

        with open(Rooms.get_rdb_filename(), 'r') as f:
            reader = csv.reader(f)
            next(reader)
            data = []

            for row in reader:
                data.append({'Room ID': row[0],
                             'Size': row[1],
                             'Capacity': row[2],
                             'Number of Beds': row[3],
                             'Room Type': row[4],
                             'Price': row[5]})

        with open('rooms_json.json', 'w') as f:
            json.dump(data, f, indent=4)

        with open('rooms_json.json', 'r') as openfile:
            json_object = json.load(openfile)

        for line in json_object:
            print(line)


@my_decorator
def add_update_room():
    """
    Info: a function that add room / updates an existing room in the room database.
    """
    flag = 1
    dtype = {'1': 'Basic', '2': 'Deluxe', '3': 'Suite'}
    size, capacity, number_of_beds, room_type, price = 'e'*5

    while True:

        custid = input('Enter the ID of the room you would like to add or to update, press e to exit: ')
        if custid == 'e':
            flag *= 0
            break

        elif custid.isdigit():
            break

        else:
            print('Invalid input! a non-negative number is required for a room ID.')
            continue

    while custid != 'e':

        size = input('Enter the size of the room, press e to exit: ')
        if size == 'e':
            flag *= 0
            break

        elif size.isdigit():
            break

        else:
            print('Invalid input! a non-negative number is required for a room size.')
            continue

    while size != 'e':
        capacity = input('Enter the the capacity, press e to exit: ')
        if capacity == 'e':
            flag *= 0
            break

        elif capacity.isdigit():
            break

        else:
            print('Invalid input! a non-negative number is required for a room capacity.')
            continue

    while capacity != 'e':
        number_of_beds = input('Enter number of beds, press e to exit: ')
        if number_of_beds == 'e':
            flag *= 0
            break

        elif number_of_beds.isdigit():
            break

        else:
            print('Invalid input! a non-negative number is required for number of beds.')
            continue

    while number_of_beds != 'e':
        room_type = input('Enter room type; 1 for Basic, 2 for Deluxe or 3 for Suite. press e to exit: ')
        if room_type == 'e':
            flag *= 0
            break

        elif room_type == '1' or room_type == '2' or room_type == '3':
            break

        else:
            print('Invalid input! Enter 1 for Basic, 2 for Deluxe or 3 for Suite.')
            continue

    while room_type != 'e':
        price = input('Enter the price per day, press e to exit: ')
        if price == 'e':
            flag *= 0
            break

        elif price.isdigit():
            break

        else:
            print('Invalid input! a non-negative number is required for price.')
            continue

    if flag == 1:
        Rooms(int(custid), int(size), int(capacity), int(number_of_beds), dtype[room_type], int(price)).update_db()
        print(f'Successfully updated room in the system:\n'
              f'{Rooms(int(custid), int(size), int(capacity), int(number_of_beds), dtype[room_type], int(price)).getter_dic()}')
        print('Returning to main menu.')

    else:
        print('No room was added/updated, Returning to main menu.')


@my_decorator
def add_update_customer():
    """
    Info: a function that add room / updates an existing customer in the room database.
    """
    flag = 1
    name, address, city, email, age = 'e'*5

    while True:

        id = input('Enter the ID of the customer you would like to add or to update, press e to exit: ')
        if id == 'e':
            flag *= 0
            break

        elif id.isdigit():
            break

        else:
            print('Invalid input! a non-negative number is required for a customer ID.')
            continue

    while id != 'e':

        name = input('Enter the name of the customer, press e to exit: ')
        name = name.casefold()
        pattern = "^(?=.{1,40}$)[a-z]+(?:[-'\s][a-z]+)*$"
        if name == 'e':
            flag *= 0
            break

        elif (re.search(pattern, name) != None):
            name = string.capwords(name)                 # CAP first letter of each word
            break

        else:
            print('Invalid input! please use only letters for customer name.')
            continue

    while name != 'e':
        address = input('Enter the the address of the customer, press e to exit: ')

        if address == 'e':
            flag *= 0
            break

        else:
            break

    while address != 'e':
        city = input('Enter city of the customer, press e to exit: ')
        if city == 'e':
            flag *= 0
            break

        else:
            break

    while city != 'e':
        email = input('Enter the email of the customer, press e to exit: ')
        pattern = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        if email == 'e':
            flag *= 0
            break

        elif (re.search(pattern, email) != None):
            break

        else:
            print('Invalid input! enter a legal email.')
            continue

    while email != 'e':
        age = input('Enter the age of the customer, press e to exit: ')
        if age == 'e':
            flag *= 0
            break

        elif age.isdigit() and int(age) >= 18:
            break

        else:
            print('Invalid input! a positive number & legal age (>=18) is required for customers age.')
            continue

    if flag == 1:
        Customers(int(id), name, address, city, email, age).update_db()
        print(f'Successfully updated customer in the system:\n'
              f'{Customers(int(id), name, address, city, email, age).getter_dic()}')
        print('Returning to main menu.')

    else:
        print('No customer was added/updated, returning to main menu.')


@my_decorator
def book_room():
    """
    Info: a function that adds a booking to the booking database.
    """
    flag = 1
    room_id, a_date, d_date, price = 'e' * 4

    while True:

        cust_id = input('Enter the ID of the customer you would like to book a room for, press e to exit: ')
        if cust_id == 'e':
            flag *= 0
            break

        elif cust_id.isdigit():
            break

        else:
            print('Invalid input! a positive number is required for a customer ID.')
            continue

    while cust_id != 'e':

        room_id = input('Enter the ID of the room you would like to book, press e to exit: ')
        if room_id == 'e':
            flag *= 0
            break

        elif room_id.isdigit():
            break

        else:
            print('Invalid input! a non-negative number is required for a room ID.')
            continue

    while room_id != 'e':
        pattern = '^[1-2][0-2][0-9][0-9]-\d{1,2}-\d{1,2}$'
        a_year = input('Enter arrival year (YYYY), press e to exit: ')
        if a_year == 'e':
            flag *= 0
            break
        a_month = input('Enter arrival month (MM), press e to exit: ')
        if a_month == 'e':
            flag *= 0
            break
        a_day = input('Enter arrival day (DD), press e to exit: ')
        if a_day == 'e':
            flag *= 0
            break
        d_year = input('Enter departure year (YYYY), press e to exit: ')
        if d_year == 'e':
            flag *= 0
            break
        d_month = input('Enter departure month (MM), press e to exit: ')
        if d_month == 'e':
            flag *= 0
            break
        d_day = input('Enter departure day (DD) press e to exit: ')
        if d_day == 'e':
            flag *= 0
            break

        str_arrival_date = a_year+'-'+a_month+'-'+a_day
        str_departure_date = d_year + '-' + d_month + '-' + d_day

        if (re.search(pattern, str_arrival_date) != None) and (re.search(pattern, str_departure_date) != None):

            try:
                a = datetime.datetime(int(a_year), int(a_month.lstrip('0')), int(a_day.lstrip('0')))
                b = datetime.datetime(int(d_year), int(d_month.lstrip('0')), int(d_day.lstrip('0')))

            except ValueError:
                print('You have given invalid dates')
                continue

            else:
                if a >= b:
                    print('Departure date must be greater than Arrival Date')
                    continue

            break

        else:
            print('Wrong date format, please try again.')
            continue

    if flag == 1:
        Bookings(int(cust_id), int(room_id), str_arrival_date, str_departure_date).book_room()
        print('Returning to main menu.')
    else:
        print('No booking was made, returning to main menu.')


@my_decorator
def cancel_booking():
    """
    Info: a function removes a booking from the booking database.
    """
    print('See below a list of all bookings:')
    df = Bookings.display_all_bookings()
    for i in range(len(df)):
        x, y = df.loc[i, 'Arrival Date'], df.loc[i, 'Departure Date']
        short_aday = x[:10]
        short_dday = y[:10]
        df.at[i, 'Arrival Date'] = short_aday
        df.at[i, 'Departure Date'] = short_dday
    print(df)

    flag = 1

    while True:
        internal_booking_id = input('Enter the internal ID number of the booking you would like to cancel, '
                                    'or press e to exit: ')
        if internal_booking_id == 'e':
            flag = 0
            break

        elif not internal_booking_id.isdigit():
            print('Invalid input! please enter a non-negative number.')
            continue

        elif internal_booking_id.isdigit():
            Bookings.cancel(int(internal_booking_id))
            break

    if flag == 0:
        print('Returning to main menu')


@my_decorator
def display_rooms():
    """
    Info: displays all rooms in the database.
    """
    print(Rooms.display_all_rooms())
    print('Returning to main menu.')


@my_decorator
def display_customers():
    """
    Info: displays all customers in the database.
    """
    print(Customers.display_all_customers())
    print('Returning to main menu.')


@my_decorator
def display_bookings():
    """
    Info: displays all bookings in the database.
    """
    df = Bookings.display_all_bookings()
    for i in range(len(df)):
        x, y = df.loc[i, 'Arrival Date'], df.loc[i, 'Departure Date']
        short_aday = x[:10]
        short_dday = y[:10]
        df.at[i, 'Arrival Date'] = short_aday
        df.at[i, 'Departure Date'] = short_dday
    print(df)
    print('Returning to main menu.')


@my_decorator
def display_bkd_rooms():
    """
    Info: displays all booked rooms in the database, based on a given Arrival and Departure dates.
    """
    flag = 1

    while True:
        pattern = '^[1-2][0-2][0-9][0-9]-\d{1,2}-\d{1,2}$'
        a_year = input('Enter a specific starting year (YYYY), press e to exit: ')
        if a_year == 'e':
            flag *= 0
            break
        a_month = input('Enter arrival a specific starting month (MM), press e to exit: ')
        if a_month == 'e':
            flag *= 0
            break
        a_day = input('Enter arrival a specific starting day (DD), press e to exit: ')
        if a_day == 'e':
            flag *= 0
            break
        d_year = input('Enter a specific ending year (YYYY), press e to exit: ')
        if d_year == 'e':
            flag *= 0
            break
        d_month = input('Enter a specific ending month (MM), press e to exit: ')
        if d_month == 'e':
            flag *= 0
            break
        d_day = input('Enter a specific ending day (DD) press e to exit: ')
        if d_day == 'e':
            flag *= 0
            break

        str_start_date = a_year+'-'+a_month+'-'+a_day
        str_end_date = d_year + '-' + d_month + '-' + d_day

        if (re.search(pattern, str_start_date) != None) and (re.search(pattern, str_end_date) != None):

            try:
                a = datetime.datetime(int(a_year), int(a_month.lstrip('0')), int(a_day.lstrip('0')))
                b = datetime.datetime(int(d_year), int(d_month.lstrip('0')), int(d_day.lstrip('0')))

            except ValueError:
                print('You have given invalid dates')
                continue

            else:
                if a >= b:
                    print('Filter range should include a Departure Date that is greater than Arrival Date')
                    continue

            break

        else:
            print('Wrong date format, please try again.')
            continue

    if flag == 1:
        print('\nList of booked rooms in the given dates: ')
        print(Bookings.display_booked_rooms(str_start_date, str_end_date))

    else:
        print('Returning to main menu.')


@my_decorator
def display_av_rooms():
    """
    Info: displays all available rooms in the database, based on a given Arrival and Departure dates.
    """
    flag = 1

    while True:
        pattern = '^[1-2][0-2][0-9][0-9]-\d{1,2}-\d{1,2}$'
        a_year = input('Enter a specific starting year (YYYY), press e to exit: ')
        if a_year == 'e':
            flag *= 0
            break
        a_month = input('Enter arrival a specific starting month (MM), press e to exit: ')
        if a_month == 'e':
            flag *= 0
            break
        a_day = input('Enter arrival a specific starting day (DD), press e to exit: ')
        if a_day == 'e':
            flag *= 0
            break
        d_year = input('Enter a specific ending year (YYY), press e to exit: ')
        if d_year == 'e':
            flag *= 0
            break
        d_month = input('Enter a specific ending month (MM), press e to exit: ')
        if d_month == 'e':
            flag *= 0
            break
        d_day = input('Enter a specific ending day (DD) press e to exit: ')
        if d_day == 'e':
            flag *= 0
            break

        str_start_date = a_year+'-'+a_month+'-'+a_day
        str_end_date = d_year + '-' + d_month + '-' + d_day

        if (re.search(pattern, str_start_date) != None) and (re.search(pattern, str_end_date) != None):

            try:
                a = datetime.datetime(int(a_year), int(a_month.lstrip('0')), int(a_day.lstrip('0')))
                b = datetime.datetime(int(d_year), int(d_month.lstrip('0')), int(d_day.lstrip('0')))

            except ValueError:
                print('You have given invalid dates')
                continue

            else:
                if a >= b:
                    print('date range filter should include an ending date that is greater than starting date')
                    continue

            break

        else:
            print('Wrong date format, please try again.')
            continue

    if flag == 1:
        print('\nList of available rooms in the given dates: ')
        print(Bookings.display_available_rooms(str_start_date, str_end_date))

    else:
        print('Returning to main menu.')


@my_decorator
def find_room_by_type():
    """
    Info: displays all rooms of the given type.
    """
    types_d = {'1': 'Basic', '2': 'Deluxe', '3': 'Suite'}
    flag = 1
    while True:
        room_type = input('To find room by type, please enter: '
                          '1 for Basic, 2 for Deluxe and 3 for Suite, or press e to exit: ')
        if room_type == 'e':
            flag = 0
            break

        elif not (room_type == '1' or room_type == '2' or room_type == '3'):
            print('Invalid input! please enter: 1 for Basic, 2 for Deluxe and 3 for Suite.')
            continue

        else:
            print(Rooms.room_by_type(types_d[room_type]))
            break

    if flag == 0:
        print('Returning to main menu')


@my_decorator
def find_room_by_number():
    """
    Info: displays the room attributes of the given room ID.
    """
    flag = 1

    while True:
        roomid = input('Enter the ID of the room you would like to find, press e to exit: ')
        if roomid == 'e':
            flag *= 0
            break

        elif roomid.isdigit():
            break

        else:
            print('Invalid input! a non-negative number is required for a room ID.')
            continue

    if flag == 1:
        print(Rooms.room_by_number(int(roomid)))

    else:
        print('Returning to main menu.')


@my_decorator
def find_cust_by_name():
    """
    Info: displays the attributes of all customers of a given name.
    """
    flag = 1

    while True:
        name = input('Enter the name of the customer, press e to exit: ')
        name = name.casefold()
        pattern = "^(?=.{1,40}$)[a-z]+(?:[-'\s][a-z]+)*$"
        if name == 'e':
            flag *= 0
            break

        elif (re.search(pattern, name) != None):
            name = string.capwords(name)
            break

        else:
            print('Invalid input! please use only letters for customer name.')
            continue

    if flag == 1:
        for i in Customers.customer_by_name(name):
            print(i)
    else:
        print('Returning to main menu.')


@my_decorator
def remove_room():
    """
    Info: removes a room from the rooms database based on the given room ID.
    Also removes related bookings from the booking database that are booked under the given room ID.
    """
    flag = 1
    while True:
        roomid = input('Enter the room ID you would like to remove, press e to exit: ')
        if roomid == 'e':
            flag = 0
            break

        elif not roomid.isdigit():
            print('Invalid input! please enter a non-negative number.')
            continue

        elif roomid.isdigit():
            Rooms.remove(int(roomid))
            break

    if flag == 0:
        print('Returning to main menu')


@my_decorator
def remove_customer():
    """
    Info: removes a customer from the customers database based on the given customer ID.
    Also removes related bookings from the booking database that are booked under the given customer ID.
    """
    flag = 1
    while True:
        customerid = input('Enter the customer ID you would like to remove, press e to exit: ')
        if customerid == 'e':
            flag = 0
            break

        elif not customerid.isdigit():
            print('Invalid input! please enter a non-negative number.')
            continue

        elif customerid.isdigit():
            Customers.remove(int(customerid))
            break

    if flag == 0:
        print('Returning to main menu')


def main_menu():
    action = None
    menu = {'1': load_and_read_json,
            '2': add_update_room,
            '3': add_update_customer,
            '4': book_room,
            '5': cancel_booking,
            '6': display_rooms,
            '7': display_customers,
            '8': display_bookings,
            '9': display_bkd_rooms,
            '10': display_av_rooms,
            '11': find_room_by_type,
            '12': find_room_by_number,
            '13': find_cust_by_name,
            '14': remove_room,
            '15': remove_customer}

    while action != 'q':

        print("""
        ______________________________________________________________________________________________________
                                           <<Hotel Management System>>
        Menu of actions:
        
        [1]    Load rooms                  [6]    Display all rooms               [11]   Find rooms by type
        [2]    Add/Update room             [7]    Display all customers           [12]   Find room by number
        [3]    Add/Update customer         [8]    Display all bookings            [13]   Find customers by name
        [4]    Book a room                 [9]    Display booked rooms            [14]   Remove a room
        [5]    Cancel a booking            [10]   Display available rooms         [15]   Remove a customer
        ______________________________________________________________________________________________________
        """)
        action = input('Please enter the number of the operation you would like to perform, or press q to quit: ')

        if action == 'q':
            print('Goodbye!')
            break

        elif (action.isdigit() and int(action) <= 15 and int(action) >= 1):
            menu[action]()

        else:
            print('Invalid input! please enter a number of an action as detailed in the main menu.')
            continue


if __name__ != '__main__':
    main_menu()
