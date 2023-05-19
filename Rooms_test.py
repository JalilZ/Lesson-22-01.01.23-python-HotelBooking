from Rooms import Rooms
from Bookings import Bookings
from Customers import Customers
import os


def test_existing_db():
    """
    info: checks that we always have a rooms database in the directory.
    """
    Rooms.existing_db()
    filename = Rooms.get_rdb_filename()
    directory = os.getcwd()
    in_directory = os.listdir(directory)
    if filename in in_directory:
        assert True
    else:
        raise AssertionError


def test_create_room():
    """
    info: test that rooms instantiated are stored in database.
    """
    room_id = 1200
    Rooms(room_id, 30, 2, 1, 'Basic', 200).update_db()
    rdb = Rooms.existing_db()
    check_id = rdb['ID'].isin([room_id]).any()
    assert check_id


def test_remove_room():
    """
    info: test that room is removed from rooms database and from bookings database if a booking
    was made under the removed room.
    """
    room_id = 1200
    customer_id = 2300         # create also a customer that booked the room to be removed (testing also that customer)
    Rooms(room_id, 40, 2, 2, 'Deluxe', 1000).update_db()  # update existing room we created in the previous test
    Customers(customer_id, 'Mike Sterling', 'Street 500', 'Brooklyn', 'mike@gmail.com', 50).update_db()
    Bookings(customer_id, room_id, '2024-01-01', '2024-01-04').book_room()
    Rooms.remove(room_id)
    rdb = Rooms.existing_db()
    bdb = Bookings.existing_db(Bookings._bdbFileName, Bookings._bcolumn_names)
    check_id = rdb['ID'].isin([room_id]).any()
    check_id_inbooking = bdb['RoomID'].isin([room_id]).any()
    assert not (check_id and check_id_inbooking)


def test_room_by_type():
    """
    info: test that database is filtered according to type given.
    """
    basic_rooms_db = Rooms.room_by_type('Basic')
    deluxe_rooms_db = Rooms.room_by_type('Deluxe')
    suite_rooms_db = Rooms.room_by_type('Suite')

    assert not basic_rooms_db['Room Type'].isin(['Deluxe', 'Suite']).any() and not \
           deluxe_rooms_db['Room Type'].isin(['Basic', 'Suite']).any() and not \
           suite_rooms_db['Room Type'].isin(['Deluxe', 'Basic']).any()


def test_getter_setter():
    """
    info: testing getter and setter
    """
    room_id = 1999
    room1 = Rooms(room_id, 50, 1, 1, 'Basic', 40)
    room1.setter(51, 2, 2, 'Suite', 40)

    assert room1.getter_dic()['ID'] == room_id
    assert room1.getter_dic()['Size'] == 51
    assert room1.getter_dic()['Capacity'] == 2
    assert room1.getter_dic()['Number of Beds'] == 2
    assert room1.getter_dic()['Room Type'] == 'Suite'
    assert room1.getter_dic()['Price'] == 40


def test_room_by_number():
    """
    info: test that database is filtered according to room ID given.
    """
    given_id = 1998
    Rooms(given_id, 30, 1, 1, 'Basic', 30).update_db()
    room_number = Rooms.room_by_number(given_id)
    assert room_number.getter_dic()['ID'] == given_id


def run_room_tests():
    test_existing_db()
    test_create_room()
    test_remove_room()
    test_room_by_type()
    test_getter_setter()
    test_room_by_number()


run_room_tests()
