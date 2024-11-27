from kivy.uix.screenmanager import Screen
# from green_screen import process_green_screen

# Load the KV file
# Builder.load_file('mascot.kv')  # Ensure mascot.kv is in the same directory

class Mascot2Screen(Screen):
    def on_enter(self):
        # Start video playback when entering the screen
        video = self.ids.mascot_video
        video.state = "play"
        video.source = "video/mascotP2.mp4"  # Ensure this path is correct
        video.options = {"eos": "loop"}  # Ensure looping works
        video.allow_stretch = True

    # process_green_screen("video/mascot_green.mp4", "video/processed_mascot.mp4")
