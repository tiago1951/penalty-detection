import cv2
import os
import random
from glob import glob
from shutil import copyfile

FRAMES_DIR = "all_frames"
SHUFFLED_DIR = "shuffled_frames"

VIDEOS_DIR = "videos"  # <--- important fix here
video_files = [
    f for f in glob(os.path.join(VIDEOS_DIR, "**", "*.*"), recursive=True)
    if f.lower().endswith(".mp4")
]
os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(SHUFFLED_DIR, exist_ok=True)

print(f"Found {len(video_files)} .mp4 files:")
for f in video_files:
    print("🎥", f)
# Step 2: Extract frames from all videos
for video_path in video_files:
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_filename = f"{video_name}_frame_{frame_count:04d}.jpg"
        cv2.imwrite(os.path.join(FRAMES_DIR, frame_filename), frame)
        frame_count += 1

    cap.release()
    print(f"Extracted {frame_count} frames from {video_name}")

# Step 3: Shuffle all frames
all_frames = os.listdir(FRAMES_DIR)
random.shuffle(all_frames)

print(f"Shuffling {len(all_frames)} frames...")

for i, frame_name in enumerate(all_frames):
    src = os.path.join(FRAMES_DIR, frame_name)
    dst = os.path.join(SHUFFLED_DIR, f"shuffled_{i:05d}.jpg")
    copyfile(src, dst)

print("✅ Done. All shuffled frames saved to 'shuffled_frames/'")