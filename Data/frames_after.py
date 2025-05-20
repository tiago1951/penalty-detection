import cv2
import os
import random
from glob import glob

OUTPUT_DIR = "after_shuffled_frames"
VIDEOS_DIR = "videos_after"

# Gather all .mp4 files from videos_after
video_files = [
    f for f in glob(os.path.join(VIDEOS_DIR, "**", "*.mp4"), recursive=True)
]

# Make output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Found {len(video_files)} .mp4 files:")
for f in video_files:
    print("🎥", f)

# Step 1: Extract frames from all videos and store temporarily in a list
temp_frame_paths = []

for video_path in video_files:
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        temp_frame_paths.append((video_name, frame_count, frame))
        frame_count += 1

    cap.release()
    print(f"Extracted {frame_count} frames from {video_name}")

# Step 2: Shuffle all frames
print(f"Shuffling {len(temp_frame_paths)} frames...")
random.shuffle(temp_frame_paths)

# Step 3: Save shuffled frames
for i, (video_name, frame_index, frame) in enumerate(temp_frame_paths):
    filename = f"shuffled_{i:05d}.jpg"
    cv2.imwrite(os.path.join(OUTPUT_DIR, filename), frame)

print(f"✅ Done. All shuffled frames saved to '{OUTPUT_DIR}/'")
