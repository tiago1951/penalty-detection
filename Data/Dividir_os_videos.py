import os
import cv2
import numpy as np
import glob
from ultralytics import YOLO

# Load trained model
model = YOLO("runs/detect/train/weights/last.pt")

# Settings
VIDEO_DIR = "videos"
BEFORE_DIR = "videos_before"
AFTER_DIR = "videos_after"
BALL_CLASS_ID = 0
MOVEMENT_THRESHOLD = 20
MIN_FRAMES_BEFORE_MOVEMENT = 20
OVERLAP_FRAMES = 5

os.makedirs(BEFORE_DIR, exist_ok=True)
os.makedirs(AFTER_DIR, exist_ok=True)

# Clean up old outputs
for folder in [BEFORE_DIR, AFTER_DIR]:
    for file in glob.glob(os.path.join(folder, "**", "*.mp4"), recursive=True):
        os.remove(file)
print("🧹 Cleared old videos from videos_before/ and videos_after/")

def detect_ball_center(results):
    for box in results.boxes:
        if int(box.cls[0]) == BALL_CLASS_ID:
            x1, y1, x2, y2 = box.xyxy[0]
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            return (float(cx), float(cy))
    return None

def process_video(input_path, rel_name, mirrored=False):
    label = "_mirrored" if mirrored else ""
    output_before = os.path.join(BEFORE_DIR, f"{rel_name}{label}_before.mp4")
    output_after = os.path.join(AFTER_DIR, f"{rel_name}{label}_after.mp4")
    os.makedirs(os.path.dirname(output_before), exist_ok=True)
    os.makedirs(os.path.dirname(output_after), exist_ok=True)

    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frames = []
    positions = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if mirrored:
            frame = cv2.flip(frame, 1)

        frames.append(frame)
        results = model(frame, verbose=False)[0]
        center = detect_ball_center(results)
        positions.append(center)

    cap.release()

    split_index = len(frames)
    last_seen = None
    missed_frames = 0
    movement_triggered = False

    for i in range(MIN_FRAMES_BEFORE_MOVEMENT, len(positions) - 1):
        curr = positions[i]
        nxt = positions[i + 1]

        if curr and nxt:
            dx = nxt[0] - curr[0]
            dy = nxt[1] - curr[1]
            dist = np.sqrt(dx**2 + dy**2)
            if dist > MOVEMENT_THRESHOLD:
                split_index = i
                movement_triggered = True
                print(f"✅ Movement detected at frame {i} (distance={dist:.2f}) {label}")
                break

        if curr:
            last_seen = i
            missed_frames = 0
        else:
            missed_frames += 1
            if not movement_triggered and missed_frames >= 7 and last_seen is not None:
                split_index = max(min(last_seen, len(frames) - 1), 0)
                print(f"⚠️ Ball disappeared. Using fallback at frame {split_index} {label}")
                break

    end_before = min(split_index, len(frames))
    start_after = max(split_index - OVERLAP_FRAMES, 0)

    # Save BEFORE
    out_before = cv2.VideoWriter(output_before, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    for i in range(0, end_before):
        out_before.write(frames[i])
    out_before.release()

    # Save AFTER
    if start_after < len(frames):
        out_after = cv2.VideoWriter(output_after, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
        for i in range(start_after, len(frames)):
            out_after.write(frames[i])
        out_after.release()

    print(f"✅ Saved BEFORE  ➤ {output_before}")
    print(f"✅ Saved AFTER   ➤ {output_after}")

# Walk through original videos
for root, _, files in os.walk(VIDEO_DIR):
    for file in files:
        if not file.endswith(".mp4"):
            continue

        input_path = os.path.join(root, file)
        rel_name = os.path.splitext(os.path.relpath(input_path, VIDEO_DIR))[0]

        # Process original and mirrored version
        process_video(input_path, rel_name, mirrored=False)
        #process_video(input_path, rel_name, mirrored=True)

