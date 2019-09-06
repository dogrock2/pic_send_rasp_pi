import PySimpleGUI as sg
from tkinter import messagebox
from cam_db import work_cam_db


# GUI to set the camera settings.
# So far is position x,y and image size for viewing. Width and Height

class Cam_GUI():
	
	def __init__(self):
		
		self.rec = work_cam_db().get_all_db()
		self.saved_data = {
            'xpos': self.rec[0][1],
            'ypos': self.rec[0][2],
            'width': self.rec[0][3],
            'height': self.rec[0][4]            
        }
		
		self.frame_admin_layout = [
				 [sg.T('X position')], 
				 [sg.Input(size=(40,1), key="txt_x", default_text=self.saved_data['xpos'])],
				 [sg.T('Y position')], 
				 [sg.Input(size=(40,1), key="txt_y", default_text=self.saved_data['ypos'])],
				 [sg.T('Width')], 
				 [sg.Input(size=(40,1), key="txt_width", default_text=self.saved_data['width'])],
				 [sg.T('Height')],
				 [sg.Input(size=(40,1), key="txt_height", default_text=self.saved_data['height'])]
				 ]
		self.layout = [      
			[sg.Frame('Settings', self.frame_admin_layout, font='Any 12', title_color='blue')],                                 
			[sg.Button("Save")]   
			] 
			
		self.create_gui()
			
	def create_gui(self):
		window = sg.Window('Cam Preview Settings', self.layout, font=("Helvetica", 12))					   
		
		while True:
			event, values = window.Read()  			
			
			if event in (None, 'Exit'):
				break
				
			if event == 'Save':
				self.save_to_db(window, values)
						
		window.Close()
		
		
	# Takes all the data from the form and updates the database.
	def save_to_db(self, win, values):
		print(values)
		try:
			validate = (int(values["txt_x"]),int(values["txt_y"]),int(values["txt_width"]),int(values["txt_height"]))
			vals = (values["txt_x"],values["txt_y"],values["txt_width"],values["txt_height"])
			MsgBox = self.msg_confirmation('Warning!', 'Are you sure you want UPDATE this record?', 'warning')			
			if MsgBox == "yes":
				work_cam_db().execute_update_db(vals)
				messagebox.showinfo("Success", "Data saved. Please restart app for changes to take effect.")
		except ValueError:
			self.display_err("Only numbers please.")


	# Message/Question for confirmation. Returns Yes or No.
	def msg_confirmation(self, _type, msg, _icon):		
		return messagebox.askquestion(_type, msg, icon=_icon)

		
	# Displays error messages.
	def display_err(self, msg):
		messagebox.showerror("Error", msg)
	
        
        
#Cam_GUI()

