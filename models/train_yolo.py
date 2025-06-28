from ultralytics import YOLO
import os

# Load and train YOLOv8 model
model = YOLO("yolov8n.pt")  # Start with pre-trained nano model
data_yaml = "data/hrsc2016/data.yaml"  # Path to dataset config

# Train model
model.train(
    data=data_yaml,
    epochs=50,
    imgsz=640,
    batch=16,
    name="ship_detection",
    augment=True
)

# Save trained model
model.save("models/ship_yolov8.pt")
