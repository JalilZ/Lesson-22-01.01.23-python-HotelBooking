1. attached 3 csv filles (Rooms1.csv, Cust1.csv, Bookings1.csv), each file includes relevant data table
2. hotelcli.py can run without the above mentioned files (3 empty files will be created accordingly (similar names) in the same directory of this project)
3. for each entity I created a class (separate module for each class)
4. a testing.py was created for each module
5. since the created objects need to be saved in the data tables, most class methods are staticmethods (No point in insantiating object each time I call a method)
6. in facade.py I created all the functions that takes input & validates it from the user, the order of these functions and the Menue of actions is ordered in the same order of the actions requested in the homework assignment (section 4)