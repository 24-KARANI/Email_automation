import os
import email
import imaplib

from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = os.getenv("IMAP_SERVER")

def delete_emails(folder, search_criteria):
    """Delete emails from a folder based on search criteria."""
    
    if IMAP_SERVER is None or EMAIL_USER is None or EMAIL_PASS is None:
        raise ValueError("EMAIL_USER and EMAIL_PASS environment variables must be set.")

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    folder_selected = False

    try:
        status, _ = mail.select(f'"{folder}"')
        if  status != "OK":
            print(f"Could not open folder: {folder}")
            return
        
        folder_selected = True

        status, messages = mail.search(None, search_criteria)
        if status != "OK":
            print(f"Error searching folder: {folder}")

        email_ids = messages[0].split()
        print(f"{folder} - Found {len(email_ids)} emails to delete.")

        deleted_emails = []
        for num in email_ids:
            res, msg_data = mail.fetch(num, "(RFC822)")
            if res != "OK" or not msg_data or not isinstance(msg_data[0], tuple) or not isinstance(msg_data[0][1], (bytes, bytearray)):
                continue

            msg = email.message_from_bytes(msg_data[0][1])
            subject_header = msg["Subject"]
            if subject_header is None:
                subject = "(No Subject)"
            else:
                decoded = decode_header(subject_header)
                if decoded and decoded[0]:
                    subject, encoding = decoded[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8", errors="ignore")
                else:
                    subject = "(Unable to decode subject)"

            from_ = msg.get("From")
            date_ = msg.get("Date")
            print(f"Deleting: {subject} - From: {from_} in: {folder}")

            mail.store(num, '+FLAGS', '\\Deleted')
            deleted_emails.append(f"From: {from_}\nSubject: {subject}\nDate: {date_}\n{'-'*50}\n")

        if deleted_emails:
            with open("deleted_emails_log.txt", "w", encoding="utf-8") as f:
                f.writelines(deleted_emails)
        
        if folder_selected:
            mail.expunge()
            print(f"Deletion complete for {folder}.\n")

    finally:
        if folder_selected:
           mail.close()
           mail.logout()

folders = [
    "[Gmail]/Spam",
    "[Gmail]/Drafts",
    "[Gmail]/Bin",
    "[Gmail]/Important",
    "[Gmail]/All Mail",
    "[Gmail]/Sent Mail"
]
primary_folder = "INBOX"

if __name__=="__main__":

    delete_emails(primary_folder, "UNFLAGGED")

    for folder in folders:
        delete_emails(folder, "ALL")
