from Customers import Customers
from Rooms import Rooms
from Bookings import Bookings
import os


def test_existing_db():
    """
    info: checks that we always have a customers database in the directory.
    """
    Customers.existing_db()
    filename = Customers.get_cdb_filename()
    directory = os.getcwd()
    in_directory = os.listdir(directory)
    if filename in in_directory:
        assert True
    else:
        raise AssertionError


def test_create_customer():
    """
    info: test that customers instantiated are stored in database.
    """
    customer_id = 2200
    Customers(2200, 'Harry Kimmel', 'Suite 250', 'Dufftown', 'harry@gmail.com', 25).update_db()
    cdb = Customers.existing_db()
    check_id = cdb['ID'].isin([customer_id]).any()
    assert check_id


def test_remove_customer():
    """
    info: test that customer is removed from customers database and from bookings database if a booking
    was made under the removed customer.
    """
    room_id = 1200
    customer_id = 2300
    Rooms(room_id, 40, 2, 2, 'Deluxe', 1000).update_db()
    Customers(customer_id, 'Ed Jackson', 'Avenue 300', 'New Port', 'ed@gmail.com', 30).update_db()
    Bookings(customer_id, room_id, '2025-01-01', '2025-01-04').book_room()
    Customers.remove(customer_id)
    cdb = Customers .existing_db()
    bdb = Bookings.existing_db(Bookings._bdbFileName, Bookings._bcolumn_names)
    check_id = cdb['ID'].isin([customer_id]).any()
    check_id_inbooking = bdb['CustID'].isin([customer_id]).any()
    assert not (check_id and check_id_inbooking)


def test_customer_by_name():
    """
    info: test that database is filtered according to name given.
    """
    given_name = 'John Lester'
    Customers(2400, given_name, 'Avenue 200', 'New Port', 'John@gmail.com', 30).update_db()
    customers_name_list = Customers.customer_by_name(given_name)
    for i in customers_name_list:
        if i.getter_dic()['Name'] == given_name:
            assert True
        else:
            raise AssertionError


def test_getter_setter():
    """
    info: testing getter and setter
    """
    customer_id = 2401
    customer1 = Customers(customer_id, 'Audrey Hicks', 'Ave 199', 'Sea road', 'audrey@yahoo.com', 30)
    customer1.setter('Audrey Hicks', 'Ave 201', 'Pike Creek', 'audrey@yahoo.com', 40)

    assert customer1.getter_dic()['ID'] == customer_id
    assert customer1.getter_dic()['Name'] == 'Audrey Hicks'
    assert customer1.getter_dic()['Address'] == 'Ave 201'
    assert customer1.getter_dic()['City'] == 'Pike Creek'
    assert customer1.getter_dic()['Email'] == 'audrey@yahoo.com'
    assert customer1.getter_dic()['Age'] == 40


def run_room_tests():
    test_existing_db()
    test_create_customer()
    test_remove_customer()
    test_customer_by_name()
    test_getter_setter()


run_room_tests()
