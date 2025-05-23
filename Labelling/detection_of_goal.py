import os, cv2, numpy as np, shutil
from ultralytics import YOLO

# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------
def post_bottom_center(box):
    """Return the centre of the bottom edge of a YOLO box [x1,y1,x2,y2]."""
    x1, y1, x2, y2 = map(int, box)
    return np.array(((x1 + x2) / 2, y2), dtype=np.float32)

def post_top_center(box):
    """Return the centre of the top edge of the post box."""
    x1, y1, x2, _ = map(int, box)
    return np.array(((x1 + x2) / 2, y1), dtype=np.int32)

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
VIDEO_DIR  = r"C:\Users\tiago1951\Desktop\Universidade\PBMA\Projeto\Data\videos_after"
OUTPUT_DIR = r"C:\Users\tiago1951\Desktop\Universidade\PBMA\Projeto\Labelling\videos_after_goal_lines"

# ------------------------------------------------------------------
# Load YOLO model
# ------------------------------------------------------------------
model = YOLO("runs/detect/train5/weights/last.pt")
model.model.names = ['Post', 'Ball']

# ------------------------------------------------------------------
# Prepare output directory
# ------------------------------------------------------------------
if os.path.exists(OUTPUT_DIR):
    try:
        shutil.rmtree(OUTPUT_DIR)
    except PermissionError:
        print("⚠️  Some files in", OUTPUT_DIR, "were locked; continuing.")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------------------------------------------
# Process every video
# ------------------------------------------------------------------
for root, _, files in os.walk(VIDEO_DIR):
    for fname in files:
        if not fname.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
            continue

        in_path  = os.path.join(root, fname)
        rel      = os.path.splitext(os.path.relpath(in_path, VIDEO_DIR))[0]
        out_path = os.path.join(OUTPUT_DIR, f"{rel}_labelled.mp4")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        print("▶️ ", in_path)

        # ----------------------------------------------------------
        # PASS 1 – decide GOAL / NOT GOAL
        # ----------------------------------------------------------
        cap = cv2.VideoCapture(in_path)
        H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        seen_outside = False

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            res   = model(frame, verbose=False, conf=0.2, iou=0.45)[0]
            boxes = res.boxes.xyxy.cpu().numpy()
            cls   = res.boxes.cls.cpu().numpy().astype(int)

            post_boxes = boxes[cls == 0]
            if len(post_boxes) < 2:
                continue
            post_boxes = post_boxes[post_boxes[:, 0].argsort()][:2]
            left_box, right_box = post_boxes

            # --- key geometry (same for both passes) ----------------
            A = post_bottom_center(left_box)
            B = post_bottom_center(right_box)
            Cleft  = post_top_center(left_box)
            Cright = post_top_center(right_box)

            AB = B - A
            N  = np.array([-AB[1], AB[0]], np.float32)
            N /= np.linalg.norm(N)
            if N[1] < 0:
                N = -N

            # intersections of the perpendiculars with bottom
            tA = (H - 1 - A[1]) / N[1]
            tB = (H - 1 - B[1]) / N[1]
            A_far = A + N * tA
            B_far = B + N * tB

            # polygon of valid zone
            zone = np.array([Cleft, Cright,
                             B_far.astype(int), A_far.astype(int)])

            # check the most confident ball
            ball_idx = np.where(cls == 1)[0]
            if len(ball_idx):
                confs = res.boxes.conf.cpu().numpy()
                best  = ball_idx[confs[ball_idx].argmax()]
                bx1, by1, bx2, by2 = map(int, boxes[best])
                P = ((bx1 + bx2) // 2, (by1 + by2) // 2)
                if cv2.pointPolygonTest(zone, P, False) < 0:
                    seen_outside = True
                    break
        cap.release()

        if seen_outside:
            verdict, color, reason = "NOT GOAL", (0, 0, 255), "– bola saiu da zona verde"
        else:
            verdict, color, reason = "GOAL!",   (0, 255, 0),  ""

        print("→", verdict, reason)

        # ----------------------------------------------------------
        # PASS 2 – annotate and save
        # ----------------------------------------------------------
        cap     = cv2.VideoCapture(in_path)
        fps     = cap.get(cv2.CAP_PROP_FPS)
        W, H    = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer  = cv2.VideoWriter(out_path,
                                  cv2.VideoWriter_fourcc(*"mp4v"),
                                  fps, (W, H))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            res   = model(frame, verbose=False)[0]
            img   = res.plot()
            boxes = res.boxes.xyxy.cpu().numpy()
            cls   = res.boxes.cls.cpu().numpy().astype(int)

            posts = boxes[cls == 0]
            if len(posts) >= 2:
                posts = posts[posts[:, 0].argsort()][:2]
                left_box, right_box = posts

                # same geometry again
                A = post_bottom_center(left_box)
                B = post_bottom_center(right_box)
                Cleft  = post_top_center(left_box)
                Cright = post_top_center(right_box)

                # yellow goal-line
                cv2.line(img, tuple(A.astype(int)), tuple(B.astype(int)),
                         (0, 255, 255), 2)

                # unit normal N
                AB = B - A
                N  = np.array([-AB[1], AB[0]], np.float32)
                N /= np.linalg.norm(N)
                if N[1] < 0:
                    N = -N

                # red perpendiculars
                for P in (A, B):
                    start = tuple(P.astype(int))
                    end   = (int(P[0] + N[0] * H),
                             int(P[1] + N[1] * H))
                    cv2.line(img, start, end, (0, 0, 255), 2)

                # green zone
                tA = (H - 1 - A[1]) / N[1]
                tB = (H - 1 - B[1]) / N[1]
                A_far = A + N * tA
                B_far = B + N * tB
                zone_poly = np.array([Cleft, Cright,
                                      B_far.astype(int), A_far.astype(int)])
                overlay = img.copy()
                cv2.fillPoly(overlay, [zone_poly], (0, 255, 0))
                cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)

            # verdict text
            txt = verdict + (" " + reason if reason else "")
            cv2.putText(img, txt, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2, cv2.LINE_AA)

            writer.write(img)

        cap.release(); writer.release()
        print("✅  Saved:", out_path)

print("🏁  All videos processed. Output in:", OUTPUT_DIR)
