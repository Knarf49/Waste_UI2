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
SCAN_DELAY = 1.4

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
        self.confidence_threshold = 0.5  # Set 50% confidence threshold
        
        try:
            # โหลดโมเดลทั้ง 4 ตัว
            self.models = [
                YOLO(r"main.pt"),
                YOLO(r"snack_package.pt"),
                YOLO(r"plbag.pt"),
                YOLO(r"plcup.pt")
            ]
        except Exception as e:
            print(f"Error loading YOLO models: {e}")

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
        
        # กำหนดหมายเลขกล้อง
        camera_port=0

        """Start the camera"""
        if not self.camera_running:
            try:
                self.capture = cv2.VideoCapture(camera_port, cv2.CAP_DSHOW)
                if self.capture.isOpened():
                    # Set camera properties
                    self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    
                    ret, test_frame = self.capture.read()
                    if ret:
                        print(f"Successfully opened camera {camera_port}")
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
                    print(f"Could not open camera {camera_port}")
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
            frame = cv2.flip(frame, 1) #1=horizontal, 0=vertical, -1=both
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # ตัวแปรเก็บผลการตรวจจับที่ดีที่สุด
            best_detection = {
                'confidence': 0,
                'class_name': None,
                'box': None,
                'model_index': None
            }

            # Run detection ด้วยทุกโมเดล
            for i, model in enumerate(self.models):
                results = model(img)
                
                for result in results:
                    boxes = result.boxes.xyxy.cpu().numpy()
                    confidences = result.boxes.conf.cpu().numpy()
                    class_ids = result.boxes.cls.cpu().numpy()

                    for box, confidence, class_id in zip(boxes, confidences, class_ids):
                        # เก็บผลการตรวจจับที่มี confidence สูงกว่า threshold และสูงที่สุด
                        if confidence > self.confidence_threshold and confidence > best_detection['confidence']:
                            best_detection = {
                                'confidence': confidence,
                                'class_name': model.names[int(class_id)],
                                'box': box,
                                'model_index': i
                            }

            # ถ้ามีการตรวจจับที่ดีที่สุดและมี confidence สูงกว่า threshold
            if best_detection['class_name'] is not None:
                x1, y1, x2, y2 = map(int, best_detection['box'])
                label = f"{best_detection['class_name']} {best_detection['confidence']:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # ตรวจสอบวัตถุและเวลา
                if best_detection['class_name'] in ["plastic_bottle", "aluminium_can","plastic_cup"]:
                    if self.detection_start_time is None:
                        self.detection_start_time = time.time()
                    
                    elapsed_time = time.time() - self.detection_start_time
                    if elapsed_time >= SCAN_DELAY:
                         # Corrected conditional assignment
                        if best_detection['class_name'] == 'plastic_bottle':
                            video_path = 'video/result/Bottle.mp4'
                        elif best_detection['class_name'] == 'aluminium_can':
                            video_path = 'video/result/Aluminium.mp4'
                        else:
                            video_path = 'video/result/Plastic_cup.mp4'
                        
                        self.switch_to_result(video_path, best_detection['class_name'])
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

# if __name__ == "__main__":
#     import kivy
#     from kivymd.app import MDApp
#     from kivy.core.window import Window

#     Window.size = (1024, 600)

#     class MyApp(MDApp):
#         def build(self):
#             return ScanScreen()

#     MyApp().run()