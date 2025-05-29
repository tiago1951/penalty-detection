import cv2
import os
import pandas as pd
from glob import glob

VIDEO_DIR = "videos"
EXT = ".mp4"
OUT_CSV = "labels.csv"

labels = []
video_files = sorted(glob(os.path.join(VIDEO_DIR, "**", f"*{EXT}"), recursive=True))
print(f"🔎 {len(video_files)} vídeos encontrados.")

for path in video_files:
    relative_path = os.path.relpath(path, VIDEO_DIR)
    result = None
    direction = None
    angle = None

    print(f"\n▶️ {relative_path}")
    print("g = Golo, f = Falhado | 1 = Esquerda, 2 = Meio, 3 = Direita | s = Ângulo Traseiro SIM, n = NÃO | Enter = Guardar")

    while True:
        cap = cv2.VideoCapture(path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (720, 480))
            cv2.putText(frame, f"{relative_path}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
            if result:
                cv2.putText(frame, f"Resultado: {result}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            if direction:
                cv2.putText(frame, f"Direcao: {direction}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            if angle:
                cv2.putText(frame, f"Angulo traseiro: {angle}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

            cv2.imshow("Rotulador", frame)
            key = cv2.waitKey(30) & 0xFF

            if key == ord("g"):
                result = "golo"
            elif key == ord("f"):
                result = "falhado"
            elif key == ord("1"):
                direction = "esquerda"
            elif key == ord("2"):
                direction = "meio"
            elif key == ord("3"):
                direction = "direita"
            elif key == ord("s"):
                angle = "sim"
            elif key == ord("n"):
                angle = "nao"
            elif key == 13:  # ENTER
                if not result:
                    print("⚠️ Falta selecionar o resultado (g = golo, f = falhado).")
                elif not direction:
                    print("⚠️ Falta selecionar a direção (1 = esquerda, 2 = meio, 3 = direita).")
                elif not angle:
                    print("⚠️ Falta indicar se há ângulo traseiro (s = sim, n = não).")
                else:
                    labels.append({
                        "video": relative_path,
                        "resultado": result,
                        "direcao": direction,
                        "angulo_traseiro": angle
                    })
                    print(f"✅ Guardado: {result}, {direction}, {angle}")
                    cap.release()
                    cv2.destroyAllWindows()
                    break
            elif key == ord("q"):
                print("🛑 Interrompido.")
                cap.release()
                cv2.destroyAllWindows()
                exit()

        if result and direction and angle:
            break

# Guarda CSV
df = pd.DataFrame(labels)
df.to_csv(OUT_CSV, index=False)
print(f"\n💾 Labels guardados em {OUT_CSV}")


