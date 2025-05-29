import os
import cv2
import numpy as np
from ultralytics import YOLO

# Load model
model = YOLO("runs/detect/train5/weights/last.pt")
model.model.names = ['Post', 'Ball']

VIDEO_DIR = r"C:\Users\tiago1951\Desktop\Universidade\PBMA\Projeto\Data\videos_after"
OUTPUT_DIR = r"C:\Users\tiago1951\Desktop\Universidade\PBMA\Projeto\Labelling\videos_with_goal_line"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_post_bottom_center(box):
    x1, y1, x2, y2 = map(int, box)
    return ((x1 + x2) // 2, y2)

for root, _, files in os.walk(VIDEO_DIR):
    for file in files:
        if not file.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
            continue

        input_path = os.path.join(root, file)
        rel_path = os.path.relpath(input_path, VIDEO_DIR)
        base_name = os.path.splitext(rel_path)[0]
        output_path = os.path.join(OUTPUT_DIR, f"{base_name}.mp4")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        cap = cv2.VideoCapture(input_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame, verbose=False)[0]
            post_boxes = [box.xyxy[0].cpu().numpy() for box in results.boxes if int(box.cls[0]) == 0]

            if len(post_boxes) >= 2:
                # Sort by x position to get left and right posts
                post_boxes.sort(key=lambda b: b[0])
                p1 = get_post_bottom_center(post_boxes[0])
                p2 = get_post_bottom_center(post_boxes[-1])
                frame = cv2.line(frame, p1, p2, (0, 255, 0), 2)

            out.write(frame)

        cap.release()
        out.release()
        print(f"✅ Goal line added: {output_path}")

print("✅ All videos processed.")
