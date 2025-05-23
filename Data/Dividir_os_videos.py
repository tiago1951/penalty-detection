import os
import cv2
import numpy as np
import glob
from ultralytics import YOLO

# Carrega o modelo
model = YOLO("runs/detect/train/weights/best.pt")

# Configurações
VIDEO_DIR                = "videos"
BEFORE_DIR               = "videos_before"
AFTER_DIR                = "videos_after"
BALL_CLASS_ID            = 0
MOVEMENT_THRESHOLD       = 30    # pixels
MIN_FRAMES_BEFORE_MOV    = 25    # ignora até este frame
OVERLAP_FRAMES           = 5
FALLBACK_MISSED_FRAMES   = 11

# Prepara pastas de saída
os.makedirs(BEFORE_DIR, exist_ok=True)
os.makedirs(AFTER_DIR, exist_ok=True)
for folder in [BEFORE_DIR, AFTER_DIR]:
    for f in glob.glob(os.path.join(folder, "**", "*.mp4"), recursive=True):
        os.remove(f)
print("🧹 Old outputs cleared")

def detect_ball_center(results):
    for box in results.boxes:
        if int(box.cls[0]) == BALL_CLASS_ID:
            x1, y1, x2, y2 = box.xyxy[0]
            return ((x1 + x2)/2, (y1 + y2)/2)
    return None

def process_video(path, name, mirrored=False):
    label      = "_mirrored" if mirrored else ""
    out_before = os.path.join(BEFORE_DIR, f"{name}{label}_before.mp4")
    out_after  = os.path.join(AFTER_DIR,  f"{name}{label}_after.mp4")
    os.makedirs(os.path.dirname(out_before), exist_ok=True)
    os.makedirs(os.path.dirname(out_after),  exist_ok=True)

    cap    = cv2.VideoCapture(path)
    fps    = cap.get(cv2.CAP_PROP_FPS)
    w      = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h      = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frames    = []
    positions = []

    # 1) captura frames e detecções
    while True:
        ret, frame = cap.read()
        if not ret: break
        if mirrored:
            frame = cv2.flip(frame, 1)
        frames.append(frame)
        res = model(frame, verbose=False)[0]
        positions.append(detect_ball_center(res))
    cap.release()

    # 2) constrói lista de índices onde bola foi detectada
    detected_idxs = [i for i, p in enumerate(positions) if p is not None]

    split_index     = len(frames)
    movement_found  = False
    last_seen_idx   = None
    missed_frames   = 0

    # 3) percorre pares de detecções consecutivas
    for j in range(len(detected_idxs)-1):
        i_curr = detected_idxs[j]
        i_next = detected_idxs[j+1]

        # só começa após MIN_FRAMES_BEFORE_MOV
        if i_curr < MIN_FRAMES_BEFORE_MOV:
            last_seen_idx = i_curr
            continue

        # calcula distância entre detecções consecutivas
        x1,y1 = positions[i_curr]
        x2,y2 = positions[i_next]
        dist = np.hypot(x2-x1, y2-y1)

        if dist > MOVEMENT_THRESHOLD:
            split_index    = i_curr
            movement_found = True
            print(f"✅ Movimento detectado entre frames {i_curr}→{i_next}, dist={dist:.2f} {label}")
            break

        last_seen_idx = i_curr

    # 4) fallback caso a bola suma sem movimento
    if not movement_found:
        # conta quantos frames após a última detecção
        missed_frames = len(frames) - 1 - last_seen_idx
        if missed_frames >= FALLBACK_MISSED_FRAMES:
            split_index = last_seen_idx
            print(f"⚠️ Fallback usado no frame {split_index} {label}")

    # 5) escreve vídeos com sobreposição
    end_before  = min(split_index , len(frames))
    start_after = max(split_index - OVERLAP_FRAMES, 0)

    # BEFORE
    w_b = cv2.VideoWriter(out_before, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w,h))
    for f in frames[:end_before]:
        w_b.write(f)
    w_b.release()

    # AFTER
    w_a = cv2.VideoWriter(out_after, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w,h))
    for f in frames[start_after:]:
        w_a.write(f)
    w_a.release()

    print(f"✅ Saved BEFORE ➤ {out_before}")
    print(f"✅ Saved AFTER  ➤ {out_after}")

# 6) executa em todos os vídeos
for root, _, files in os.walk(VIDEO_DIR):
    for fn in files:
        if not fn.lower().endswith(".mp4"): continue
        p = os.path.join(root, fn)
        n = os.path.splitext(os.path.relpath(p, VIDEO_DIR))[0]
        process_video(p, n, mirrored=False)
        # process_video(p, n, mirrored=True)

