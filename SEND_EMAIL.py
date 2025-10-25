# In SEND_EMAIL.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import CONFIG

# MODIFIED: This function now accepts the list of recipients
def send_html_email(html_content, receiver_emails_list):
    """Sends an email with the report formatted as an HTML table in the body."""

    # Ensure it's a list, even if just one email
    if not isinstance(receiver_emails_list, list):
        receiver_emails_list = [receiver_emails_list]

    print(f"Preparing to send HTML email to: {', '.join(receiver_emails_list)}")
    msg = MIMEMultipart()
    msg['From'] = CONFIG.SENDER_EMAIL
    # MODIFIED: Join the list of emails for the 'To' header
    msg['To'] = ", ".join(receiver_emails_list)
    msg['Subject'] = "Your Custom Flight Summary Report"

    # Attach the HTML content, specifying the subtype as 'html'
    msg.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP(CONFIG.SMTP_SERVER, CONFIG.SMTP_PORT)
        server.starttls()
        server.login(CONFIG.SENDER_EMAIL, CONFIG.EMAIL_PASSWORD)
        # MODIFIED: Send to the list of recipients
        server.sendmail(CONFIG.SENDER_EMAIL, receiver_emails_list, msg.as_string())
        server.quit()
        print("HTML Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise e
