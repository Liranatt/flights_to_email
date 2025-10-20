# In SEND_EMAIL.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import CONFIG

def send_html_email(html_content):
    """Sends an email with the report formatted as an HTML table in the body."""
    print("Preparing to send HTML email...")
    msg = MIMEMultipart()
    msg['From'] = CONFIG.SENDER_EMAIL
    msg['To'] = CONFIG.RECEIVER_EMAIL
    msg['Subject'] = "Weekly Flight Summary Report"

    # Attach the HTML content, specifying the subtype as 'html'
    msg.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP(CONFIG.SMTP_SERVER, CONFIG.SMTP_PORT)
        server.starttls()
        server.login(CONFIG.SENDER_EMAIL, CONFIG.EMAIL_PASSWORD)
        server.sendmail(CONFIG.SENDER_EMAIL, CONFIG.RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("HTML Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
