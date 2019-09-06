import PySimpleGUI as sg
from tkinter import messagebox
from admin_db import work_admin_db


class Admin_Settings_GUI():
	
    def __init__(self):        

        # Variable that will store all the data from the database
        self. saved_data = {
            'Email':'',
            'Phone':'',
            'Sid':'',
            'Token':'',
            'Tphone':''
        }

        # Calls the function to retrieve data from the db
        self.get_db_data()

        self.frame_admin_layout = [      
             [sg.T('Email')], 
             [sg.Input(size=(40,1), key="txt_email", default_text=self.saved_data['Email'])],
             [sg.T('Phone')], 
             [sg.Input(size=(40,1), key="txt_phone", default_text=self.saved_data['Phone'])],
             [sg.T('Twilio SID')], 
             [sg.Input(size=(40,1), key="txt_sid", default_text=self.saved_data['Sid'])],
             [sg.T('Twilio Token')], 
             [sg.Input(size=(40,1), key="txt_token", default_text=self.saved_data['Token'])],
             [sg.T('Twilio Phone')],
             [sg.Input(size=(40,1), key="txt_tphone", default_text=self.saved_data['Tphone'])]             
             ]        
        self.layout = [      
            [sg.Frame('Settings', self.frame_admin_layout, font='Any 12', title_color='blue')],                                 
            [sg.Button("Save")]      
            ]
                
        self.create_gui()


    def create_gui(self):
        window = sg.Window('Admin Settings', self.layout, font=("Helvetica", 12))        

        while True:
            event, values = window.Read()

            if event in (None, 'Exit'):
                break

            if event == 'Save':
                self.save_to_db(window, values)


        window.Close()


    # Takes all the data in the db and stores it in a dictionary.
    def get_db_data(self):
        admin_db_data = work_admin_db().get_all_db()
        self.saved_data['Email'] = admin_db_data[0][4]
        self.saved_data['Phone'] = admin_db_data[0][3]
        self.saved_data['Sid'] = admin_db_data[0][10]
        self.saved_data['Token'] = admin_db_data[0][12]
        self.saved_data['Tphone'] = admin_db_data[0][11]
        

    # Saves the data to the database
    def save_to_db(self, win, values):
                
        email = values['txt_email']
        phone = values['txt_phone']
        api_key = values['txt_sid']   
        twToken = values['txt_token']
        twPhone = values['txt_tphone']

        # Verifies that the fields are not blank
        vals = (email, phone, api_key, twToken, twPhone)
        for i in vals:
            if not i:
                self.display_err("Cannot have any blanks")
                return

        MsgBox = self.msg_confirmation('Are you sure you want SAVE this data?')			
        if MsgBox == "yes":
            qry = 'UPDATE Admin_Table SET email = "'+email+'", phone = '+phone+', api_key = "'+api_key+'", twphone = '+twPhone+', twToken = "'+twToken+'"'
            work_admin_db().execute_query_db(qry)
            self.get_db_data()
            
    
    # Message/Question for confirmation. Returns Yes or No.    
    def msg_confirmation(self, msg ):		
	    return messagebox.askquestion("Verification", msg, icon="question")
		

	# Displays error messages.
    def display_err(self, msg):
	    messagebox.showerror("Error", msg)
		



#Admin_Settings_GUI()