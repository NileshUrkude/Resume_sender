import os
import re
import smtplib
from email.message import EmailMessage
from pathlib import Path


DEFAULT_SUBJECT = "Application for Python FullStack Developer - Immediate Joiner"
DEFAULT_ATTACHMENT = Path(__file__).with_name("resume.pdf")
DEFAULT_SENDER = os.environ.get("RESUME_SENDER_EMAIL")
SMTP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
DRY_RUN = False
DEFAULT_RECIPIENTS = os.environ.get("RESUME_RECIPIENTS", "")    # add recipients mails here


def parse_recipients(value):
   recipients = [item.strip() for item in re.split(r"[,\n]", value) if item.strip()]
   if not recipients:
      raise ValueError("At least one recipient email address is required")
   return recipients


def is_valid_email(address):
   return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", address))


def build_message(sender_email, recipient, subject, body, attachment_path):
   message = EmailMessage()
   message["From"] = sender_email
   message["To"] = recipient
   message["Subject"] = subject
   message.set_content(body)
   message.add_attachment(
      attachment_path.read_bytes(),
      maintype="application",
      subtype="pdf",
      filename=attachment_path.name,
   )
   return message


def recipient_is_accepted(smtp, sender_email, recipient):
   smtp.mail(sender_email)
   response_code, _ = smtp.rcpt(recipient)
   return response_code in (250, 251)


def send_emails(sender_email, recipients, subject, body, attachment_path, password, dry_run=False):
   if not attachment_path.is_file():
      raise FileNotFoundError(f"Attachment not found: {attachment_path}")

   valid_recipients = []
   for recipient in recipients:
      if is_valid_email(recipient):
         valid_recipients.append(recipient)
      else:
         print(f"Mail not found (invalid address): {recipient}")

   if not valid_recipients:
      print("No valid email addresses to send")
      return

   if dry_run:
      print(f"Dry run: would send to {', '.join(valid_recipients)}")
      print(f"Attachment: {attachment_path} ({attachment_path.stat().st_size} bytes)")
      return

   smtp = None
   connection_errors = []
   for connection_mode in ("starttls", "ssl"):
      try:
         if connection_mode == "starttls":
            smtp = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
         else:
            smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30)
            smtp.ehlo()
         smtp.login(sender_email, password)
         break
      except (OSError, smtplib.SMTPException) as error:
         connection_errors.append(f"{connection_mode}: {error}")
         if smtp is not None:
            smtp.close()
         smtp = None

   if smtp is None:
      raise smtplib.SMTPException(
         "Gmail connection/login failed. " + " | ".join(connection_errors)
      )

   try:
      for recipient in valid_recipients:
         try:
            if not recipient_is_accepted(smtp, sender_email, recipient):
               print(f"Mail not found: {recipient}")
               continue
         except smtplib.SMTPRecipientsRefused:
            print(f"Mail not found: {recipient}")
            continue

         message = build_message(sender_email, recipient, subject, body, attachment_path)
         try:
            refused = smtp.send_message(message)
            if refused:
               print(f"Mail not found: {recipient}")
            else:
               print(f"Successfully sent email to {recipient}")
         except smtplib.SMTPRecipientsRefused:
            print(f"Mail not found: {recipient}")
   finally:
      smtp.quit()

# Content of the email
# add here body of mail
EMAIL_BODY = """
# add here body of mail
"""
def main():
   if not SMTP_PASSWORD:
      raise SystemExit("Set the GMAIL_APP_PASSWORD environment variable to your Gmail App Password.")
   try:
      send_emails(
         DEFAULT_SENDER,
         parse_recipients(DEFAULT_RECIPIENTS),
         DEFAULT_SUBJECT,
         EMAIL_BODY.strip(),
         DEFAULT_ATTACHMENT,
         SMTP_PASSWORD,
         DRY_RUN,
      )
   except (OSError, ValueError, smtplib.SMTPException) as error:
      raise SystemExit(f"Unable to send email: {error}") from error


if __name__ == "__main__":
   main()
