import sqlite3
import hashlib

class SQL:
    def __init__(self):
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
        return False
            