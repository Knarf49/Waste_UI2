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
from kivymd.uix.label import MDLabel

Builder.load_string('''
<ScanScreen>:
    name: "scan"
    canvas.before:
        Color:
            rgba: (221/255, 237/255, 233/255, 1)
        Rectangle:
            size: self.size
            pos: self.pos

    FloatLayout:
        CameraImage:
            id: camera_view
            size_hint: .7, .7
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
        
        MDLabel:
            id: status_label
            text: "กำลังเปิดกล้อง..."
            font_name: 'prompt-B'
            font_size: "30sp"
            halign: "center"
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            theme_text_color: "Custom"
            text_color: 0, 0, 0, 1
            opacity: 0
''')

class CameraImage(Image):
   pass

class ScanScreen(Screen):
   def __init__(self, **kwargs):
       super().__init__(**kwargs)
       
       # Initialize variables
       self.capture = None
       self.camera_running = False
       self.detection_start_time = None
       self.update_event = None
       
       try:
           # Load YOLO model
           self.model = YOLO("best.pt")
       except Exception as e:
           print(f"Error loading YOLO model: {e}")

   def on_enter(self):
       """Called when the screen is displayed"""
       print("Entering scan screen...")
       # แสดงข้อความก่อนเริ่มเปิดกล้อง
       self.ids.status_label.opacity = 1
       if not self.camera_running:
           self.start_camera()

   def on_leave(self):
       """Called when leaving the screen"""
       self.stop_camera()

   def start_camera(self):
       """Start the camera"""
       if not self.camera_running:
           try:
               self.capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)
               if self.capture.isOpened():
                   # Set camera properties
                   self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                   self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                   
                   ret, test_frame = self.capture.read()
                   if ret:
                       print("Successfully opened camera 1")
                       self.camera_running = True
                       # ซ่อนข้อความเมื่อกล้องเปิดสำเร็จ
                       self.ids.status_label.opacity = 0
                       self.update_event = Clock.schedule_interval(self.update_frame, 1.0 / 30.0)
                       return
                   else:
                       print("Could not read frame from camera")
                       self.capture.release()
                       # แสดงข้อความ error
                       self.ids.status_label.text = "ไม่สามารถเปิดกล้องได้"
               else:
                   print("Could not open camera 1")
                   # แสดงข้อความ error
                   self.ids.status_label.text = "ไม่พบกล้อง"
                   
           except Exception as e:
               print(f"Error opening camera: {e}")
               if self.capture:
                   self.capture.release()
               # แสดงข้อความ error
               self.ids.status_label.text = "เกิดข้อผิดพลาดในการเปิดกล้อง"

   def update_frame(self, dt):
        """Update camera frame"""
        if not self.camera_running or not self.capture:
            return False

        try:
            ret, frame = self.capture.read()
            if not ret:
                print("Failed to get frame")
                self.stop_camera()
                return False

            # Process frame
            frame = cv2.flip(frame, 0)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Run YOLO detection
            results = self.model(img)
            
            # Process YOLO results
            self.detected_plastic_bottle = False
            self.detected_aluminium_can = False  # เพิ่มตัวแปรสำหรับ aluminium can
            
            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy()
                confidences = result.boxes.conf.cpu().numpy()
                class_ids = result.boxes.cls.cpu().numpy()

                for box, confidence, class_id in zip(boxes, confidences, class_ids):
                    x1, y1, x2, y2 = map(int, box)
                    label = f"{self.model.names[int(class_id)]} {confidence:.2f}"
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # ตรวจสอบทั้ง plastic_bottle และ aluminium_can
                    if self.model.names[int(class_id)] == "plastic_bottle":
                        self.detected_plastic_bottle = True
                        if self.detection_start_time is None:
                            self.detection_start_time = time.time()
                    elif self.model.names[int(class_id)] == "aluminium_can":
                        self.detected_aluminium_can = True
                        if self.detection_start_time is None:
                            self.detection_start_time = time.time()

            # ตรวจสอบเวลาและเปลี่ยนหน้าตามวัตถุที่ตรวจพบ
            if self.detection_start_time is not None:
                elapsed_time = time.time() - self.detection_start_time
                if elapsed_time >= 3:
                    if self.detected_plastic_bottle:
                        self.switch_to_result('video/result/Bottle.mp4', 'Bottle')
                    elif self.detected_aluminium_can:
                        self.switch_to_result('video/result/Aluminium.mp4', 'Aluminium')
            else:
                self.detection_start_time = None

            # Convert to texture
            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.ids.camera_view.texture = texture

        except Exception as e:
            print(f"Error in update_frame: {e}")
            self.stop_camera()
            return False

        return True

   def stop_camera(self):
       """Stop the camera"""
       if self.update_event:
           self.update_event.cancel()
           self.update_event = None
       
       if self.capture:
           self.capture.release()
           self.capture = None
       
       self.camera_running = False
       # ซ่อนข้อความเมื่อปิดกล้อง
       self.ids.status_label.opacity = 0
       print("Camera stopped")

   def switch_to_result(self, video_path, detected_object):
        """Switch to result screen with specific video"""
        self.stop_camera()
        result_screen = self.manager.get_screen("result")
        result_screen.change_video(video_path, detected_object)
        self.manager.current = 'result'

if __name__ == "__main__":
    import kivy
    from kivymd.app import MDApp
    from kivy.core.window import Window

    Window.size = (1024, 600)

    class MyApp(MDApp):
        def build(self):
            return ScanScreen()

    MyApp().run()