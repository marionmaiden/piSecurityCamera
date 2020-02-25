#!/usr/bin/python3

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from configparser import RawConfigParser
from datetime import datetime

class EmailSend:

    credentials  = "credentials"
    passwordStr  = "password"
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
        self.password = config.read(self.credentials, self.passwordStr)
        self.smtp = config.read(self.credentials, self.smtpStr)
        self.port = config.read(self.credentials, self.portStr)
        self.sender = config.read(self.credentials, self.senderStr)

        self.recipient = config.read(self.target, self.recipientStr)
        self.subject = config.read(self.target, self.subjectStr)

    """
    """
    def getEmailConfig(self, filename):
        config = RawConfigParser()
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

        print(self.smtp)
        print(self.port)

        # Send message
        smtp = smtplib.SMTP(self.smtp, self.port)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(self.sender, self.password)
        smtp.sendmail(self.sender, self.recipient, msg.as_string())
        smtp.quit()
        print("-> Email sent")
