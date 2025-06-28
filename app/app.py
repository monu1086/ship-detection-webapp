from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO
import sqlite3
import os

app = Flask(__name__)
model = YOLO("yolov8n.pt")  # Load pre-trained YOLOv8 model

def init_db():
    conn = sqlite3.connect('detections.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS detections
                 (id INTEGER PRIMARY KEY, timestamp TEXT, ship_count INTEGER, ship_types TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # Run YOLOv8 inference
    results = model(img)
    detections = results[0].boxes.data.cpu().numpy()  # [x1, y1, x2, y2, conf, cls]
    
    # Process detections
    ship_count = len(detections)
    ship_types = [model.names[int(cls)] for cls in detections[:, 5]]
    
    # Save to database
    conn = sqlite3.connect('detections.db')
    c = conn.cursor()
    c.execute("INSERT INTO detections (stamp, ship_count, ship_types) VALUES (datetime('now'), ?, ?)",
              (ship_count, ','.join(ship_types)))
    conn.commit()
    conn.close()
    
    return jsonify({'ship_count': ship_count, 'ship_types': ship_types})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
