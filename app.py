import cv2
import time
import os
from detector import detect_accident
from email_alert import send_email_alert
from location import get_location

if not os.path.exists("snapshots"):
    os.makedirs("snapshots")

def main():
    print("🚀 Road Accident Alert System Started")

    cap = cv2.VideoCapture(0)  # webcam
    last_alert_time = 0
    cooldown = 30  # seconds

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        accident, vehicle_count = detect_accident(frame)

        cv2.putText(frame, f"Vehicles: {vehicle_count}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if accident:
            cv2.putText(frame, "🚨 ACCIDENT DETECTED!", (20, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            now = time.time()
            if now - last_alert_time > cooldown:
                last_alert_time = now

                snapshot_path = f"snapshots/accident_{int(now)}.jpg"
                cv2.imwrite(snapshot_path, frame)

                lat, lon, maps_link = get_location()

                subject = "🚨 Road Accident Detected"
                body = f"""
Accident detected by AI system.

📍 Location:
Latitude: {lat}
Longitude: {lon}

🗺️ Google Maps:
{maps_link}

⏰ Time:
{time.ctime(now)}

Please take immediate action.
"""

                send_email_alert(subject, body, snapshot_path)

        cv2.imshow("Road Accident Alert System", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
