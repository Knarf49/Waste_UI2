import cv2
import torch
import numpy as np
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.image import Image
from threading import Thread
from ultralytics import YOLO
import time

Builder.load_string('''
<ScanScreen>:
    name: "scan"
    canvas.before:
        Color:
            rgba: (221/255, 237/255, 233/255, 1)  # Set background color to white
        Rectangle:
            size: self.size
            pos: self.pos

    FloatLayout:
        CameraImage:
            id: camera_view
            size_hint: .7, .7
            pos_hint: {"center_x": 0.5, "center_y": 0.5}

        MDRaisedButton:
            text: 'Open Camera (OpenCV)'
            size_hint: None, None
            size: 200, 50
            pos_hint: {'center_x': 0.5, 'y': 0.1}
            on_release: root.start_camera_thread()
''')

class CameraImage(Image):
    pass

class ScanScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ตัวแปรสำหรับจัดการกล้อง
        self.camera_running = False  # สถานะของกล้อง
        self.capture = None  # ตัวจับภาพจากกล้อง
        self.model = YOLO(r"C:\Users\Frank\Documents\GitHub\Waste_UI2\best.pt")  # โหลด YOLO โมเดล (แก้ไข path ให้ตรงกับโมเดลของคุณ)
        self.detected_plastic_bottle = False
        self.detection_start_time = None

    def start_camera_thread(self):
        """
        ฟังก์ชันเริ่มต้นกล้องใน thread แยก
        """
        if not self.camera_running:
            thread = Thread(target=self.open_camera_with_opencv)
            thread.start()

    def open_camera_with_opencv(self):
        """
        เปิดกล้องด้วย OpenCV
        """
        if self.capture is not None:
            self.stop_camera()

        self.capture = cv2.VideoCapture(1)  # ใช้ index 1 สำหรับ USB camera
        if not self.capture.isOpened():
            print("Error: Could not open the USB camera.")
            return

        self.camera_running = True
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)

    def update_frame(self, dt):
        """
        อัปเดตภาพจากกล้องและแสดงในหน้าจอ Kivy
        """
        if self.capture is None or not self.capture.isOpened():
            print("Error: Camera is not opened.")
            self.stop_camera()
            return

        ret, frame = self.capture.read()
        if ret:
            # Flip the frame vertically
            frame = cv2.flip(frame, 0)

            # Convert the frame to RGB for YOLO
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Run the YOLO model
            results = self.model(img)

            # Draw bounding boxes on the frame
            self.detected_plastic_bottle = False
            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy()
                confidences = result.boxes.conf.cpu().numpy()
                class_ids = result.boxes.cls.cpu().numpy()

                for box, confidence, class_id in zip(boxes, confidences, class_ids):
                    x1, y1, x2, y2 = map(int, box)
                    label = f"{self.model.names[int(class_id)]} {confidence:.2f}"
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    if self.model.names[int(class_id)] == "plastic_bottle":
                        self.detected_plastic_bottle = True
                        if self.detection_start_time is None:
                            self.detection_start_time = time.time()

            if self.detected_plastic_bottle:
                # ตรวจสอบเวลาที่ผ่านไป
                elapsed_time = time.time() - self.detection_start_time
                if elapsed_time >= 3:
                    print("Plastic bottle detected for 3 seconds. Switching to ResultScreen...")
                    self.detect_object()
            else:
                self.detection_start_time = None

            # Flip the frame back for display
            frame = cv2.flip(frame, 0)

            # Convert the frame to Kivy texture
            buf = frame.tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
            texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
            self.ids.camera_view.texture = texture
        else:
            print("Error: Failed to read frame from camera.")
            self.stop_camera()

    def detect_object(self):
        """
        ฟังก์ชันนี้จะเรียกเมื่อมีการตรวจจับวัตถุ (ในที่นี้จำลองการตรวจจับ)
        """
        detected_class = "plastic_bottle"  # คุณสามารถเชื่อมต่อกับ YOLO หรือโมเดลอื่นได้ในส่วนนี้

        if detected_class == "plastic_bottle":
            # เปลี่ยนค่า obj ใน ResultScreen
            result_screen = self.manager.get_screen('result')
            result_screen.obj = 'Bottle'
            result_screen.change_video(f'video/result/Bottle.mp4')  # อัปเดตวิดีโอ
            print("Detected: Plastic Bottle")
            print("Switching to ResultScreen with updated object and video.")
            # เปลี่ยนหน้าจอไปยัง ResultScreen
            self.manager.current = 'result'
            self.stop_camera()
        else:
            print("No object detected.")

    def stop_camera(self):
        """
        หยุดกล้อง
        """
        if self.capture:
            Clock.unschedule(self.update_frame)
            self.capture.release()
            self.capture = None
            self.camera_running = False
            print("Camera has been stopped.")

if __name__ == "__main__":
    import kivy
    from kivymd.app import MDApp
    from kivy.core.window import Window

    Window.size = (1024, 600)

    class MyApp(MDApp):
        def build(self):
            return ScanScreen()

    MyApp().run()
