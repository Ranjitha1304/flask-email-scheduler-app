import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, message):
    sender_email = 'ranjitha13cs@gmail.com'
    password = 'iixy zrjl wzbc vqtk'  # App password or real password

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)
            print(f'Email sent to {to_email}')
    except Exception as e:
        print(f'Error sending email: {e}')
