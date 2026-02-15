from flask import Flask, jsonify
from flask_cors import CORS
import cv2
import time
import os

from detector import detect_accident
from email_alert import send_email_alert
from sms_alert import send_sms
from location import get_location

app = Flask(__name__)
CORS(app)

# 🔥 Open camera in backend
camera = cv2.VideoCapture(0)

last_alert_time = 0
cooldown = 30

os.makedirs("snapshots", exist_ok=True)

@app.route("/status")
def status():
    global last_alert_time

    ret, frame = camera.read()
    if not ret:
        return jsonify({"error": "Camera not working"})

    accident, vehicle_count = detect_accident(frame)

    response = {
        "accident": accident,
        "vehicle_count": vehicle_count,
        "timestamp": time.ctime(),
        "snapshot": None,
        "maps_link": None
    }

    if accident:
        now = time.time()

        if now - last_alert_time > cooldown:
            last_alert_time = now

            filename = f"accident_{int(now)}.jpg"
            path = os.path.join("snapshots", filename)
            cv2.imwrite(path, frame)

            lat, lon, maps_link = get_location()

            subject = "🚨 Road Accident Detected!"

            body = f"""
Accident detected by AI Surveillance System.

📍 Location Details:
Latitude: {lat}
Longitude: {lon}

🗺️ Google Maps:
{maps_link}

⏰ Time:
{time.ctime(now)}

⚠️ Immediate emergency response required.
"""

            send_email_alert(subject, body, path)

            send_sms(
                f"🚨 Accident Detected!\nLocation: {maps_link}\nTime: {time.ctime(now)}"
            )

            response["snapshot"] = f"snapshots/{filename}"
            response["maps_link"] = maps_link

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
