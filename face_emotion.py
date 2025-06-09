import cv2
from deepface import DeepFace
import tkinter as tk
from tkinter import filedialog, messagebox
import win32gui
import time


def emotion_to_farsi(emotion_en):
    dictionary = {
        "angry": "عصبانی",
        "disgust": "انزجار",
        "fear": "ترس",
        "happy": "خوشحال",
        "sad": "غمگین",
        "surprise": "متعجب",
        "neutral": "خنثی"
    }
    return dictionary.get(emotion_en, emotion_en)

def bring_window_to_front(win_title):
    hwnd = win32gui.FindWindow(None, win_title)
    if hwnd:
        win32gui.ShowWindow(hwnd, 5)
        win32gui.SetForegroundWindow(hwnd)

def detect_emotion_from_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("خطا", "دوربین در دسترس نیست.")
        return

    messagebox.showinfo("راهنما", "برای خروج از وبکم کلید Q را بزنید.")
    window_title = "Webcam - Press Q to exit"

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            result = DeepFace.analyze(img_path=frame, actions=["emotion"], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
            cv2.putText(frame, f"Emotion: {emotion}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        except Exception as e:
            print(f"Error in emotion detection: {e}")
            cv2.putText(frame, "Face not detected", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        cv2.imshow(window_title, frame)
        bring_window_to_front(window_title)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.01)

    cap.release()
    cv2.destroyAllWindows()

def detect_emotion_from_image():
    filepath = filedialog.askopenfilename(title="انتخاب تصویر", 
                                          filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    if not filepath:
        return

    try:
        img = cv2.imread(filepath)
        if img is None:
            messagebox.showerror("خطا", "تصویر یافت نشد یا فرمت پشتیبانی نمی‌شود.")
            return

        result = DeepFace.analyze(img_path=img, actions=["emotion"], enforce_detection=False)
        emotion_en = result[0]['dominant_emotion']
        emotion_fa = emotion_to_farsi(emotion_en)
        messagebox.showinfo("نتیجه", f"حالت چهره: {emotion_fa}")

    except Exception as e:
        messagebox.showerror("خطا در تحلیل عکس", str(e))

def main():
    root = tk.Tk()
    root.title("تشخیص حالت چهره")
    root.geometry("300x150")

    label = tk.Label(root, text="لطفا یک حالت را انتخاب کنید:", font=("Arial", 12))
    label.pack(pady=10)

    btn_webcam = tk.Button(root, text="وبکم", font=("Arial", 12), width=15, command=lambda: [root.destroy(), detect_emotion_from_webcam()])
    btn_webcam.pack(pady=5)

    btn_image = tk.Button(root, text="انتخاب عکس", font=("Arial", 12), width=15, command=lambda: [root.destroy(), detect_emotion_from_image()])
    btn_image.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
