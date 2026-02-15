from email_alert import send_email_alert
from sms_alert import send_sms

send_sms("🚨 Test SMS from Accident System")

send_email_alert(
    "🚨 TEST EMAIL WITH SNAPSHOT",
    "If you see an attachment, snapshot email works perfectly.",
    "snapshots/test.jpg"
)
