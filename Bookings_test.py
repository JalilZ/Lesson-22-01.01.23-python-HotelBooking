from Bookings import Bookings
from Rooms import Rooms
from Customers import Customers
import os
from datetime import datetime


def test_existing_db():
    """
    info: checks that we always have a bookings database in the directory.
    """
    Bookings.existing_db(Bookings._bdbFileName, Bookings._bcolumn_names)
    filename = Bookings.get_bdb_filename()
    directory = os.getcwd()
    in_directory = os.listdir(directory)
    if filename in in_directory:
        assert True
    else:
        raise AssertionError


def test_book():
    """
    info: test that bookings instantiated are stored in database.
    """
    customer_id = 2402
    Customers(2402, 'Jimmy Rice', 'Suite 250', 'Portland', 'Jimmy@gmail.com', 25).update_db()
    room_id = 1997
    Rooms(room_id, 35, 1, 1, 'Suite', 500).update_db()
    Bookings(customer_id, room_id, '2023-03-01', '2023-03-04').book_room()

    bdb = Bookings.existing_db(Bookings._bdbFileName, Bookings._bcolumn_names)

    assert bdb['CustID'].isin([customer_id]).any() and bdb['RoomID'].isin([room_id]).any()


def test_cancel_booking():
    """
    info: test that booking is removed from database accordingly.
    """
    book_internal_id = 7601575  # for testing purpose please use the internal ID of the booking generated in test_book()
    Bookings.cancel(7601575)
    bdb = Bookings.existing_db(Bookings._bdbFileName, Bookings._bcolumn_names)

    assert not bdb['BookInternalID'].isin([book_internal_id]).any()


def test_display_bkd_rooms():
    """
    Info: test that booked rooms are displayed according to arrival and end date given to the function.
    """

    customer_id = 2402
    Customers(2402, 'Jimmy Rice', 'Suite 250', 'Portland', 'Jimmy@gmail.com', 25).update_db()
    room_id = 1997
    Rooms(room_id, 35, 1, 1, 'Suite', 500).update_db()
    Bookings(customer_id, room_id, '2027-03-10', '2027-03-15').book_room()

    start_date = '2027-03-01'
    end_date = '2027-03-12'
    a = datetime.strptime(start_date, '%Y-%m-%d')
    b = datetime.strptime(end_date, '%Y-%m-%d')
    bkd_rooms = Bookings.display_booked_rooms(start_date, end_date)
    check_start = bkd_rooms['Arrival Date'].between(a, b)
    check_end = bkd_rooms['Departure Date'].between(a, b)
    list1 = list()
    list2 = list()
    for i in check_start:
        if i is True:
            list1.append(1)
        else:
            list1.append(0)
    for i in check_end:
        if i is True:
            list2.append(1)
        else:
            list2.append(0)
    check_list = [x + y for x, y in zip(list1, list2)]

    # if one element is zero in the check_list, then the test fails (meaning the given
    # start date and end date is not within the arrival and departure date of booking in the database)
    for element in check_list:
        if element == 0:
            raise AssertionError
    else:
        assert True


def test_available_rooms():

    start_date = '2020-01-01'
    end_date = '2027-03-12'

    bkd_rooms = Bookings.display_booked_rooms(start_date, end_date)
    av_rooms = Bookings.display_available_rooms(start_date, end_date)

    # there should not be similar room ID between booked database and available database for the same given dates.
    v = bkd_rooms['RoomID'].isin(av_rooms['ID'])
    for i in v:
        if i is False:

            assert True
        else:
            raise AssertionError


def run_room_tests():
    test_existing_db()
    test_book()
    test_cancel_booking()  # booking cancellation is made through the booking internal id
    test_display_bkd_rooms()
    test_available_rooms()


run_room_tests()
