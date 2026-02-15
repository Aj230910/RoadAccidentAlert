import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

def send_sms(message):
    try:
        client = Client(
            os.getenv("TWILIO_SID"),
            os.getenv("TWILIO_AUTH")
        )

        message = client.messages.create(
            body=message,
            from_=os.getenv("TWILIO_PHONE"),
            to=os.getenv("MY_PHONE")
        )

        print("✅ SMS Sent Successfully!")
        print("Message SID:", message.sid)

    except Exception as e:
        print("❌ SMS Error:", e)
