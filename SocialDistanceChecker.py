import cv2
import numpy as np
from ultralytics import YOLO
import os

#Initilialize model YOLO (kami menggunakan model yolov8n)
model = YOLO('yolov8s.pt')

def euclidean_distance(point1,point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def checkSocialDistance(detections,frame, minDistance = 100):
     # Ambil pusat bounding box untuk manusia
    humans = [det for det in detections.boxes if int(det.cls) == 0]
    centers = []
    for human in humans:
        x1, y1, x2, y2 = human.xyxy[0].tolist()  # Bounding box koordinat
        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)
        centers.append((center_x, center_y))
    
    # Cek pelanggaran jarak
    violations = set()
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            if euclidean_distance(centers[i], centers[j]) < minDistance:
                violations.add(i)
                violations.add(j)

    # Tandai bounding box
    annotated_frame = frame.copy()
    for idx, human in enumerate(humans):
        x1, y1, x2, y2 = map(int, human.xyxy[0].tolist())
        color = (0, 0, 255) if idx in violations else (0, 255, 0)  # Merah untuk pelanggaran
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
        cv2.circle(annotated_frame, centers[idx], 5, color, -1)

    return len(violations), annotated_frame



# Function untuk menghitung jumlah manusia dalam suatu frame.
def countHumanInFrame(frame, minDistance = 100):
    result = model(frame)
    detections = result[0]

     # Hitung jumlah manusia dan pelanggaran jarak sosial
    num_humans = len([det for det in detections.boxes if int(det.cls) == 0])
    num_violations, annotated_frame = checkSocialDistance(detections, frame, minDistance)

    return num_humans, num_violations, annotated_frame


# Function untuk mendeteksi dari video yang di input.
def detectFromVideo(video_path,output_path = None):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    if output_path:
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        num_humans, num_violations, annotated_frame = countHumanInFrame(frame)
        cv2.putText(annotated_frame, f"Humans: {num_humans}", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"Violations: {num_violations}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        print(f"Humans: {num_humans}")

        # Tampilkan frame secara langsung
        cv2.imshow('Human Detection', annotated_frame)

        if output_path:
            out.write(annotated_frame)
        
         # Tekan 'q' untuk keluar dari video yang ditampilkan.
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    if output_path:
        out.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)


# Realtime Detection(Dari webcam)
def detectFromWebcam():
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        num_humans, num_violations, annotated_frame = countHumanInFrame(frame)
        cv2.putText(annotated_frame, f"Humans: {num_humans}", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"Violations: {num_violations}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        print(f"Humans: {num_humans}")

        # Tampilkan frame secara langsung
        cv2.imshow('Human Detection', annotated_frame)

        # Tekan 'q' untuk keluar dari webcam
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)


if __name__ == "__main__":
    input_video_path = "input/Shopping Crowd Video.mp4"
    output_video_path = "output/testingVideo_output.mp4"

    if not os.path.exists("output"):
        os.makedirs("output")

    # Kalau mau detect dari file video, uncomment 2 baris code dibawah ini.
    detectFromVideo(input_video_path, output_video_path)
    print(f"Video hasil tersimpan di {output_video_path}")

    # Kalau mau detect dari webcam, uncomment function dibawah ini.
    # detectFromWebcam()