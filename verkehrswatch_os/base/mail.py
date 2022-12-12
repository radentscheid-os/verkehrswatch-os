
import smtplib, ssl
from base import config as c


def send_email(message):
    # Create a secure SSL context
    
    ssl.create_default_context()
    server = None
    try:
        server = smtplib.SMTP(c.SMTP_SERVER,c.SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(c.SENDER_EMAIL, c.EMAIL_PASSWORD)
        server.sendmail(c.SENDER_EMAIL, c.DEFAULT_RECEIVER_EMAIL, message)
    except Exception as e:
        print(e)
    finally:
        server.quit() 
