import imaplib
import email
from email.header import decode_header

from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

if EMAIL_USER is None or EMAIL_PASS is None:
	raise ValueError("EMAIL_USER and EMAIL_PASS environment variables must be set.")

# Connect to IMAP server
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(EMAIL_USER, EMAIL_PASS)
mail.select("INBOX", readonly=True)

status, messages = mail.search(None, 'UNSEEN')

if status == "OK":
	email_ids = messages[0].split()
	print(f"Found {len(email_ids)} matching emails.")

	log_lines = []
	for num in email_ids:
		# Fetch email by ID
		res, msg_data = mail.fetch(num, "(RFC822)")
		if res != "OK":
			continue

		# Parse the raw email
		if msg_data and isinstance(msg_data[0], tuple) and isinstance(msg_data[0][1], (bytes, bytearray)):
			msg = email.message_from_bytes(msg_data[0][1])
		else:
			print(f"Failed to parse email with ID {num}: unexpected fetch result.")
			continue
		
		# Decode subject
		subject, encoding = decode_header(msg["Subject"])[0]
		if isinstance(subject, bytes):
			subject = subject.decode(encoding if encoding else "utf-8")

		# From field
		from_ = msg.get("From")

		# Date field
		date_ = msg.get("Date")

		print(f"From: {from_}\nSubject: {subject}\nDate: {date_}\n{'-'*50}")

		# Save to log
		log_lines.append(f"From: {from_}\nSubject: {subject}\nDate: {date_}\n{'-'*50}")

	with open("email_log.txt", "w", encoding="utf-8") as f:
		f.writelines(log_lines)

else: 
	print("Error searching inbox.")
	
mail.close()
mail.logout()