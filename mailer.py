import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import mimetypes

# Load environment variables
load_dotenv()

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
GMAIL_ADDRESS = os.getenv('GMAIL_ADDRESS')
APP_PASSWORD = os.getenv('APP_PASSWORD')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')

ATTACHMENTS_FOLDER = 'attachments'  # Folder name

def load_attachments():
    attachments = []

    # Check if folder exists, if not create it
    if not os.path.exists(ATTACHMENTS_FOLDER):
        os.makedirs(ATTACHMENTS_FOLDER)
        print(f"[INFO] Attachments folder '{ATTACHMENTS_FOLDER}' created (it was missing).")

    # Now load all files inside the folder
    for filename in os.listdir(ATTACHMENTS_FOLDER):
        file_path = os.path.join(ATTACHMENTS_FOLDER, filename)
        if os.path.isfile(file_path):
            attachments.append(file_path)

    return attachments

def send_email(body, subject):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = GMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL
    msg.set_content(body)

    # Attach files
    attachments = load_attachments()
    for file_path in attachments:
        try:
            ctype, encoding = mimetypes.guess_type(file_path)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)

            with open(file_path, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(file_path)
                msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)
            
            print(f"[INFO] Attached file: {file_name}")
        except Exception as e:
            print(f"[ERROR] Failed to attach {file_path}: {e}")

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(GMAIL_ADDRESS, APP_PASSWORD)
        server.send_message(msg)

    print("[SUCCESS] Email sent successfully with attachments!")
