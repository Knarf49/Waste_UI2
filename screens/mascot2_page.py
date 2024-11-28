from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

class Mascot2Screen(Screen):
    def on_enter(self):
        """Start the video playback and schedule transition."""
        # Set video source and start playback
        video = self.ids.mascot_video
        video.source = "video/greeting.mp4"  # Ensure this path is correct
        video.state = "play"
        video.allow_stretch = True

        # Schedule transition to the next screen after 3 seconds
        Clock.schedule_once(self.go_to_next_screen, 6)

    def go_to_next_screen(self, dt):
        """Transition to the 'showbin' screen."""
        self.manager.current = "showbin"
