import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def send_email_alert(subject, body, image_path=None):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = subject

        # ✅ HTML Email Body
        html_body = f"""
        <html>
          <body>
            <h2 style="color:red;">🚨 Road Accident Detected!</h2>
            <p><b>Immediate action required.</b></p>
            <p>{body.replace(chr(10), "<br>")}</p>
          </body>
        </html>
        """
        msg.attach(MIMEText(html_body, "html"))

        # ✅ Attach snapshot if available
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                mime = MIMEBase("application", "octet-stream")
                mime.set_payload(f.read())
                encoders.encode_base64(mime)
                mime.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{os.path.basename(image_path)}"',
                )
                msg.attach(mime)

        # ✅ Gmail SSL
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()

        print("✅ Alert Email with snapshot sent!")

    except Exception as e:
        print("❌ Email Error:", e)
