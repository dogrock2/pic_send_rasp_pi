import PySimpleGUI as sg
from tkinter import messagebox
from profiles_db import work_profiles_db


class Profiles_DBviewer():
	
	def __init__(self):

		# Variables for the table.
		self.data = []
		self.header_list = [['ID'],['FNAME'],['LNAME'],['PHONE'],['EMAIL'],['COMMS']]

		# Sets all the components for form.
		self.radio_column = [[sg.Radio('Add', "Radio", default=True, size=(10,1), key="radio_add", enable_events=True)],
         	    	         [sg.Radio('Modify', "Radio", default=False, size=(10,1), key="radio_mod", enable_events=True)],
            	             [sg.Radio('Delete', "Radio", default=False, size=(10,1), key="radio_del", enable_events=True)]]
		
		self.frm_column = [[sg.Text('Lname'),sg.Input(size=(12,1), key="lname_txt"),sg.Text('Fname'),sg.Input(size=(12,1), key="fname_txt")],      
        		           [sg.Text('ID       '),sg.Input(size=(12,1), key="id_txt", disabled=True, default_text=" auto"),sg.Text('Email  '),sg.Input(size=(12,1), key="email_txt")],      
              		       [sg.Text('Phone'),sg.Input(size=(12,1), key="phone_txt"),sg.Text('Comms'),sg.InputCombo(('SMS', 'Email', 'SMS/Email', 'N/A'), size=(10, 1), key="comms_txt", default_value="N/A")]]
		
		self.main_table = [sg.Table(values=self.data,
					             enable_events=True,
						         headings=self.header_list,
								 max_col_width=25,
								 auto_size_columns=True,
								 justification='right',
								 key="table_data",
								 alternating_row_color='lightblue',
                                 num_rows=min(10, 20))]

		self.layout = [[sg.Column(self.frm_column),sg.Column(self.radio_column)],
					   [sg.Button(button_text="Submit", pad=(90,0)), sg.Button(button_text="Clear")],
					   self.main_table
					    ]

		# Calls the function to open the window with all the components.
		self.get_all_dbData()
		self.create_gui()


	def create_gui(self):
		window = sg.Window('Profiles Database', grab_anywhere=False).Layout(self.layout) # Creates the window/GUI		
		self.win = window

		while True:						
			event, values = window.Read()
			# Exits the program by breaking the loop.		
			if event in (None, 'Exit'):
				break

			# Grabs the index of the row that was clicked in the table
			# and sends the number over to function to fill the form.
			if event == 'table_data':								
				data_selected = self.data[values['table_data'][0]]
				self.set_txtbox_data(window, data_selected)
			
			# Clears out and defaults the form. If radio button delete is selected 
			# then clears out the id field too otherwise says auto.
			if event == 'Clear':
				if values['radio_del']:
					self.set_txtbox_data(window, ['','','','','','N/A'])
				else:
					self.set_txtbox_data(window, [' auto','','','','','N/A'])
			
			# When submit button is clicked it gets the radio button currently selected and calls
			# the appropiate function to either add, modify or delete.
			if event == 'Submit':
				option_selected = (values['radio_add'], values['radio_mod'], values['radio_del'])
				queries_dic = (self.add_query, self.mod_query, self.del_query)
				for x in range(3):					
					if option_selected[x]:
						queries_dic[x](window, values)

			# When radio button delete gets selected then id will be enabled otherwise stays disabled.
			if event == "radio_del":
				self.set_txtbox_data(window, ['','','','','','N/A'])
				window.Element('id_txt').Update("")
				window.Element('id_txt').Update(disabled=False)

			# When radio any button other than delete gets selected then id will be disabled with text set to string auto.
			if event == "radio_add":
				self.set_txtbox_data(window, ['','','','','','N/A'])
				window.Element('id_txt').Update(" auto")
				window.Element('id_txt').Update(disabled=True)

			if event == "radio_mod":
				self.set_txtbox_data(window, ['','','','','','N/A'])
				window.Element('id_txt').Update(disabled=True)
			
		window.Close() # Ends the program


	# Grabs all the data from the database and sends the result to the database_tables function.
	def get_all_dbData(self):		
		prof_db = work_profiles_db().search_all_db
		self.database_tables(prof_db())
		
	
	# Stores data in the data array variable thats used as values to display in table.
	def database_tables(self, data):		
		rows_cnt = len(data)						
		for i in range(rows_cnt):
			result = [] 			
			for j in range(6):
				result.append(data[i][j])
			self.data.append(result)
		

	# Updates all the data in the table.
	def update_table(self, win):	
		win.Element('table_data').Update("")
		self.data = []
		self.get_all_dbData()		
		win.Element('table_data').Update(self.data)

						        
	# Sets the  data in the text boxes when the table gets clicked.
	# Also used to clear the form.
	def set_txtbox_data(self, win, values):		
		win.Element('id_txt').Update(values[0])
		win.Element('fname_txt').Update(values[1])
		win.Element('lname_txt').Update(values[2])
		win.Element('phone_txt').Update(values[3])
		win.Element('email_txt').Update(values[4])
		win.Element('comms_txt').Update(values[5])
	

	# Performs form validation.
	def validate_data(self, win, values):
		ok_pass = True
		comms = values['comms_txt']
		fname = values['fname_txt']
		lname = values['lname_txt']
		email = values['email_txt']

		try:
			phone = int(values['phone_txt'])
		except:
			self.display_err("Only numbers in the phone# field or put just a zero.")
			win.Element('phone_txt').Update("")
			return False

		#############################################################################
		###################### FORM VALIDATION ######################################
		#***************************************************************************#
		
		if comms == "SMS":
			if not phone:
				self.display_err("You selected SMS. Phone# box cannot be blank.")
				ok_pass = False

		if comms == "Email":
			if not email:
				self.display_err("You selected Email. Email box cannot be blank.")
				ok_pass = False

		if comms == "SMS/Email":
			if not phone or not email:
				self.display_err("You selected SMS/Email. Neither Phone# nor the Email box can be blank.")
				ok_pass = False
		
		if not fname or not lname:
			self.display_err("Neither first name or last name can be blank.")
			ok_pass = False
		##############################################################################

		if ok_pass:
			return True

		return False
	

	# Runs the Query to add to db.
	def add_query(self, win, values):
		comms = values['comms_txt']
		fname = values['fname_txt']
		lname = values['lname_txt']
		email = values['email_txt']
		phone = values['phone_txt']
		
		res = self.validate_data(win, values)
		
		if res:
			MsgBox = self.msg_confirmation('Verification!', 'Are you sure you want to ADD this information?', 'question')			
			if MsgBox == "yes":				
				qry = "INSERT INTO Profiles_Table (fname, lname, phone, email, comms) VALUES ('"+fname+"','"+lname+"',"+str(phone)+",'"+email+"','"+comms+"')"
				work_profiles_db().execute_query_db(qry)
				self.set_txtbox_data(win, [' auto','','','','','N/A'])
				self.update_table(win)

	
	
	# Runs the query to del from the db.
	def del_query(self, win, values):
		print("Delete Query")
		id = phone = values['id_txt']
		if not id:
			display_err("ID cannot be blank.")
		else:
			MsgBox = self.msg_confirmation('Warning!', 'Are you sure you want DELETE this record?', 'warning')			
			if MsgBox == "yes":	
				qry = "DELETE from Profiles_Table WHERE id = "+id
				work_profiles_db().execute_query_db(qry)	
				self.set_txtbox_data(win, ['','','','','','N/A'])
				self.update_table(win)
	
	
	# Runs the query to modify a record in the db.
	def mod_query(self, win, values):
		comms = values['comms_txt']
		fname = values['fname_txt']
		lname = values['lname_txt']
		email = values['email_txt']
		phone = values['phone_txt']
		id = values['id_txt']
		
		res = self.validate_data(win, values)

		MsgBox = self.msg_confirmation('Verification!', 'Are you sure you want UPDATE this record?', 'question')			
		if MsgBox == "yes":
			qry = "UPDATE Profiles_Table SET fname = '"+fname+"', lname = '"+lname+"', phone = "+phone+", email = '"+email+"', comms = '"+comms+"' WHERE id = "+id+""
			work_profiles_db().execute_query_db(qry)
			self.set_txtbox_data(win, ['','','','','','N/A'])
			self.update_table(win)


	# Message/Question for confirmation. Returns Yes or No.
	def msg_confirmation(self, _type, msg, _icon):		
		return messagebox.askquestion(_type, msg, icon=_icon)
		

	# Displays error messages.
	def display_err(self, msg):
		messagebox.showerror("Error", msg)
		# sg.PopupError('ERROR', msg)



