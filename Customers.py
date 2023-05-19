import pandas as pd


class Customers:

    _cdbFileName = 'Cust1.csv'
    _ccolumn_names = ['ID', 'Name', 'Address', 'City', 'Email', 'Age']

    _bdbFileName = 'Bookings1.csv'

    def __init__(self, cust_id: int, name: str, address: str, city: str, email: str, age: int):
        self._id = cust_id
        self._name = name
        self._address = address
        self._city = city
        self._email = email
        self._age = age

    @staticmethod
    def existing_db():
        """
        Info: Checks if we already have an existing DB for this Class, if not; a new blank DB will be created.
        And finally returns the database.
        """

        try:
            open(Customers._cdbFileName, 'r')
        except FileNotFoundError:
            database = pd.DataFrame(columns=Customers._ccolumn_names)
            database.to_csv(Customers._cdbFileName, index=False)

        finally:
            database = pd.read_csv(Customers._cdbFileName)

        return database

    def update_db(self):
        """
        Info: This function is used to instantiate a new customer object and to update the database for Customers Class.
        """
        cust_ls = \
            [
                self._id,
                self._name,
                self._address,
                self._city,
                self._email,
                self._age
            ]

        cdb = Customers.existing_db()                        # read the Customers class database

        if cdb.empty:                                        # if empty, start writing
            cdb.loc[len(cdb)] = cust_ls
            cdb.to_csv(Customers._cdbFileName, index=False)

        else:
            check_id = cdb['ID'].isin([self._id]).any()
            if check_id:
                cdb.loc[cdb['ID'] == self._id, Customers._ccolumn_names[1::]] = cust_ls[1::]
                cdb.to_csv(Customers._cdbFileName, index=False)

            else:                                        # if customer ID does not exist, make a new record.
                cdb.loc[len(cdb)] = cust_ls
                cdb.to_csv(Customers._cdbFileName, index=False)

    # Why I did not use @x.deleter or __del__ and why I used a static method: see explanation in Rooms class
    @staticmethod
    def remove(customerid):
        """
        Info: a static class method to remove a customer with the given ID from the Customers database.
        Also removes related bookings made under the customer ID that is being removed.
        """

        cdb = Customers.existing_db()

        if cdb.empty:
            print('There are no customers in the system to remove, new customers can be added in the main menu.')
        else:
            if not cdb['ID'].isin([customerid]).any():
                print(f'We don\'t have a customer with ID {customerid} in our system!')
            else:
                print(f'Customer {customerid} was removed.')
                cdb = cdb[cdb['ID'] != customerid]
                cdb.to_csv(Customers._cdbFileName, index=False)

        try:
            bdb = pd.read_csv(Customers._bdbFileName)
        except FileNotFoundError:
            pass
        else:
            bdb = bdb[bdb['CustID'] != customerid]
            bdb.to_csv(Customers._bdbFileName, index=False)

    def setter(self, name: str, address: str, city: str, email: str, age: int):
        """Info: a method that updates the attributes of a customer object
        and updates the existing record id in the Customers database.
        """
        self._name = name
        self._address = address
        self._city = city
        self._email = email
        self._age = age
        self.update_db()

    # If the user needs to get the value of a customer object then he can get it ONLY as a dictionary of all attributes,
    # therefore I did not use @property (returning each self._attribute is useless)
    def getter_dic(self):
        return {'ID': self._id, 'Name': self._name, 'Address': self._address,
                'City': self._city, 'Email': self._email, 'Age': self._age}

    def __str__(self):
        return f'Customer ID number: {self._id}, Customer Name: {self._name}, Address: {self._address},' \
               f' City: {self._city}, Email: {self._email}, Age: {self._age}'

    @staticmethod
    def display_all_customers():
        cdb = Customers.existing_db()
        if cdb.empty:
            cdb.to_csv(Customers._cdbFileName, index=False)

        return cdb

    @staticmethod
    def customer_by_name(cust_name: str):
        """Info: a method that takes a given customer name from the database as a parameter and instantiates
        the customer object/objects (each as an element in a list)
        """

        cdb = Customers.existing_db()
        find_cust_name = cdb['Name'].isin([cust_name]).any()
        cust_obj_ls = list()

        if find_cust_name:
            cdb = cdb[cdb['Name'] == cust_name]
            for i in range(len(cdb)):    # in case we have different customers (different ID's) with similar names.
                row = cdb.iloc[i]
                cust_obj = Customers(row[0], row[1], row[2], row[3], row[4], row[5])
                cust_obj_ls.append(cust_obj)

            return cust_obj_ls
        else:
            cust_obj_ls = [f'No customer with the given name {cust_name} was found in the system.']
            return cust_obj_ls

    @staticmethod
    def get_cdb_filename():
        c_filename = Customers._cdbFileName
        return c_filename
