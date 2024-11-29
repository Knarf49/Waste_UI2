from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

class Mascot2Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # โหลดไฟล์เสียง
        self.sound = SoundLoader.load(r"C:\Users\Frank\Downloads\มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี 6.m4a")
        if self.sound:
            self.sound.volume = 1.0

    def on_enter(self):
        """Start the video playback and schedule transition."""
        # Set video source and start playback
        video = self.ids.mascot_video
        video.source = "video/greeting.mp4"
        video.state = "play"
        video.allow_stretch = True

        # เล่นเสียงหลังจาก 1 วินาที
        Clock.schedule_once(self.play_sound, 0)
        # Schedule transition to the next screen after 3 seconds
        Clock.schedule_once(self.go_to_next_screen, 4)

    def play_sound(self, dt):
        """Play the sound"""
        if self.sound:
            self.sound.play()

    def go_to_next_screen(self, dt):
        """Transition to the 'showbin' screen."""
        if self.sound:
            self.sound.stop()  # หยุดเสียงก่อนเปลี่ยนหน้า
        self.manager.current = "showbin"

    def on_leave(self):
        """Called when leaving the screen"""
        if self.sound:
            self.sound.stop()  # หยุดเสียงเมื่อออกจากหน้า