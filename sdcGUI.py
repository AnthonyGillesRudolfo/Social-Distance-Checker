import tkinter as tk
from tkinter import filedialog, messagebox
from SocialDistanceChecker import detectFromVideo, detectFromWebcam  # Impor dari file lain
import threading
import os

Running = False

def detect_from_video_gui():
    try:
        input_video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.*")])
        if not input_video_path:
            messagebox.showwarning("Peringatan", "Tidak ada file video yang dipilih.")
            return
        output_video_path = "output/processed_video.mp4"
        if not os.path.exists("output"):
            os.makedirs("output")

        messagebox.showinfo("Info", "Memulai deteksi dengan webcam. Tekan 'q' untuk berhenti.")
        detectFromVideo(input_video_path, output_video_path)
        messagebox.showinfo("Sukses", f"Video hasil tersimpan di {output_video_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan saat memilih file: {e}")

def detect_from_webcam_gui():
    global Running

    messagebox.showinfo("Info", "Memulai deteksi dengan webcam. Tekan 'q' untuk keluar dari webcam.")
    Running = True 
    detectFromWebcam()
    Running = False


def CloseGUI():
    global Running
    Running = False
    root.destroy()

def create_gui():
    global root
    root = tk.Tk()
    root.title("Social Distance Checker")
    root.geometry("400x200")

    title_label = tk.Label(root, text="Social Distance Checker", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    video_button = tk.Button(root, text="Deteksi from Video", command=detect_from_video_gui, width=20, bg="blue", fg="black")
    video_button.pack(pady=10)

    webcam_button = tk.Button(root, text="Deteksi from Webcam", command=detect_from_webcam_gui, width=20, bg="green", fg="black")
    webcam_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=CloseGUI, width=20, bg="red", fg="black")
    exit_button.pack(pady=10)

    root.mainloop()



if __name__ == "__main__":
    create_gui()

