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