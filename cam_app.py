
from picamera import PiCamera
from time import sleep
from io import BytesIO
from PIL import Image
from cam_db import work_cam_db



class cam_view():
	
	def __init__(self):
		self.rec = work_cam_db().get_all_db()
		self.stream = BytesIO()
		self.camera = PiCamera()
		self.x = self.rec[0][1]
		self.y = self.rec[0][2]
		self.width = self.rec[0][3]
		self.height = self.rec[0][4]
		self.start_cam()		
		
	def start_cam(self):		
		self.camera.start_preview(fullscreen=False, window=(self.x, self.y, self.width, self.height))		
		self.camera.capture(self.stream, format='jpeg')
		self.stream.seek(0)
		image = Image.open(self.stream)		

	def stop_cam(self):
    		self.camera.stop_preview()
	
	def take_pic(self):
    		self.camera.capture('/home/pi/Desktop/4pi/pics/picture.jpg')
#cam_view()

