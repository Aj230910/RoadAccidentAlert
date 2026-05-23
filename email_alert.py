import os
import smtplib
import logging
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# Load environment variables
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")  # can be comma-separated

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465


def validate_config():
    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
        raise ValueError("Missing email configuration in environment variables")


def build_email(subject: str, body: str, image_path: str = None) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject

    html_body = f"""
    <html>
      <body style="font-family: Arial;">
        <h2 style="color:red;">🚨 Road Accident Detected!</h2>
        <p><b>Immediate action required.</b></p>
        <p>{body.replace(chr(10), "<br>")}</p>
      </body>
    </html>
    """

    msg.attach(MIMEText(html_body, "html"))

    # Attach image properly
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, "rb") as img:
                img_data = img.read()
                image = MIMEImage(img_data)
                image.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{os.path.basename(image_path)}"'
                )
                msg.attach(image)
        except Exception as e:
            logging.warning(f"Image attachment failed: {e}")

    return msg


def send_email_alert(subject: str, body: str, image_path: str = None):
    try:
        validate_config()

        msg = build_email(subject, body, image_path)

        recipients = [email.strip() for email in RECEIVER_EMAIL.split(",")]

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipients, msg.as_string())

        logging.info("✅ Alert email sent successfully")

    except smtplib.SMTPAuthenticationError:
        logging.error("❌ Authentication failed. Check email/password or App Password.")
    except Exception as e:
        logging.error(f"❌ Failed to send email: {e}")
