import smtplib
from email.mime.text import MIMEText

from lib import config


def send_otp_email(otp, recipient):
    sender = 'bcsm-s19-043@superior.edu.pk'

    msg = MIMEText(f'OTP: {otp}')
    msg['Subject'] = 'OTP | Trade Quotes'
    msg['From'] = sender
    msg['To'] = recipient
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, config.SMTP_PWD)
    smtp_server.sendmail(sender, recipient, msg.as_string())
    smtp_server.quit()
