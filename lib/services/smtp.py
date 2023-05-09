import os.path
import smtplib
from email.mime.text import MIMEText

import jinja2

from lib import config

jEnvironmanet = jinja2.Environment(loader=jinja2.FileSystemLoader("./assets/templates"))
jTemplate = jEnvironmanet.get_template("email.html")


def send_otp_email(otp, recipient):
    sender = "bcsm-s19-043@superior.edu.pk"

    msg = MIMEText(
        jTemplate.render(
            title="OTP Request",
            message=f"Here is your OTP for Better Boiler: {otp}. Please contact support if this was not intentional.",
        ),
        "html",
    )
    msg["Subject"] = "OTP | Better Boiler"
    msg["From"] = sender
    msg["To"] = recipient
    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp_server.login(sender, config.SMTP_PWD)
    smtp_server.sendmail(sender, recipient, msg.as_string())
    smtp_server.quit()


def send_verification_support_email(ticket_id, recipient):
    sender = "bcsm-s19-043@superior.edu.pk"

    msg = MIMEText(
        jTemplate.render(
            title="Better Boiler",
            message=f"Your request for support has been created. Your ticket ID is {ticket_id}. We will get back to you as soon as possible.",
        ),
        "html",
    )
    msg["Subject"] = "Support Request | Better Boiler"
    msg["From"] = sender
    msg["To"] = recipient
    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp_server.login(sender, config.SMTP_PWD)
    smtp_server.sendmail(sender, recipient, msg.as_string())
    smtp_server.quit()
