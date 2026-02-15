import cv2
import time
import os

from detector import detect_accident
from email_alert import send_email_alert
from sms_alert import send_sms
from location import get_location

# 🔥 Create snapshots folder
os.makedirs("snapshots", exist_ok=True)

def main():
    print("🚀 Road Accident Alert System Started")

    # 🔥 Windows camera fix
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("❌ Camera not detected. Try changing index (0 → 1)")
        return

    last_alert_time = 0
    cooldown = 30  # seconds

    while True:
        ret, frame = cap.read()

        if not ret:
            print("❌ Failed to grab frame")
            break

        accident, vehicle_count = detect_accident(frame)

        # Show vehicle count
        cv2.putText(
            frame,
            f"Vehicles: {vehicle_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        if accident:
            cv2.putText(
                frame,
                "🚨 ACCIDENT DETECTED!",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3,
            )

            now = time.time()

            if now - last_alert_time > cooldown:
                last_alert_time = now

                filename = f"accident_{int(now)}.jpg"
                path = os.path.join("snapshots", filename)
                cv2.imwrite(path, frame)

                # 🔥 Get location
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

                # 🔥 Send Email
                send_email_alert(subject, body, path)

                # 🔥 Send SMS
                send_sms(
                    f"🚨 Accident Detected!\nLocation: {maps_link}\nTime: {time.ctime(now)}"
                )

        # Show camera window
        cv2.imshow("Road Accident Alert System", frame)

        # Press Q to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("🛑 System Stopped")


if __name__ == "__main__":
    main()
