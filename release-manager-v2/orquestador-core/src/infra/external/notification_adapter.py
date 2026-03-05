import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from domain.interfaces.services import INotificationService
from typing import List
import os

class EmailNotificationAdapter(INotificationService):
    def send_release_report(self, recipients: List[str], report_data: dict):
        smtp_server = os.getenv("SMTP_SERVER", "localhost")
        smtp_port = int(os.getenv("SMTP_PORT", "1025"))
        sender_email = os.getenv("SENDER_EMAIL", "release-manager@example.com")

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = f"Release Report: {report_data.get('release_id')}"

        body = f"Release Process Finished\n\n"
        body += f"Status: {report_data.get('status')}\n"
        body += "Generated PRs:\n"
        for pr in report_data.get('pr_links', []):
            body += f"- {pr}\n"
        
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.send_message(msg)
        except Exception as e:
            print(f"Failed to send email: {e}")
