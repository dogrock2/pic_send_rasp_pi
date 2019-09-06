import PySimpleGUI as sg
from tkinter import messagebox
from admin_db import work_admin_db


class Admin_PWD_GUI():
	
    def __init__(self):
        
        # Sets all the components for form.
        self.frame_pwd_layout = [      
             [sg.T('Original PWD'), sg.Input(size=(12,1), key="txt_original", password_char='*', pad=(20,0))],
             [sg.T('New PWD'), sg.Input(size=(12,1), pad=(45,0), key="txt_new", password_char='*')],
             [sg.T('Comfirm PWD'), sg.Input(size=(12,1), pad=(14,0), key="txt_confirm", password_char='*')]
             ]
        self.layout = [                      
                [sg.Frame('Password', self.frame_pwd_layout, font='Any 12', title_color='blue')],    
                [sg.Button("Save")]      
                ]
        # Calls the function to open the window with all the components.
        self.create_gui()


    # Calls the window object so the window gets created and opens up.
    def create_gui(self):
        window = sg.Window('Change Password', self.layout, font=("Helvetica", 12))

        while True:
            event, values = window.Read()

            if event in (None, 'Exit'):
                break

            if event == "Save":
                self.chng_pwd(window, values)            
            
        window.Close()

    
    # Verifies that the original password entere matches the one in the database.
    def verify_old_pwd(self, pwd):
        admin_db = work_admin_db().search_pwd_db()        
        if admin_db[0][0] == pwd:
            return True
        return False


    # Clears all the text boxes in the form    
    def clear_fields(self, win):
        win.Element('txt_original').Update('')
        win.Element('txt_new').Update('')
        win.Element('txt_confirm').Update('')


    # Does form validation and then changes the password.
    def chng_pwd(self, win, vals):
                
        if not vals['txt_original'] or not  vals['txt_new'] or not vals['txt_confirm']:
            self.display_err("Cannot have any blanks.")
            self.clear_fields(win)
        else:
            if not self.verify_old_pwd(vals['txt_original']):
                self.display_err("The original password entered is incorrect.")
                self.clear_fields(win)
            else:
                if vals['txt_new'] != vals['txt_confirm']:
                    self.display_err("New password must match the confirm password.")
                    self.clear_fields(win)
                else:
                    MsgBox = self.msg_confirmation('Are you sure you want CHANGE your password?')			
                    if MsgBox == "yes":
                        qry = "UPDATE Admin_Table SET pwd = '"+vals['txt_new']+"' WHERE id = 1"
                        work_admin_db().execute_query_db(qry)
                        self.clear_fields(win)
                        messagebox.showinfo("Success", "Your password has been changed.")
                        
                    

    # Message/Question for confirmation. Returns Yes or No.    
    def msg_confirmation(self, msg ):		
	    return messagebox.askquestion("Verification", msg, icon="question")
		

	# Displays error messages.
    def display_err(self, msg):
	    messagebox.showerror("Error", msg)
		

# call_main = Admin_PWD_GUI()
