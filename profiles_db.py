import sqlite3

class work_profiles_db:

    # Initializes the database
    def __init__(self):        
        self.con = sqlite3.connect("db/data.db")
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    # Performs query to get all the records currently in the database.
    def search_all_db(self):
        self.cur.execute("SELECT * from Profiles_Table")
        rows = self.cur.fetchall()  
        return rows

    # Performs query to get a single record by ID.
    def search_one_db(self, id):
        self.cur.execute("SELECT * from Profiles_Table WHERE id = "+id)
        row = self.cur.fetchall()  
        return row

    # Executes any query thats sent to it via a parameter.
    def execute_query_db(self, qry):        
        self.cur.execute(qry)        
        self.con.commit()
        
 # ref = b = Entry(self.frame2, width=11, textvariable=self.table_data, validate="focus", validatecommand=self.on_id_Click)	
 # ref = # b.bind("<Button-1>", lambda event: self.on_id_Click(event, "DATA TO PASS"))