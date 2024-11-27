from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
# from green_screen import process_green_screen

# Load the KV file
# Builder.load_file('mascot.kv')  # Ensure mascot.kv is in the same directory

class Mascot2Screen(Screen):
    def on_enter(self):
        # Start video playback when entering the screen
        video = self.ids.mascot_video
        video.state = "play"
        video.source = "video/greeting.mp4"  # Ensure this path is correct
        video.allow_stretch = True

        # Schedule transition to the next screen after 2 seconds
        Clock.schedule_once(self.go_to_next_screen, 4)

    def go_to_next_screen(self, dt):
        # Transition to the "next_screen"
        self.manager.current = "showbin"