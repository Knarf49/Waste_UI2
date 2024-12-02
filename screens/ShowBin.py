from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader

class ShowbinScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound = SoundLoader.load('sound/button_sound.mp3')  # Load your sound file

    def play_sound(self, *args):
        if self.sound:
            self.sound.play()