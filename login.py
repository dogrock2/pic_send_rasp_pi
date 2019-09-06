import PySimpleGUI as sg
from tkinter import messagebox
from admin_db import work_admin_db

class Admin_login_GUI():
	
    def __init__(self, cb):

        self.close_win = False
        self.callback = cb
        
        # Sets all the components for form.
        self.frame_login_layout = [      
                [sg.T('User Name'), sg.Input(size=(12,1), key="txt_user", default_text=" admin", disabled=True)],
                [sg.T('Password'), sg.Input(size=(12,1), key="txt_pwd", password_char='*', pad=(11,0), focus=True)]
                ]
        self.layout = [                      
                [sg.Frame('Login', self.frame_login_layout, font='Any 12', title_color='blue')],    
                [sg.Button("Submit"), sg.Button("Clear")]      
                ]
        # Calls the function to open the window with all the components.
        self.create_gui()


    # Calls the window object so the window gets created and opens up.
    def create_gui(self):
        window = sg.Window('Login', self.layout, font=("Helvetica", 12))

        while True:

            if self.close_win:
                break

            event, values = window.Read()

            if event in (None, 'Exit'):
                break

            if event == "Clear":
                self.clear_fields(window)
            if event == "Submit":
                self.confirm_pwd(window, values)   
                           
        window.Close()


    # Clears all the text boxes in the form    
    def clear_fields(self, win):
        win.Element('txt_pwd').Update('')


    # Verifies the password.
    def confirm_pwd(self, win, vals):            
        admin_pwd = work_admin_db().search_pwd_db()           
        if vals["txt_pwd"] == admin_pwd[0][0]:   
            win.Hide()                    
            self.close_window()
            self.callback()       
        else:
            self.clear_fields(win)
            self.display_err("Incorrect password!")

    def close_window(self):
        self.close_win = True
                    

	# Displays error messages.
    def display_err(self, msg):
	    messagebox.showerror("Error", msg)
		

# call_main = Admin_login_GUI()