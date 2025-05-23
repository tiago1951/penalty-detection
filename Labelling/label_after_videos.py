import os
import cv2
from ultralytics import YOLO

# Load your trained model
model = YOLO("runs/detect/train5/weights/last.pt")
model.model.names = ['Post', 'Ball']


# Input/output folders (WSL paths)
VIDEO_DIR = "C:\\Users\\tiago1951\\Desktop\\Universidade\\PBMA\\Projeto\\Data\\videos_after"

OUTPUT_DIR = "C:\\Users\\tiago1951\\Desktop\\Universidade\\PBMA\\Projeto\\Labelling\\videos_after_goal_lines"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Walk through all subfolders
for root, _, files in os.walk(VIDEO_DIR):
    for file in files:
        if not file.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
            continue

        input_path = os.path.join(root, file)
        rel_path = os.path.relpath(input_path, VIDEO_DIR)
        base_name = os.path.splitext(rel_path)[0]

        # Paths for original and mirrored outputs
        output_path_original = os.path.join(OUTPUT_DIR, f"{base_name}.mp4")
        output_path_mirrored = os.path.join(OUTPUT_DIR, f"{base_name}_mirrored.mp4")

        # Ensure output directories exist
        os.makedirs(os.path.dirname(output_path_original), exist_ok=True)
        os.makedirs(os.path.dirname(output_path_mirrored), exist_ok=True)

        # Capture video
        cap = cv2.VideoCapture(input_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Define output writers
        out_original = cv2.VideoWriter(output_path_original, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
        out_mirrored = cv2.VideoWriter(output_path_mirrored, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # --- Original version ---
            results_original = model(frame, verbose=False)[0]
            annotated_original = results_original.plot()
            out_original.write(annotated_original)

            # --- Mirrored version ---
            mirrored_frame = cv2.flip(frame, 1)
            results_mirrored = model(mirrored_frame, verbose=False)[0]
            annotated_mirrored = results_mirrored.plot()
            out_mirrored.write(annotated_mirrored)

        cap.release()
        out_original.release()
        out_mirrored.release()

        print(f"✅ Saved annotated: {output_path_original}")
        print(f"✅ Saved mirrored : {output_path_mirrored}")

print("✅ All videos processed.")
