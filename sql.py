import sqlite3
import hashlib
import pandas as pd

class SQL:
    """
    SQL class to manage database operations for a hotel management system.
    """
    def __init__(self):
        """ Initializes the SQL class, connects to the database, and creates a default password if it doesn't exist.
        """
        self.Total_rooms = 50  # Set total number of rooms to 50
        try:
            self.con = sqlite3.connect("database.db")  # Attempt to connect to the SQLite database
            self.create_tables()
            self.create_password()                     # Call method to create password (or setup)
        except:
            raise FileNotFoundError                    # Raise error if database file not found or connection fails

    def create_tables(self):
        """ Creates necessary tables in the database if they do not already exist.
            This includes tables for Rooms, Reservations, Customers, Passwords, and Tasks.
        """
        cursor = self.con.cursor()
        # Create Rooms table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `Rooms` (
                `roomID` TEXT PRIMARY KEY UNIQUE NOT NULL, 
                `roomType` TEXT NOT NULL, 
                `price` REAL NOT NULL, 
                `status` TEXT NOT NULL)
        """)
        self.populate_rooms()
        # Create Customers table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `Customers` (
                `customerID` TEXT PRIMARY KEY UNIQUE NOT NULL, 
                `firstName` TEXT NOT NULL, 
                `age` INTEGER NOT NULL, 
                `lastName` TEXT NOT NULL, 
                `email` TEXT NOT NULL, 
                `phoneNumber` INTEGER UNIQUE NOT NULL)
        """)
        # Create Reservations table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `Reservations` (
                `reservationID` TEXT PRIMARY KEY UNIQUE NOT NULL, 
                `guestID` TEXT REFERENCES `Customers`(`customerID`), 
                `roomID` TEXT REFERENCES `Rooms`(`roomId`), 
                `check_in` TEXT, `check_out` TEXT, 
                `status` TEXT DEFAULT 'Pending')
        """)
        # Create Password table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `Password` (
                `Password_Number` TEXT PRIMARY KEY UNIQUE NOT NULL, 
                `Hashed_Password` TEXT NOT NULL)
        """)
        # Create Tasks table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `Tasks` (
                `description` TEXT NOT NULL, 
                `createdAt` TEXT NOT NULL, 
                `dueDate` TEXT NOT NULL, 
                `status` TEXT DEFAULT 'Pending')
        """)
        
    def populate_rooms(self):
        """ Populates the Rooms table with predefined room groups.
            Each group has a prefix, count, type, price, and status.
            This method inserts rooms into the database if they do not already exist.
        """
         # Create a cursor to execute SQL queries
        cursor = self.con.cursor()
    
        # Define room groups as tuples: (prefix, count, type, price, status)
        room_groups = [
            ("A", 12, "Standard", 50, "Available"),
            ("B", 11, "Deluxe", 75, "Available"),
            ("C", 10, "Executive", 125, "Available"),
            ("D", 9,  "Suit", 250, "Available"),
            ("E", 8,  "Predential Suite", 445, "Available")
        ]
        # Insert each room into the Rooms table
        for prefix, count, room_type, price, status in room_groups:
            for i in range(1, count + 1):
                room_id = f"{prefix}{i:02}"  # e.g., B01, C10, etc.
                cursor.execute("""
                    INSERT OR IGNORE INTO Rooms (roomID, roomType, Price, status)
                    VALUES (?, ?, ?, ?)
                """, (room_id, room_type, price, status))
        
        self.con.commit()
        cursor.close()

    def close(self):
        self.con.close()

    def create_password(self):
        """ Creates a default password entry in the database if it doesn't already exist.
            The default password is 'admin', which is hashed using SHA-256.
        """
        cursor = self.con.cursor()  # Create a cursor object for executing SQL queries
        cursor.execute("SELECT Password_Number FROM Password")  # Query to get existing password entries
        rows = cursor.fetchall()  # Fetch all rows from the query result

        if not rows:  # If no password exists yet
            password = "admin"  # Default password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash the password securely
            cursor.execute("INSERT INTO Password VALUES(?,?)", ("1", hashed_password))  # Insert default password into DB

        cursor.close()  # Close the cursor
        self.con.commit()  # Commit changes to the database
   
    def create_new_password(self, old_password, new_password):
        """ Changes the current password to a new one if the old password matches.
            Returns True if the password was changed successfully, False otherwise.
        """
        cursor = self.con.cursor()  # Create cursor for database operations
        cursor.execute("SELECT Hashed_password FROM Password ORDER BY Password_Number DESC LIMIT 1")  # Get latest stored password hash
        row = cursor.fetchone()  # Fetch the single result

        old_hash = hashlib.sha256(old_password.encode()).hexdigest()  # Hash the provided old password

        if not row:  # If no password is stored yet
            pass  # Do nothing (or handle accordingly)
        else:
            if old_hash == row[0]:  # Check if old password matches the stored hash
                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()  # Hash new password
                cursor.execute("INSERT INTO Password(Hashed_Password) VALUES(?)", (hashed_password,))  # Insert new hashed password
                cursor.close()  # Close cursor
                self.con.commit()  # Save changes
                return True  # Indicate password update success

        cursor.close()  # Close cursor if no match or no password
        self.con.commit()  # Commit any changes (though likely none here)
        return False  # Indicate password update failure

    def check_login(self, password):
        """ Checks if the provided password matches the latest stored password hash.
            Returns True if the password matches, False otherwise.
        """
        cursor = self.con.cursor()  # Create cursor to execute SQL queries
        cursor.execute("SELECT Hashed_password FROM Password ORDER BY Password_Number DESC LIMIT 1")  # Get latest stored password hash
        row = cursor.fetchone()  # Fetch the password hash from the query result

        hash_password = hashlib.sha256(password.encode()).hexdigest()  # Hash the input password

        if not row:  # If no password is stored yet
            pass  # Do nothing (could handle differently if needed)
        else:
            if hash_password == row[0]:  # Check if input password hash matches stored hash
                cursor.close()  # Close cursor
                return True  # Password is correct

        cursor.close()  # Close cursor if no match or no stored password
        self.con.commit()  # Commit any pending changes (usually unnecessary here)
        return False  # Password is incorrect or no stored password

    def get_overview(self):
        """ Retrieves an overview of the hotel occupancy status.
            Returns a tuple containing:
            - Total number of rooms
            - Number of occupied rooms
            - Number of available rooms
            - Occupancy rate (as a fraction)
        """
         # Create a cursor to execute SQL queries
        cursor = self.con.cursor()  # Create cursor to execute SQL queries
        cursor.execute("SELECT roomID FROM Rooms WHERE status='Occupied'")  # Get all occupied rooms
        results = cursor.fetchall()  # Fetch all occupied room IDs

        # Create an overview tuple:
        # (total rooms, occupied rooms, available rooms, occupancy ratio)
        overview = (
            self.Total_rooms,
            len(results),
            self.Total_rooms - len(results),
            len(results) / self.Total_rooms
        )

        cursor.close()  # Close the cursor
        self.con.commit()  # Commit any changes (likely none here)
        return overview  # Return the occupancy overview

    def get_tasks(self, date=None,time=None):
        """ Retrieves tasks from the database, optionally filtered by date and time.
            If date is None, retrieves all pending tasks.
            If date is provided, retrieves tasks due on that date or later.
            Returns a list of tuples containing task details.
        """
        # Create a cursor to execute SQL queries
        cursor = self.con.cursor()
        # If no date is provided, fetch all pending tasks
        if date==None:
            cursor.execute("SELECT * FROM Tasks WHERE status='Pending'")
        else:
            # If a date is provided, filter tasks by due date
            if time==None:
                time="00:00:00"
            end_time = date+" "+"23:59:59"
            start_time = date+" "+time
            cursor.execute("SELECT * FROM Tasks WHERE dueDate>=? AND dueDate <?", (start_time, end_time))
        # Fetch all results from the executed query
        result = cursor.fetchall()
        cursor.close()
        self.con.commit()
        return result
    
    def get_reservations(self, reservationID = None, guestID=None, date=None):
        """ Retrieves reservations from the database.
            If reservationID is provided, retrieves that specific reservation.
            If guestID and date are provided, retrieves reservations for that guest on that date.
            If only date is provided, retrieves reservations for that date.
            If no parameters are provided, retrieves all reservations.
            Returns a list of tuples containing reservation details.
        """
        # Create a cursor to execute SQL queries
        cursor = self.con.cursor()
        # If reservationID is provided, fetch that specific reservation
        if reservationID:
            cursor.execute("SELECT * FROM Reservations WHERE reservationID=?",(reservationID,))
        else:
            # If no reservationID is provided, filter by guestID and date
            if guestID == None and date == None:
                cursor.execute("SELECT * FROM Reservations")
            elif guestID != None and date != None:
                cursor.execute("SELECT * FROM Reservations WHERE guestID = ? AND check_in=? OR check_out = ?", (guestID, date, date))
            elif guestID ==None and date !=None:
                cursor.execute("SELECT * FROM Reservations WHERE check_in = ? or check_out = ?", (date, date))
            else:
                cursor.execute("SELECT * FROM Reservations WHERE guestID = ?", (guestID,))
        results = cursor.fetchall()
        cursor.close()
        self.con.commit()
        return results
    
    def change_reservation(self, reservationID, guestID, roomID, check_out, status):
        """ Updates an existing reservation with new details.
            Parameters:
            - reservationID: ID of the reservation to update
            - guestID: ID of the guest associated with the reservation
            - roomID: ID of the room reserved
            - check_out: Check-out date for the reservation
            - status: Status of the reservation (e.g., 'Completed', 'Pending')
            Returns True if the update was successful, False otherwise.
        """
         # Create a cursor to execute SQL queries
         # Create a cursor to execute SQL queries
        cursor = self.con.cursor()
        # Attempt to update the reservation with the provided details
        try:
            cursor.execute("UPDATE Reservations SET guestID=?, roomID=?, check_out=?, status=? WHERE reservationID=?", (guestID, roomID, check_out, status, reservationID))
            cursor.close()
            self.con.commit()
            return True
        # If an error occurs during the update, print the error and return False
        except sqlite3.Error as e:
            print("Failed: ", e)
            cursor.close()
            return False
            
    def make_reservation(self, reservationID, guestID, roomID, check_in, check_out, status):
        """ Creates a new reservation in the database.
            Parameters:
            - reservationID: Unique ID for the reservation
            - guestID: ID of the guest making the reservation
            - roomID: ID of the room reserved
            - check_in: Check-in date for the reservation
            - check_out: Check-out date for the reservation
            - status: Status of the reservation (e.g., 'Pending', 'Completed')
            Returns True if the reservation was added successfully, False otherwise.
        """
         # Create a cursor to execute SQL queries
        cursor = self.con.cursor()
        # Attempt to insert the new reservation into the Reservations table
        try:
            cursor.execute("INSERT INTO Reservations(reservationID, guestID, roomID, check_in, check_out, status) VALUES(?,?,?,?,?,?)", (reservationID, guestID, roomID, check_in, check_out, status))
            cursor.close()
            self.con.commit()
            return True
        except sqlite3.Error as e:
            print("Failed: ", e)
            cursor.close()
            return False
        
    def delete_reservation(self, reservationID):
        """ Deletes a reservation from the database.
            Parameters:
            - reservationID: ID of the reservation to delete
            Returns None.
        """
         # Create a cursor to execute SQL queries
        cursor = self.con.cursor()
        try:
            # Execute the delete command to remove the reservation with the specified ID
            cursor.execute("DELETE FROM Reservations WHERE reservationID = ?", (reservationID,))
            cursor.close()
            self.con.commit()
        except sqlite3.Error as e:
            print("Failed: ", e)
            cursor.close()
    
    def get_rooms(self, status, roomType):
        """ Retrieves rooms from the database based on their status and type.
            Parameters:
            - status: Status of the rooms (e.g., 'Occupied', 'Available', 'All Rooms')
            - roomType: Type of the rooms (e.g., 'Single', 'Double', 'All Rooms')
            Returns a list of tuples containing room details.
        """
         # Create a cursor to execute SQL queries
        cursor = self.con.cursor()
        # Depending on the status and roomType, execute the appropriate SQL query
        if status=="All Rooms" and roomType=="All Rooms":
            cursor.execute("SELECT * FROM Rooms")
        elif status!="All Rooms" and roomType=="All Rooms":
            cursor.execute("SELECT * FROM Rooms WHERE status=?", (status,))
        elif status=="All Rooms" and roomType!="All Rooms":
            cursor.execute("SELECT * FROM Rooms WHERE roomType=?", (roomType,))
        else:
            cursor.execute("SELECT * FROM Rooms WHERE status=? AND roomType=?", (status, roomType))
        
        results = cursor.fetchall()
        cursor.close()
        return results
    
    def get_guests(self, query=None):
        """ Retrieves guests from the database based on a search query.    
            If query is None, retrieves all guests.
            If query is provided, searches for guests by customerID, firstName, lastName, phoneNumber, or email.
            Returns a list of tuples containing guest details.
        """
         # Create a cursor to execute SQL queries
        cursor=self.con.cursor()
        # If no query is provided, fetch all guests
        if query==None:
            cursor.execute("SELECT * FROM Customers")
        # If a query is provided, search for guests matching the criteria
        else:
            query = f"%{query}%"
            cursor.execute("""SELECT * FROM Customers
                            WHERE customerID LIKE ?
                                OR firstName LIKE ?
                                OR lastName LIKE ?
                                OR phoneNumber = ?
                                OR email LIKE ?""", (query, query, query, query, query))
        results = cursor.fetchall()
        cursor.close()
        return results
    
    def add_guest(self, id, first, last, age, email, phone):
        """ Adds a new guest to the database.
            Parameters:
            - id: Unique ID for the guest
            - first: First name of the guest
            - last: Last name of the guest
            - age: Age of the guest
            - email: Email address of the guest
            - phone: Phone number of the guest
            Returns True if the guest was added successfully, False otherwise.
        """
         # Create a cursor to execute SQL queries
        cursor = self.con.cursor()
        # Check if any of the required fields are empty
        if id=="" or first=="" or last=="":
            return False
        # Attempt to insert the new guest into the Customers table
        try:
            # Execute the insert command with the provided guest details
            cursor.execute("INSERT INTO Customers(customerID, firstName, lastName, age, email, phoneNumber) VALUES(?,?,?,?,?,?)", (id, first, last, age, email, phone))
            cursor.close()
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return False
        return True
    
    def add_task(self, description, created, due, status):
        """ Adds a new task to the database.
            Parameters:
            - description: Description of the task
            - created: Creation date of the task
            - due: Due date for the task
            - status: Status of the task (e.g., 'Pending', 'Completed')
            Returns True if the task was added successfully, False otherwise.
        """
        # Create a cursor to execute SQL queries
        cursor = self.con.cursor()
        try:
            cursor.execute("INSERT INTO Tasks(description, createdAt, dueDate, status) VALUES(?,?,?,?)", (description, created, due, status))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return False
        cursor.close()
        return True
    
    def change_status(self, description, created, due, status):
        """ Changes the status of an existing task in the database.
            Parameters:
            - description: Description of the task
            - created: Creation date of the task
            - due: Due date for the task
            - status: New status for the task (e.g., 'Pending', 'Completed')
            Returns True if the status was updated successfully, False otherwise.
        """
        # Create a cursor to execute SQL queries
        cursor = self.con.cursor()
        try:
            # Execute the update command to change the status of the specified task
            cursor.execute("UPDATE Tasks SET status=? WHERE description=? AND createdAt=? AND dueDate =?", (status, description, created, due))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return False
        cursor.close()
        return True
    
    def get_reservation_id_for_checkout(self):
        """ Retrieves reservation IDs for check-out that have a check-in date but no check-out date.
            Returns a list of reservation IDs that are pending check-out.
        """
         # Create a cursor to execute SQL queries
        cursor = self.con.cursor()
        # Execute the query to find reservations that have check-in but no check-out
        cursor.execute("SELECT reservationID FROM Reservations WHERE check_out IS NULL AND check_in IS NOT NULL")
        rows = cursor.fetchall()
        cursor.close()
        # Extract reservation IDs from the fetched rows
        results = [row[0] for row in rows]
        return results
    
    def get_reservation_id_for_checkin(self):
        """ Retrieves reservation IDs that have not yet checked in.
            Returns a list of reservation IDs that are pending check-in.
        """
         # Create a cursor to execute SQL queries
        cursor = self.con.cursor()
        cursor.execute("SELECT reservationID FROM Reservations WHERE check_in IS NULL")
        rows = cursor.fetchall()
        cursor.close()
        # Extract reservation IDs from the fetched rows
        results = [row[0] for row in rows]
        return results
    
    def get_price(self, roomID):
        """ Retrieves the price of a room based on its roomID.
            Parameters:
            - roomID: ID of the room for which to retrieve the price
            Returns the price of the room as a tuple, or None if the room does not exist.
        """
         # Create a cursor to execute SQL queries
        cursor = self.con.cursor()
        cursor.execute("SELECT price FROM Rooms WHERE roomID=?", (roomID,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def check_out(self, reservationID, check_out):
        """ Updates the check-out date for a reservation and marks it as completed.
            Parameters:
            - reservationID: ID of the reservation to update
            - check_out: Check-out date for the reservation
            Returns True if the update was successful, False otherwise.
        """
         # Create a cursor to execute SQL queries
        cursor = self.con.cursor()
        try:
            # Execute the update command to set the check-out date and change status to 'Completed'
            cursor.execute("UPDATE Reservations SET check_out = ? ,status='Completed' WHERE reservationID = ?", (check_out, reservationID))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return False
        cursor.close()
        return True
    
    def check_in(self, reservationID, check_in):
        """ Updates the check-in date for a reservation and marks it as completed.
            Parameters:
            - reservationID: ID of the reservation to update
            - check_in: Check-in date for the reservation
            Returns True if the update was successful, False otherwise.
        """
         # Create a cursor to execute SQL queries
        cursor = self.con.cursor()
        try:
            # Execute the update command to set the check-in date and change status to 'Completed'
            cursor.execute("UPDATE Reservations SET check_in = ?, status='Completed' WHERE reservationID = ?", (check_in, reservationID))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return False
        cursor.close()
        return True
    
    def get_next_reservation_id(self):
        """ Generates the next reservation ID based on the highest existing reservation ID in the database.
            The reservation ID format is 'R' followed by a three-digit number (e.g., 'R001', 'R002').
            Returns the next reservation ID as a string, or None if an error occurs.
        """
         # Create a cursor to execute SQL queries
        cursor = self.con.cursor()
        try:
            # Execute a query to find the maximum reservation ID, extracting the numeric part
            cursor.execute("SELECT MAX(CAST(SUBSTR(reservationID, 2) AS INTEGER)) FROM Reservations")
            result = cursor.fetchone()
            # If no reservations exist, start with 'R001'
            max_id_num = result[0] if result[0] is not None else 0
            # Generate the next reservation ID by incrementing the maximum found ID
            next_id = f"R{max_id_num + 1:03}"
            return next_id
        except sqlite3.Error as e:
            print(f"Error generating Reservation ID: {e}")
            return None
        finally:
            cursor.close()

    def get_occupancy_data(self, start, end):   
        """ Generates an occupancy report for the hotel.
            The report includes daily occupancy rates between the specified start and end dates.
            Returns a DataFrame containing the occupancy data.
        """

        # Execute the occupancy report query
        query ="""
        WITH RECURSIVE all_dates(occupancy_date) AS (
            SELECT DATE(?)
            UNION ALL
            SELECT DATE(occupancy_date, '+1 day')
            FROM all_dates
            WHERE occupancy_date < DATE(?)
        )
        SELECT
            d.occupancy_date AS 'Date',
            COUNT(DISTINCT r.roomID) AS 'Occupied Rooms',
            (SELECT COUNT(*) FROM Rooms) AS 'Total Rooms',
            ROUND(
                (COUNT(DISTINCT r.roomID) * 100.0) / 
                (SELECT COUNT(*) FROM Rooms),
                2
            ) AS 'Occupancy Rate (%)'
        FROM all_dates d
        LEFT JOIN Reservations r
            ON d.occupancy_date >= DATE(r.check_in)
            AND d.occupancy_date < DATE(r.check_out)
            AND r.status != 'Cancelled'
        GROUP BY d.occupancy_date
        ORDER BY d.occupancy_date;
        """
        # Load results into DataFrame
        report_df = pd.read_sql_query(query, self.con, params=(start, end))
        
        return report_df
    
    def get_revenue_data(self, start, end):
        """ Generates a revenue report for the hotel.
            The report includes daily revenue, average room rate, and rooms occupied between the specified start and end dates.
            Returns a DataFrame containing the revenue data.
        """
        # Execute the revenue report query
        query = """
        WITH RECURSIVE all_dates(occupancy_date) AS (
            SELECT DATE(?)
            UNION ALL
            SELECT DATE(occupancy_date, '+1 day')
            FROM all_dates
            WHERE occupancy_date < DATE(?)
        ),
        revenue_data AS (
            SELECT
                d.occupancy_date,
                rm.price
            FROM all_dates d
            JOIN Reservations res
                ON d.occupancy_date >= DATE(res.check_in)
                AND d.occupancy_date < DATE(res.check_out)
                AND res.status != 'Cancelled'
            JOIN Rooms rm ON res.roomID = rm.roomID
            GROUP BY d.occupancy_date, res.roomID
        )
        SELECT
            occupancy_date AS 'Date',
            COALESCE(SUM(price), 0) AS 'Daily Revenue',
            COALESCE(ROUND(AVG(price), 2), 0) AS 'Average Room Rate',
            COUNT(*) AS 'Rooms Occupied'
        FROM revenue_data
        GROUP BY occupancy_date
        ORDER BY occupancy_date;
        """

        # Load results into DataFrame
        report_df = pd.read_sql_query(query, self.con, params=(start, end))
        
        return report_df
    
    def generate_guest_report(self):
        """ Generates a guest report summarizing customer information and their reservation history.
            The report includes guest details, total reservations, nights stayed, total revenue, first stay, and last stay.
            Returns a DataFrame containing the guest report data.
        """
        query = """
        WITH guest_reservations AS (
            SELECT
                c.customerID,
                c.firstName || ' ' || c.lastName AS fullName,
                c.age,
                c.email,
                c.phoneNumber,
                r.reservationID,
                r.check_in,
                r.check_out,
                r.status,
                rm.roomType,
                rm.price,
                -- Calculate nights stayed
                CAST(JULIANDAY(r.check_out) - JULIANDAY(r.check_in) AS INTEGER) AS nights,
                -- Calculate reservation revenue
                ((JULIANDAY(r.check_out) - JULIANDAY(r.check_in)) * rm.price) AS revenue
            FROM Customers c
            LEFT JOIN Reservations r ON c.customerID = r.guestID
            LEFT JOIN Rooms rm ON r.roomID = rm.roomID
            WHERE r.status != 'Cancelled' OR r.status IS NULL
        )
        SELECT
            customerID AS 'Customer ID',
            fullName AS 'Full Name',
            age AS 'Age',
            email AS 'Email',
            phoneNumber AS 'Phone',
            COUNT(reservationID) AS 'Total Reservations',
            COALESCE(SUM(nights), 0) AS 'Total Nights',
            COALESCE(SUM(revenue), 0) AS 'Total Revenue',
            COALESCE(MIN(check_in), 'Never') AS 'First Stay',
            COALESCE(MAX(check_out), 'Never') AS 'Last Stay'
        FROM guest_reservations
        GROUP BY customerID
        ORDER BY fullName;
        """
        
        df = pd.read_sql_query(query, self.con)
        return df