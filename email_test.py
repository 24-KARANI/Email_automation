import imaplib
import email
from email.header import decode_header

from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = os.getenv("IMAP_SERVER")


def list_unread_emails(folder="INBOX"):
    """List unread emails in the given folder."""
    
    if EMAIL_USER is None or EMAIL_PASS is None or IMAP_SERVER is None:
        raise ValueError("EMAIL_USER and EMAIL_PASS environment variables must be set.")
    
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)

    try:
        # Select folder in readonly mode
        status, _ = mail.select(folder, readonly=True)
        if status != "OK":
            print(f" Could not open folder: {folder}")
            return

        status, messages = mail.search(None, "UNSEEN")
        if status != "OK":
            print("Error searching inbox.")
            return

        email_ids = messages[0].split()
        print(f" Folder: {folder} — Found {len(email_ids)} unread emails.\n")
        
        log_lines = []
        
        for num in email_ids:
            res, msg_data = mail.fetch(num, "(RFC822)")
            if res != "OK" or not msg_data or not isinstance(msg_data[0], tuple) or not isinstance(msg_data[0][1], (bytes, bytearray)):
                continue

            msg = email.message_from_bytes(msg_data[0][1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")

            from_ = msg.get("From")
            date_ = msg.get("Date")

            print(f"From: {from_}\nSubject: {subject}\nDate: {date_}\n{'-'*50}\n")

    finally:
        mail.close()
        mail.logout()
        
if __name__=="__main__":
    list_unread_emails()