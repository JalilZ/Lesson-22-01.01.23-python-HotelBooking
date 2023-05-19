import pandas as pd


class Rooms:

    _rdbFileName = 'Rooms1.csv'
    _rcolumn_names = ['ID', 'Size', 'Capacity', 'Number of Beds', 'Room Type', 'Price']

    _bdbFileName = 'Bookings1.csv'

    def __init__(self, room_id: int, size: int, capacity: int, number_of_beds: int, room_type: str, price: int):
        self._id = room_id
        self._size = size
        self._capacity = capacity
        self._number_of_beds = number_of_beds
        self._room_type = room_type
        self._price = price

    @staticmethod
    def existing_db():
        """
        Info: Checks if we already have an existing DB for this Class, if not; a new blank DB will be created.
        And finally returns the database.
        """

        try:
            open(Rooms._rdbFileName, 'r')
        except FileNotFoundError:
            database = pd.DataFrame(columns=Rooms._rcolumn_names)
            database.to_csv(Rooms._rdbFileName, index=False)

        finally:
            database = pd.read_csv(Rooms._rdbFileName)

        return database

    def update_db(self):
        """
        Info: This function is used to instantiate a new room object and to update the database for Rooms Class.
        """

        room_ls = \
            [
                self._id,
                self._size,
                self._capacity,
                self._number_of_beds,
                self._room_type,
                self._price
            ]

        rdb = Rooms.existing_db()                        # read the Rooms class database

        if rdb.empty:                                    # if empty, start writing
            rdb.loc[len(rdb)] = room_ls
            rdb.to_csv(Rooms._rdbFileName, index=False)

        else:                                            # if room ID already exists, update the existing record.
            check_id = rdb['ID'].isin([self._id]).any()
            if check_id:
                rdb.loc[rdb['ID'] == self._id, Rooms._rcolumn_names[1::]] = room_ls[1::]
                rdb.to_csv(Rooms._rdbFileName, index=False)

            else:                                        # if room ID does not exist, make a new record.
                rdb.loc[len(rdb)] = room_ls
                rdb.to_csv(Rooms._rdbFileName, index=False)

    # Why I Chose not to use @x.deleter or to modify __del__:
    # Since I am directly working with a database, I will not assign variables to my instantiated rooms (useless)
    # the Rooms database csv file will serve as memory for my program.

    @staticmethod
    def remove(roomid):
        """
        Info: a static class method to remove a room with the given ID from the Rooms database.
        Also removes related bookings made under the room ID that is being removed.
        """

        rdb = Rooms.existing_db()                   # read the Rooms class database, creates empty one if we have no DB

        if rdb.empty:
            print('There are no rooms in the system to remove, new rooms can be added in the main menu.')
        else:
            if not rdb['ID'].isin([roomid]).any():
                print(f'We don\'t have a room with ID {roomid} in our system!')
            else:
                print(f'Room {roomid} was removed.')
                rdb = rdb[rdb['ID'] != roomid]
                rdb.to_csv(Rooms._rdbFileName, index=False)

        try:
            bdb = pd.read_csv(Rooms._bdbFileName)
        except FileNotFoundError:
            pass
        else:
            bdb = bdb[bdb['RoomID'] != roomid]
            bdb.to_csv(Rooms._bdbFileName, index=False)

    def setter(self, size: int, capacity: int, number_of_beds: int, room_type: str, price: int):
        """Info: a method that updates the attributes of a room object
         and updates the existing record id in the Rooms database.
        """
        self._size = size
        self._capacity = capacity
        self._number_of_beds = number_of_beds
        self._room_type = room_type
        self._price = price
        self.update_db()

    # If the user needs to get the value of a room object then he can get it ONLY as a dictionary of all attributes,
    # therefore I did not use @property (returning each self._attribute is useless)
    def getter_dic(self):
        return {'ID': self._id, 'Size': self._size, 'Capacity': self._capacity,
                'Number of Beds': self._number_of_beds, 'Room Type': self._room_type, 'Price': self._price}

    def __str__(self):
        return f'Room ID number: {self._id}, Room size: {self._size}, Room capacity: {self._capacity},' \
               f' Number of Beds: {self._number_of_beds}, Room type: {self._room_type}, Room price: {self._price}'

    @staticmethod
    def room_by_type(room_type: str):
        """Info: a method that takes a given room type as a parameter and returns
        database of all rooms from the database with the same given room type.
        """

        rdb = Rooms.existing_db()

        if room_type == 'Basic':
            rdb = rdb[rdb['Room Type'] == 'Basic']

        elif room_type == 'Deluxe':
            rdb = rdb[rdb['Room Type'] == 'Deluxe']
        else:
            rdb = rdb[rdb['Room Type'] == 'Suite']

        return rdb

    @staticmethod
    def display_all_rooms():
        rdb = Rooms.existing_db()
        if rdb.empty:
            rdb.to_csv(Rooms._rdbFileName, index=False)

        return rdb

    @staticmethod
    def room_by_number(room_id: int):
        """Info: a method that takes a given room number from the database as a parameter and
        instantiate a room object.
        """

        rdb = Rooms.existing_db()
        find_room_id = rdb['ID'].isin([room_id]).any()
        if find_room_id:
            rdb = rdb[rdb['ID'] == room_id]
            row = rdb.iloc[0]
            room_object = Rooms(row[0], row[1], row[2], row[3], row[4], row[5])
            return room_object
        else:
            print(f'No room with the given ID {room_id} was found in the system.')

    @staticmethod
    def get_rdb_filename():
        r_filename = Rooms._rdbFileName
        return r_filename
