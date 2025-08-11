Email Deletion Script
This Python script connects to an email account via IMAP and deletes messages from specific folders based on search criteria.
It supports logging of deleted emails for reference.

📌 Features
Connects securely to an email server using IMAP over SSL.

Deletes emails from:

Primary inbox (only unstarred/unflagged emails)

Gmail folders such as Spam, Drafts, Bin, Important, All Mail, Sent Mail.

Logs details of deleted emails (From, Subject, Date) into a local text file.

Handles email subject decoding safely.

Reads credentials from an .env file for security.

📂 Folder Deletion Logic
Primary Folder (INBOX) → Deletes only UNFLAGGED (unstarred) emails.

Other Gmail folders → Deletes ALL emails.

🔧 Requirements
Python 3.8+

Gmail account with IMAP enabled.

Less secure app access or an App Password (for Gmail with 2FA enabled).

The following Python packages:

bash
Copy
Edit
pip install python-dotenv
📄 Environment Variables
Create a .env file in the same directory as the script:

env
Copy
Edit
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_password_or_app_password
IMAP_SERVER=imap.gmail.com
⚠️ Security Note: Use an App Password if your account has 2FA enabled.
Never commit .env files to version control.

▶️ How to Run
bash
Copy
Edit
python delete_emails.py
The script will:

Connect to the specified IMAP server.

Delete unstarred emails from the INBOX.

Delete all emails from the predefined Gmail folders.

Save deleted email details to deleted_emails_log.txt.

📝 Log File
deleted_emails_log.txt will contain a list of deleted messages:

sql
Copy
Edit
From: sender@example.com
Subject: Example Subject
Date: Mon, 10 Aug 2025 12:34:56 +0000

---

⚠️ Disclaimer
This script permanently deletes emails from your account.
Use with caution and test on a secondary account before running on your main inbox.
