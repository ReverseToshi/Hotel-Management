import sqlite3
import hashlib

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
                cursor.execute("INSERT INTO Password(Hashed) VALUES(?)", (hashed_password))
                cursor.close()
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

    def get_tasks(self):
        cursor = self.con.cursor()
        cursor.execute("SELECT description, dueDate FROM Tasks WHERE status='Pending'")
        tasks = []
        result = cursor.fetchall()
        for row in result:
            tasks.append((row[0], row[1]))
        cursor.close()
        self.con.commit()
        return tasks
    
    def get_reservations(self, guestID=None, date=None):
        cursor = self.con.cursor()
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