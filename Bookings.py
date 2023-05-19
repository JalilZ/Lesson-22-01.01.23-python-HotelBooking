import pandas as pd
from datetime import datetime, timedelta
import random


class Bookings:

    _cdbFileName = 'Cust1.csv'
    _ccolumn_names = ['ID', 'Name', 'Address', 'City', 'Email', 'Age']
    _rdbFileName = 'Rooms1.csv'
    _rcolumn_names = ['ID', 'Size', 'Capacity', 'Number of Beds', 'Room Type', 'Price']

    _bdbFileName = 'Bookings1.csv'
    _bcolumn_names = ['BookInternalID', 'CustID', 'RoomID', 'Arrival Date', 'Departure Date', 'Total Price']

    def __init__(self, cust_id: int, room_id: int, arrival_date: 'y-m-d', departure_date: 'y-m-d'):
        self._cust_id = cust_id
        self._room_id = room_id
        self._aday = datetime.strptime(arrival_date, '%Y-%m-%d')
        self._dday = datetime.strptime(departure_date, '%Y-%m-%d')
        self._nights = self._dday - self._aday
        self._tprice = 'book a room for final price'
        self.book_ls = \
            [
                self._cust_id,
                self._room_id,
                self._aday,  # did not remove hours minutes to keep it a date type object instead of str
                self._dday,
                self._tprice  # date object, using .days display only amount without days
            ]

    @staticmethod
    def existing_db(filename, columns):
        """
        Info: Checks if we already have an existing DB, if not; a new blank DB will be created.
        And finally returns the database.
        """

        try:
            open(filename, 'r')
        except FileNotFoundError:
            database = pd.DataFrame(columns=columns)
            database.to_csv(filename, index=False)

        finally:
            database = pd.read_csv(filename)

        return database

    @staticmethod
    def gen_internal_id():
        """
        Info: Generates a unique Internal ID Number for each booking.
        """

        bdb = Bookings.existing_db(Bookings._bdbFileName, Bookings._bcolumn_names)
        used_booking_id = set(bdb['BookInternalID'])
        x = random.randint(1000000, 9999999)

        while x in used_booking_id:
            x = random.randint(1000000, 9999999)

        return x

    def book_room(self):
        """
        Info: a method that adds a booking to our Bookings database.
        """

        # open existing / create empty databases
        rdb = Bookings.existing_db(Bookings._rdbFileName, Bookings._rcolumn_names)
        cdb = Bookings.existing_db(Bookings._cdbFileName, Bookings._ccolumn_names)
        bdb = Bookings.existing_db(Bookings._bdbFileName, Bookings._bcolumn_names)

        check_cust_id = cdb['ID'].isin([self._cust_id]).any()      # Boolean
        check_id = rdb['ID'].isin([self._room_id]).any()           # Boolean

        if not check_cust_id:                                      # scenario1: customer does not exist
            print('We don\'t have this customer in our system, please create a customer first.')

        elif not check_id:                                         # scenario2: room does not exist
            print('We don\'t have this room in our system, please create a room first.')

        elif check_id:                                             # scenario3: customer & room exists
            get_type = rdb.loc[rdb['ID'] == self._room_id, 'Room Type'].values[0]

            if self._nights < timedelta(days=2) and get_type == 'Deluxe':
                # scenario3.1: Deluxe nights < 2
                print('You are trying to book a Deluxe room which required at least 2 '
                      'nights stay, booking was not processed.')

            elif self._nights < timedelta(days=3) and get_type == 'Suite':
                # scenario3.2: Suite nights < 3
                print('You are trying to book a Suite room which required at least 3 '
                      'nights stay, booking was not processed.')

            elif self._room_id not in bdb['RoomID'].values:
                # scenario3.3: room ID does not exist in our Bookings database >> safe to add without further checks.

                # calculate price (86400 are seconds in a day)
                self._price = rdb[rdb['ID'] == self._room_id]['Price'].iloc[0]
                self._tprice = self._price * self._nights.total_seconds() / 86400

                # generate Unique Booking Internal ID
                internal_id = Bookings.gen_internal_id()
                tmp_ls = list()
                tmp_ls.append(internal_id)
                tmp_ls += [self._cust_id, self._room_id, self._aday, self._dday, self._tprice]
                bdb.loc[len(bdb)] = tmp_ls
                bdb.to_csv(Bookings._bdbFileName, index=False)
                print('Booking Completed.')

            else:
                # scenario3.4: room ID does exist in our Bookings database >> locate collision database

                # copy database to avoid 'SettingWithCopyWarning' panda warning of modifying the original database.
                temp_bdb = bdb[bdb['RoomID'] == self._room_id].copy()

                # convert data to 'datetime' objects
                temp_bdb['Arrival Date'] = pd.to_datetime(temp_bdb['Arrival Date'])
                temp_bdb['Departure Date'] = pd.to_datetime(temp_bdb['Departure Date'])

                collision = temp_bdb[temp_bdb['Arrival Date'].between(self._aday, self._dday)
                                     | temp_bdb['Departure Date'].between(self._aday, self._dday)]

                if not collision.empty:
                    # Collision was found.
                    print('\n**************************************************************************')
                    print('This booking collides with other bookings as detailed below:')
                    print(collision)
                    print('Booking was not processed.')
                    print('**************************************************************************\n')

                else:
                    # Collision was not found >> add booking.
                    # calculate price
                    self._price = rdb[rdb['ID'] == self._room_id]['Price'].iloc[0]
                    self._tprice = self._price * self._nights.total_seconds() / 86400

                    # generate Unique Booking Internal ID
                    internal_id = Bookings.gen_internal_id()
                    tmp_ls = list()
                    tmp_ls.append(internal_id)
                    tmp_ls += [self._cust_id, self._room_id, self._aday, self._dday, self._tprice]
                    bdb.loc[len(bdb)] = tmp_ls
                    bdb.to_csv(Bookings._bdbFileName, index=False)
                    print('Booking Completed.')

    # Why I did not use @x.deleter or __del__ and why I used a static method: see explanation in Rooms class
    @staticmethod
    def cancel(internalid):
        """
        Info: a static class method to remove a booking with the given Booking Internal ID from the Bookings database.
        """

        bdb = Bookings.existing_db(Bookings._bdbFileName, Bookings._bcolumn_names)
        check_bk_internal_id = bdb['BookInternalID'].isin([internalid]).any()
        if not check_bk_internal_id:                                      # scenario1: customer does not exist
            print(f'We don\'t have a booking with internal ID {internalid} in our system!')
        else:
            print(f'Booking {internalid} was removed.')
            bdb = bdb[bdb['BookInternalID'] != internalid]
            bdb.to_csv(Bookings._bdbFileName, index=False)

    @staticmethod
    def display_all_bookings():
        """
        Info: a static class method that returns the full Bookings database.
        """

        bdb = Bookings.existing_db(Bookings._bdbFileName, Bookings._bcolumn_names)
        if bdb.empty:
            bdb.to_csv(Bookings._bdbFileName, index=False)
        return bdb

    @staticmethod
    def display_booked_rooms(start_date, end_date):
        """
        Info: a static class method that returns Bookings database filtered by Arrival Date and Departure Date.
        """

        bdb = Bookings.existing_db(Bookings._bdbFileName, Bookings._bcolumn_names)
        a = datetime.strptime(start_date, '%Y-%m-%d')
        b = datetime.strptime(end_date, '%Y-%m-%d')

        bkd_rooms = bdb.copy()
        bkd_rooms['Arrival Date'] = pd.to_datetime(bkd_rooms['Arrival Date'])
        bkd_rooms['Departure Date'] = pd.to_datetime(bkd_rooms['Departure Date'])

        booked = bkd_rooms[bkd_rooms['Arrival Date'].between(a, b) | bkd_rooms['Departure Date'].between(a, b)]

        return booked

    @staticmethod
    def display_available_rooms(start_date, end_date):
        """
        Info: a static class method that returns available Rooms database based on given dates.
        """

        rdb = Bookings.existing_db(Bookings._rdbFileName, Bookings._rcolumn_names)
        booked = Bookings.display_booked_rooms(start_date, end_date)
        av_room = rdb.copy()

        for i in booked['RoomID']:
            av_room = av_room[av_room['ID'] != i]

        return av_room

    @staticmethod
    def get_bdb_filename():
        b_filename = Bookings._bdbFileName
        return b_filename

