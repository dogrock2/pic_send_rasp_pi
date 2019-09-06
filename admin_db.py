import sqlite3

class work_admin_db:

    # Initializes the database
    def __init__(self):        
        self.con = sqlite3.connect("db/data.db")
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()


    # Performs query to get all the data from the admin record.
    def get_all_db(self):
        self.cur.execute("Select * from Admin_Table WHERE id = 1")
        rec = self.cur.fetchall()  
        return rec


    # Performs query to get admin password.
    def search_pwd_db(self):
        self.cur.execute("Select pwd from Admin_Table WHERE id = 1")
        pwd = self.cur.fetchall()  
        return pwd


    # Executes any query thats sent to it via a parameter.
    def execute_query_db(self, qry):        
        self.cur.execute(qry)        
        self.con.commit()