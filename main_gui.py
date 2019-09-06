import PySimpleGUI as sg
from tkinter import messagebox
from profiles_db import work_profiles_db
from profiles_gui import Profiles_DBviewer
from admin_gui import Admin_Settings_GUI
from mult_gui import Admin_Mult_GUI
from pwd_gui import Admin_PWD_GUI
from login import Admin_login_GUI
from cam_gui import Cam_GUI
from cam_app import cam_view as cam
import send_email 
import send_msg


class Admin_Main_GUI():
	
    def __init__(self):     

        #self.cam_inst = cam
        self.all_names = ['Choose one...']
        self.get_all_names()
        
                
        # ------ Menu Definition ------ #
        self.menu_def = [['Settings', ['Multimedia', 'Password', 'Settings','Camera' ]],
                    ['Students',['Profiles']] ]
                    
        # ------ GUI Definition ------ #
        self.layout = [
                [sg.Menu(self.menu_def, tearoff=False, pad=(20,1))],
                [sg.InputCombo((self.all_names), size=(30, 1), key="names_combo"), sg.Button(button_text="Take")], 
                ]
        self.camera = cam()
        self.create_gui()
        
        

    def create_gui(self):        
        window = sg.Window("School Multimedia App").Layout(self.layout)        
        ins_dic = {
            "Profiles": Profiles_DBviewer,
            "Settings": Admin_Settings_GUI, 
            "Multimedia": Admin_Mult_GUI,
            "Camera": Cam_GUI
            
        }
        
        while True:
            event, values = window.Read()

            if event in (None, 'Exit'):
                break
                        
            if event == "Take":
                self.take_pic(window, values)
            elif event == "Password":
                Admin_PWD_GUI()
            else:                                                                      
                Admin_login_GUI( ins_dic[event] )
        
        window.Close()

    # Gets all the data from the database. Takes the id with the first and last name. Stores
    # the data in the variable all_names and displays it in the drop down box upon boot.
    def get_all_names(self):        
        db_data = work_profiles_db().search_all_db()
        rows_cnt = len(db_data)	
        for i in range(rows_cnt):	
            self.all_names.append( str(db_data[i][0])+" "+db_data[i][1]+" "+db_data[i][2] )  
                
        
    # Grabs the ID of the selected name when the TAKE button is pressed.
    def take_pic(self, win, value):        
        sel_val = value['names_combo']
        sel_id = sel_val.split(" ")[0]        
        self.camera.take_pic()
        if not sel_id == 'Choose':
            self.grab_data_by_id(sel_id)
    
    # Gets the contact information from the profiles table in db searching by id.
    def grab_data_by_id(self, id):
        
        db_data = work_profiles_db().search_one_db(id)        
        type = db_data[0][5]

        if type == 'Email':
            self.send_email_msg(db_data[0][4])
        elif type == 'SMS':
            self.send_txt_msg(db_data[0][3])
        elif type == 'SMS/Email':
            self.send_email_msg(db_data[0][4])
            self.send_txt_msg(db_data[0][3])
        else:
            messagebox.showerror("Error", "No communications method selected.")
                    
        
    # Calls the email script and sends the email.
    def send_email_msg(self, mail_to):
        send_email.send_msg(mail_to)
        

    # Sends the txt message by calling the twilio script.
    def send_txt_msg(self, txt_to):        
        send_msg.send_twilio_msg(txt_to)

Admin_Main_GUI()

