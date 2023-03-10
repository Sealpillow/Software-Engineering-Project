import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

# Your email account credentials
def main(user_email,newPassword):
    username = "OnlyFlats@hotmail.com"
    password = "iloveNTU2!"

    # Sender's name and email address
    sender_name = 'OnlyFlats'
    sender_email = 'OnlyFlats@hotmail.com'

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
        smtp.login(username, password)

        # Send the email
        smtp.sendmail(sender_email, recipient_email, msg.as_string())
        print("sent")
        smtp.quit()

if __name__ == "__main__":
    main()