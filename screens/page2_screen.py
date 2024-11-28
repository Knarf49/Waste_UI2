from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import random

class Page2Screen(Screen):
    def on_enter(self, *args):
        """Called when the screen is entered."""
        # Show spinner and hide button initially
        self.ids.loading_spinner.opacity = 1
        self.ids.loading_spinner.active = True
        self.ids.delayed_button.opacity = 0
        self.ids.delayed_button.disabled = True

        # Start the spinner and schedule video playback
        #เปลี่ยนตัวหม
        Clock.schedule_once(self.show_button, 8)  # Show button after 5 seconds
        self.play_random_video()

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
        # Randomly select a video from the list
        selected_video = random.choice(video_sources)
        # Set the video player's source to the selected video
        self.ids.video_player.source = selected_video
        # Start playing the video
        self.ids.video_player.state = 'play'

    def show_button(self, *args):
        """Show the button and stop the spinner."""
        self.ids.loading_spinner.opacity = 0
        self.ids.loading_spinner.active = False
        self.ids.delayed_button.opacity = 1
        self.ids.delayed_button.disabled = False
