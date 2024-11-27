from kivy.uix.screenmanager import Screen

class ShowBinScreen(Screen):
    def on_enter(self):
        # Start video playback when entering the screen
        video = self.ids.showbin_video
        video.state = "play"
        video.source = "video/Showbin.mp4"  # Ensure this path is correct
        video.options = {"eos": "loop"}  # Ensure looping works
        video.allow_stretch = True