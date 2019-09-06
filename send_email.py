import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Uses gmail acct to send emails.

EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']  # gets email password store in an env variable.

def send_msg(emailTo):

    EMAIL_FROM = "anieves80@gmail.com"
    multimedia_file = "/home/pi/Desktop/4pi/pics/picture.jpg"
    msg = MIMEMultipart()
    msg['Subject'] = "Picture Message"
    msg['From'] = EMAIL_FROM    
    msg['To'] = emailTo

    msg.attach(MIMEText("A multimedia message from the Raspberry Pi 4", 'plain'))

    filename = os.path.basename(multimedia_file)
    attachment = open(multimedia_file, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
        smtp.send_message(msg)

    

