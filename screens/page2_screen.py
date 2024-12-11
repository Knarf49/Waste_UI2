from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import random

class Page2Screen(Screen):
    def on_enter(self, *args):
        """Called when the screen is entered."""
        # แสดง spinner
        self.ids.loading_spinner.opacity = 1
        self.ids.loading_spinner.active = True

        # เล่นวิดีโอ
        self.play_random_video()
        
        # เริ่มเปิดกล้องที่ 5 วินาที
        Clock.schedule_once(self.prepare_camera, 2.7)
        # เปลี่ยนหน้าที่ 8 วินาที
        Clock.schedule_once(self.switch_to_scan, 3.5)

    def prepare_camera(self, dt):
        """เตรียมกล้องก่อนเปลี่ยนหน้า"""
        scan_screen = self.manager.get_screen('scan')
        scan_screen.start_camera()

    def play_random_video(self):
        """Select and play a random video."""
        video_sources = [
            'video/loading/B-loading1.mp4',
            'video/loading/G-loading1.mp4',
            'video/loading/R-loading1.mp4',
            'video/loading/Y-loading1.mp4',
            'video/loading/Y-loading2.mp4',
            'video/loading/Y-loading3.mp4',
        ]
        selected_video = random.choice(video_sources)
        self.ids.video_player.source = selected_video
        self.ids.video_player.state = 'play'

    def switch_to_scan(self, *args):
        """Switch to scan screen after loading."""
        self.manager.current = 'scan'
        self.manager.transition.direction = 'left'