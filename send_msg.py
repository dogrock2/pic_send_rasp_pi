from twilio.rest import Client
from admin_db import work_admin_db
from requests import get

# Uses the twilio API to send a text message.


def send_twilio_msg(dest):  
      
    msg = "Multimedia txt msg from Raspberry Pi 4."
    media_url = "/home/pi/Desktop/4pi/pics/picture.jpg"
    myIP = get('https://api.ipify.org').text    

    db_data = work_admin_db().get_all_db()  
    account_sid = db_data[0][10]
    auth_token = db_data[0][12]
    phone = db_data[0][11]

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+"+str(dest),
        from_="+"+str(phone),
        body=msg,
        media_url=myIP+media_url)


