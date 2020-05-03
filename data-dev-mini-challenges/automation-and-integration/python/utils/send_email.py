# ----------------------------------------------------------------------------
from credentials import email as creds

import email, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# ----------------------------------------------------------------------------
def send(recipient, subject, message):
    sender_email = creds.email_address
    password = creds.password

    receiver_email = recipient

    email = MIMEMultipart()

    email['From'] = sender_email
    email['To'] = receiver_email 
    email['Subject'] = subject

    body = message
    email.attach(MIMEText(body, 'plain'))

    # Use gmail with port
    session = smtplib.SMTP('smtp.gmail.com', 587) 
    # Enable security
    session.starttls() 
    # Login with mail_id and password
    session.login(sender_email, password) 
    # Send email
    session.sendmail(sender_email, receiver_email, email.as_string())

    session.quit()
    
# ----------------------------------------------------------------------------
# The above code is tweaked from an original blog post on Towards Data Science:
# Blog link: https://towardsdatascience.com/email-automation-with-python-72c6da5eef52