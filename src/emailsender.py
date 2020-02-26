#!/usr/bin/python3

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import ssl
import configparser
from datetime import datetime

class EmailSender:

    credentials  = 'credentials'
    passwordStr  = 'password'
    smtpStr      = "smtp"
    portStr      = "port"
    senderStr    = "sender"

    target       = "target"
    recipientStr = "recipient"
    subjectStr   = "subject"

    """

    """
    def __init__(self, filename):
        config = self.getEmailConfig(filename)
        self.password = config.get(self.credentials, self.passwordStr)
        self.smtp = config.get(self.credentials, self.smtpStr)
        self.port = config.get(self.credentials, self.portStr)
        self.sender = config.get(self.credentials, self.senderStr)

        self.recipient = config.get(self.target, self.recipientStr)
        self.subject = config.get(self.target, self.subjectStr)

    """
    """
    def getEmailConfig(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)
        return config


    """
    """
    def sendEmail(self, filename):
        # Create e-mail message
        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = self.recipient
        msg["Subject"] = self.subject

        body = "Picture taken! at {}".format(datetime.now())
        msg.attach(MIMEText(body, "plain"))

        # Process attachment
        attachment = open(filename, "rb")
        payload = MIMEBase("image", "jpeg")
        payload.set_payload((attachment).read())
        encoders.encode_base64(payload)


        # Add header to payload
        payload.add_header("Content-Disposition", "attachment; filemane={}".format(filename))

        # Attach payload to message
        msg.attach(payload)

        context = ssl.create_default_context()

        # Send message
        smtp = smtplib.SMTP(self.smtp, self.port)
        smtp.ehlo()
        smtp.starttls(context = context)
        smtp.login(self.sender, self.password)
        smtp.sendmail(self.sender, self.recipient, msg.as_string())
        smtp.quit()
        print("-> Email sent")
