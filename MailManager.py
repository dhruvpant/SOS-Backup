import smtplib
from XmlManager import XmlManager

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from LogManager import Log
#### Initializations ####
# Initializing logging
logger = Log.initialize('MailManager')

def send(message, status):
    SMTP_HOST = XmlManager.primaryConfig["smtpHost"]
    SMTP_PORT = XmlManager.primaryConfig["smtpPort"]
    DEBUG_STATUS = False
    SENDER = XmlManager.primaryConfig["JarvisEmail"]
    RECEIVER = XmlManager.primaryConfig["PrimaryCustEmail"]
    PASSWORD = XmlManager.primaryConfig["JarvisPasscode"]
    SUBJECT = XmlManager.primaryConfig["NotificationEmailSubject"]
    try:
        # creates SMTP session
        s = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        # start TLS for security
        s.starttls()
        s.ehlo()
        # Switch to enable / disable debugging
        s.set_debuglevel(DEBUG_STATUS)
        # Authentication
        s.login(SENDER, PASSWORD)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = SUBJECT+" - "+status
        msg['From'] = SENDER
        msg['To'] = RECEIVER

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(message, 'plain')
        part2 = MIMEText(message, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)
        # sending the mail
        s.sendmail(SENDER, RECEIVER, msg.as_string())
    except Exception as err:
        logger.error(err)
    finally:
        # terminating the session
        s.quit()
