from flask import current_app
import smtplib
from email.message import EmailMessage
from app import mail

EMAIL_ADDRESS = "rochesterprojects@gmail.com"
EMAIL_PASSWORD = "csc210final"

def sendEmail(to, subject, template):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to
    msg.set_content('HTML failed to load.')
    msg.add_alternative(template, subtype='html')

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)