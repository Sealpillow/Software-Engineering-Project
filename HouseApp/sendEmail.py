import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from dotenv import load_dotenv
load_dotenv()


# Your email account credentials
def main(user_email, newPassword):
    """
    This is the main function of the script.

    This function sends an email containing a new password to the user's email using the company's email

    Args:
        user_email (str): Description of arg1.
        newPassword (str): Description of arg2.
    """

    # Sender's name and email address
    sender_name = os.getenv('sender_name')
    sender_email = os.getenv('sender_email')
    sender_password = os.getenv('sender_password')

    # Recipient's email address
    recipient_email = user_email

    # Create a message object
    msg = MIMEMultipart()
    msg['From'] = formataddr((sender_name, sender_email))
    msg['To'] = recipient_email
    msg['Subject'] = 'Password Reset Request'

    # Add body to the message
    body = 'Hello,\n\nThis is your new password: ' + newPassword
    msg.attach(MIMEText(body, 'plain'))

    # Connect to Gmail SMTP server
    with smtplib.SMTP('smtp.office365.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)

        # Send the email
        smtp.sendmail(sender_email, recipient_email, msg.as_string())
        print("sent")
        smtp.quit()


if __name__ == "__main__":
    main()
