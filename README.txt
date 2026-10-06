Resume Sender - Windows Setup

Files to include in the ZIP
- resume_sender.py
- 2_Fullstack resume.pdf
- README.txt

Do not include the venv or __pycache__ folders. Keep the PDF in the same
folder as resume_sender.py; the script expects its exact filename above.

On the other desktop
1. Install Python
2. Extract the ZIP to a folder.
3. Open PowerShell in that folder.
4. Set the recipient list and Gmail App Password for this PowerShell window:

   $env:RESUME_RECIPIENTS = "person@example.com,another@example.com"
   $env:GMAIL_APP_PASSWORD = "your-16-character-app-password"

   Optionally override the sender address:

   $env:RESUME_SENDER_EMAIL = "your-gmail-address@gmail.com"

5. Run the script:

   python resume_sender.py

The script uses only Python's standard library, so no packages need to be
installed with pip. 

How to get the Gmail SMTP password (App Password)
1. Sign in to the Google Account for the Gmail address you will send from.
2. Open https://myaccount.google.com/security.
3. Under "How you sign in to Google", turn on 2-Step Verification if it is
   not already enabled. Follow Google's prompts to finish setup.
4. Open https://myaccount.google.com/apppasswords.
5. If prompted, sign in again. Enter an identifying name such as "Resume
   Sender" and create the app password.
6. Copy the generated 16-character password. Use it as GMAIL_APP_PASSWORD
   in the PowerShell commands above. Enter the characters without spaces.

Use this App Password only; do not use your regular Gmail password. Do not put
the App Password in the ZIP, README, or script, and do not share it. If the
App Passwords page is unavailable, the Google Account may not support App
Passwords (for example, some work or school accounts or accounts with
Advanced Protection).

The environment variables above apply only to the current PowerShell window.
Set them again in a new window. To test without sending, change DRY_RUN to True
near the top of resume_sender.py, then change it back to False when ready.
