import sqlite3

class work_cam_db:

    # Initializes the database
    def __init__(self):        
        self.con = sqlite3.connect("db/data.db")
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()


    # Performs query to get all the data from the cam settings record.
    def get_all_db(self):
        self.cur.execute("Select * from Cam_Table WHERE id = 1")
        rec = self.cur.fetchall()  
        return rec

    # Updates the cam settings record. Accepts a tuple as parameter.
    def execute_update_db(self, data): 
        print(data)      
        self.cur.execute("UPDATE Cam_Table SET xpos = "+data[0]+", ypos = "+data[1]+", width = "+data[2]+", height = "+data[3]+" Where id = 1")
        self.con.commit()
