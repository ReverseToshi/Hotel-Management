import sqlite3
import hashlib
import pandas as pd

class SQL:
    def __init__(self):
        self.Total_rooms = 50
        try:
            self.con = sqlite3.connect("database.db")
            self.create_password()
        except:
            raise FileNotFoundError

    def close(self):
        self.con.close()

    def create_password(self):
        cursor = self.con.cursor()
        cursor.execute("SELECT Password_Number FROM Password")
        rows = cursor.fetchall()
        if not rows:
            password = "admin"
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("INSERT INTO Password VALUES(?,?)", ("1", hashed_password))

        cursor.close()
        self.con.commit()
        
    def create_new_password(self, old_password, new_password):
        cursor = self.con.cursor()
        cursor.execute("SELECT Hashed_password FROM Password ORDER BY Password_Number DESC LIMIT 1")
        row = cursor.fetchone()
        old_hash = hashlib.sha256(old_password.encode()).hexdigest()
        if not row:
            pass
        else:
            if old_hash==row[0]:
                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                cursor.execute("INSERT INTO Password(Hashed_Password) VALUES(?)", (hashed_password,))
                cursor.close()
                self.con.commit()
                return True
        
        cursor.close()
        self.con.commit()
        return False

    def check_login(self, password):
        cursor = self.con.cursor()
        cursor.execute("SELECT Hashed_password FROM Password ORDER BY Password_Number DESC LIMIT 1")
        row = cursor.fetchone()
        hash_password = hashlib.sha256(password.encode()).hexdigest()
        if not row:
            pass
        else:
            if hash_password == row[0]:
                cursor.close()
                return True
        
        cursor.close()
        self.con.commit()
        return False

    def get_overview(self):
        cursor = self.con.cursor()
        cursor.execute("SELECT roomID FROM Rooms WHERE status='Occupied'")
        results = cursor.fetchall()
        overview = (self.Total_rooms, len(results), self.Total_rooms - len(results), (len(results))/self.Total_rooms)
        cursor.close()
        self.con.commit()
        return overview

    def get_tasks(self, date=None,time=None):
        cursor = self.con.cursor()
        if date==None:
            cursor.execute("SELECT * FROM Tasks WHERE status='Pending'")
        else:
            if time==None:
                time="00:00:00"
            end_time = date+" "+"23:59:59"
            start_time = date+" "+time
            cursor.execute("SELECT * FROM Tasks WHERE dueDate>=? AND dueDate <?", (start_time, end_time))
        result = cursor.fetchall()
        cursor.close()
        self.con.commit()
        return result
    
    def get_reservations(self, reservationID = None, guestID=None, date=None):
        cursor = self.con.cursor()
        if reservationID:
            cursor.execute("SELECT * FROM Reservations WHERE reservationID=?",(reservationID,))
        else:
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
        cursor = self.con.cursor()
        try:
            cursor.execute("UPDATE Reservations SET guestID=?, roomID=?, check_out=?, status=? WHERE reservationID=?", (guestID, roomID, check_out, status, reservationID))
            cursor.close()
            self.con.commit()
            return True
        except sqlite3.Error as e:
            print("Failed: ", e)
            cursor.close()
            return False
            
    def make_reservation(self, reservationID, guestID, roomID, check_in, check_out, status):
        cursor = self.con.cursor()
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
        cursor = self.con.cursor()
        try:
            cursor.execute("DELETE FROM Reservations WHERE reservationID = ?", (reservationID,))
            cursor.close()
            self.con.commit()
        except sqlite3.Error as e:
            print("Failed: ", e)
            cursor.close()
    
    def get_rooms(self, status, roomType):
        cursor = self.con.cursor()
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
        cursor=self.con.cursor()
        if query==None:
            cursor.execute("SELECT * FROM Customers")
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
        cursor = self.con.cursor()
        if id=="" or first=="" or last=="":
            return False
        try:
            cursor.execute("INSERT INTO Customers(customerID, firstName, lastName, age, email, phoneNumber) VALUES(?,?,?,?,?,?)", (id, first, last, age, email, phone))
            cursor.close()
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return False
        return True
    
    def add_task(self, description, created, due, status):
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
        cursor = self.con.cursor()
        try:
            cursor.execute("UPDATE Tasks SET status=? WHERE description=? AND createdAt=? AND dueDate =?", (status, description, created, due))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return False
        cursor.close()
        return True
    
    def get_reservation_id_for_checkout(self):
        cursor = self.con.cursor()
        cursor.execute("SELECT reservationID FROM Reservations WHERE check_out IS NULL AND check_in IS NOT NULL")
        rows = cursor.fetchall()
        cursor.close()
        results = [row[0] for row in rows]
        return results
    
    def get_reservation_id_for_checkin(self):
        cursor = self.con.cursor()
        cursor.execute("SELECT reservationID FROM Reservations WHERE check_in IS NULL")
        rows = cursor.fetchall()
        cursor.close()
        results = [row[0] for row in rows]
        return results
    
    def get_price(self, roomID):
        cursor = self.con.cursor()
        cursor.execute("SELECT price FROM Rooms WHERE roomID=?", (roomID,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def check_out(self, reservationID, check_out):
        cursor = self.con.cursor()
        try:
            cursor.execute("UPDATE Reservations SET check_out = ? ,status='Completed' WHERE reservationID = ?", (check_out, reservationID))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return False
        cursor.close()
        return True
    
    def check_in(self, reservationID, check_in):
        cursor = self.con.cursor()
        try:
            cursor.execute("UPDATE Reservations SET check_in = ?, status='Completed' WHERE reservationID = ?", (check_in, reservationID))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return False
        cursor.close()
        return True
    
    def get_next_reservation_id(self):
        cursor = self.con.cursor()
        try:
            cursor.execute("SELECT MAX(CAST(SUBSTR(reservationID, 2) AS INTEGER)) FROM Reservations")
            result = cursor.fetchone()
            max_id_num = result[0] if result[0] is not None else 0
            next_id = f"R{max_id_num + 1:03}"
            return next_id
        except sqlite3.Error as e:
            print(f"Error generating Reservation ID: {e}")
            return None
        finally:
            cursor.close()

    def get_occupancy_data(self, start, end):    
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