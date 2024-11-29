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


class CameraImage(Image):
    pass

class ScanScreen(Screen):
    CAMERA_INDEX = 0
    MAIN_MODEL = r"main.pt"  # Path to your YOLO model

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = None
        self.model = YOLO(self.MAIN_MODEL)
        self.camera_running = False
        self.detection_start_time = None

    def on_enter(self, *args):
        """
        Called when the screen is entered. Starts the camera automatically.
        """
        super().on_enter(*args)
        self.start_camera_thread()
        print(self.model.names) 

    def on_leave(self, *args):
        """
        Called when the screen is left. Stops the camera.
        """
        super().on_leave(*args)
        self.stop_camera()

    def start_camera_thread(self):
        """
        Starts the camera in a new thread.
        """
        self.ids.detection_status.text = "กำลังเปิดกล้อง..."  # Update the label text to "Opening camera..."
        if not self.camera_running:
            self.open_camera_with_opencv()

    def open_camera_with_opencv(self):
        """
        Opens the camera using OpenCV.
        """
        self.capture = cv2.VideoCapture(self.CAMERA_INDEX)
        if not self.capture.isOpened():
            self.ids.detection_status.text = "ข้อผิดพลาด: ไม่สามารถเปิดกล้องได้"  # Error message in case of failure
            return
        self.camera_running = True
        self.ids.detection_status.text = "ไม่พบวัตถุ"  # No object detected message
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)

    def update_frame(self, dt):
        """
        Updates the camera frame and runs object detection.
        """
        if self.capture is None or not self.capture.isOpened():
            self.stop_camera()
            return

        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 1)  # Mirror the frame
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = self.model(img)
            best_detection = self.get_best_detection(results, frame)

            if best_detection:
                x1, y1, x2, y2 = map(int, best_detection["box"])
                label = f"{best_detection['class_name']} {best_detection['confidence']:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

                self.ids.detection_status.text = f"พบวัตถุ: {best_detection['class_name']}"  # Object detected message
            else:
                self.ids.detection_status.text = "ไม่พบวัตถุ"  # No object detected message

            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
            texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
            self.ids.camera_view.texture = texture

    def get_best_detection(self, results, frame):
        """
        Processes YOLO results and returns the best detection.
        """
        best_detection = None
        max_confidence = 0

        for result in results:
            for box, confidence, class_id in zip(result.boxes.xyxy.cpu().numpy(),
                                                 result.boxes.conf.cpu().numpy(),
                                                 result.boxes.cls.cpu().numpy()):
                if confidence > max_confidence:
                    max_confidence = confidence
                    best_detection = {
                        "box": box,
                        "confidence": confidence,
                        "class_name": result.names[int(class_id)]
                    }

        return best_detection

    def stop_camera(self):
        """
        Stops the camera.
        """
        if self.capture:
            Clock.unschedule(self.update_frame)
            self.capture.release()
            self.capture = None
            self.camera_running = False
            self.ids.detection_status.text = "กล้องปิดแล้ว"  # Camera closed message
