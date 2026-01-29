from ultralytics import YOLO

# Load YOLO model (default COCO model)
model = YOLO("yolov8n.pt")

# COCO class IDs for vehicles
VEHICLE_CLASSES = [2, 3, 5, 7]  
# 2=car, 3=motorbike, 5=bus, 7=truck

def detect_accident(frame):
    """
    Demo Logic:
    If too many vehicles overlap / sudden detection spike -> treat as accident.
    (Real accident model requires accident dataset training)
    """

    results = model(frame, verbose=False)
    boxes = results[0].boxes

    vehicle_count = 0

    for box in boxes:
        cls = int(box.cls[0])
        if cls in VEHICLE_CLASSES:
            vehicle_count += 1

    # Simple threshold logic (demo)
    if vehicle_count >= 3:
        return True, vehicle_count

    return False, vehicle_count
