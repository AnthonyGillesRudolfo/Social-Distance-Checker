# Project YOLO Human Detection
Proyek ini menggunakan YOLOv8n untuk mendeteksi dan menghitung jumlah manusia dalam video.

## Cara menjalankan

### 1. Persiapan Lingkungan
Pastikan Python sudah terinstal di komputer Anda. Buat virtual environment dan instal dependensi:
```bash
python -m venv yolo_env
source yolo_env/bin/activate  # Untuk macOS/Linux
yolo_env\Scripts\activate     # Untuk Windows
pip install -r requirements.txt
```

### 2.1. Deteksi Manusia dari file video
1. Jika mau mendeteksi manusia dari video, masukan video anda ke dalam folder input
2. Pastikan function detectFromVideo() di uncomment dan detectFromWebcam di comment.
3. Masukan path video anda di input_video_path
4. atur nama untuk output video di output_video_path
5. Jalankan program:
```bash
python3 main.py
```

### 2.2. Deteksi Manusia dari webcam
1. Pastikan detectFromWebcam di uncomment dan detectFromVideo() di comment
2. Jalankan program:
```bash
python3 main.py
```




