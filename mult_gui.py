import PySimpleGUI as sg
from tkinter import messagebox
from admin_db import work_admin_db


class Admin_Mult_GUI():
	
    def __init__(self): 

        self.mult_results = {
            "pic_enable":"",
            "pic_res":" default",
            "vid_enable":"",
            "vid_frames":"",
            "vid_length":"",
            "vid_enable_txt":""
        }      
        self.get_db_data()

        self.frame_pic_layout = [   
            [sg.Checkbox('Enable Pics', key="chk_pic", disabled=True, default=True)], 
            [sg.T('Pic Res'), sg.Input(size=(12,1), default_text=" default", disabled=True )]
            ]
        self.frame_vid_layout = [ 
            [sg.T('Video Rec'), sg.InputCombo(('Enabled', 'Disabled'), size=(10, 1), key="vid_rec", default_value=self.mult_results['vid_enable_txt'])], 
            [sg.T('Video Frames'), sg.Input(size=(12,1), key="txt_vid_frames", default_text=self.mult_results["vid_frames"])],
            [sg.T('Video Length'), sg.Input(size=(12,1), key="txt_vid_length", default_text=self.mult_results["vid_length"])]
            ]        
        self.layout = [      
            [sg.Frame('Pictures', self.frame_pic_layout, font='Any 12', title_color='blue')], 
            [sg.Frame('Videos', self.frame_vid_layout, font='Any 12', title_color='blue')],                  
            [sg.Button("Save")]      
            ]

        self.create_gui()    
        

    def create_gui(self):
        window = sg.Window('Multimedia Settings', self.layout, font=("Helvetica", 12))
        #self.get_db_data(window)    

        while True:
            event, values = window.Read()

            if event in (None, 'Exit'):
                break
            
            if event == "Save":
                self.save_to_db(window, values)
                
        window.Close()


    # Gets data from the database and stores it in an dictionary
    def get_db_data(self):
        admin_db_data = work_admin_db().get_all_db()
        self.mult_results['pic_enable'] = admin_db_data[0][5] 
        self.mult_results['vid_enable'] = admin_db_data[0][7]
        self.mult_results['vid_frames'] = admin_db_data[0][8]
        self.mult_results['vid_length'] = admin_db_data[0][9]
        if self.mult_results['vid_enable'] == 1:
            self.mult_results['vid_enable_txt'] = "Enabled"
        else:
            self.mult_results['vid_enable_txt'] = "Disabled"
    
 
    # Saves the data in the form in the database.
    def save_to_db(self, win, values):
        vid_rec = values['vid_rec']
        txt_vid_frames = values['txt_vid_frames']
        txt_vid_length = values['txt_vid_length']        

        # Converts value of drop down box to either 1 or 0 to be stored in database.
        if vid_rec == 'Enabled':
            rec = 1
        else:
            rec = 0

        #-------------------VALIDATION-----------------------
        # Checks for blanks
        if not txt_vid_frames or not txt_vid_length:
            self.display_err("Text boxes cannot be blank.")
            return

        # Makes sure theres only numbers in the text box 1        
        try:
            frames = int(txt_vid_frames)
        except:
            self.display_err("Only numbers allowed in the text boxes.")
            return

        # Makes sure theres only numbers in the text box 2        
        try:
            vid_len = int(txt_vid_length)
        except:
            self.display_err("Only numbers allowed in the text boxes.")
            return
        #----------------------------------------------------

        # Runs query if validation passes    
        MsgBox = self.msg_confirmation('Are you sure you want SAVE this data?')			
        if MsgBox == "yes":    
            qry = 'UPDATE Admin_Table SET video_enable = '+str(rec)+', video_res = '+str(frames)+', video_length = '+str(vid_len)+' WHERE id = 1'
            work_admin_db().execute_query_db(qry)
        


    # Message/Question for confirmation. Returns Yes or No.    
    def msg_confirmation(self, msg ):		
	    return messagebox.askquestion("Verification", msg, icon="question")
		

	# Displays error messages.
    def display_err(self, msg):
	    messagebox.showerror("Error", msg)
        
        



#call_main = Admin_Mult_GUI()
