from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

class EndCreditScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_sounds()

    def _init_sounds(self):
        """Initialize sound files"""
        self.whoosh_sound = SoundLoader.load('sound/whoosh.mp3')
        
        if self.whoosh_sound:
            self.whoosh_sound.volume = 1.0

    def on_enter(self):
        # Start playing the video when entering the screen
        self.ids.thankVdo.state = "play"

        # Schedule a transition after 5 seconds
        Clock.schedule_once(self.go_to_mascot, 5)

        #play whoosh sound after 3 seconds
        Clock.schedule_once(self.play_whoosh_sound, 3)

    def on_leave(self):
        # Pause the video and cancel any scheduled tasks when leaving the screen
        self.ids.thankVdo.state = "pause"
        Clock.unschedule(self.go_to_mascot)
        Clock.unschedule(self.play_whoosh_sound)

    def go_to_mascot(self, dt):
        # Transition to the mascot page
        self.manager.current = "mascot"
        self.manager.transition.direction = "right"

    def play_whoosh_sound(self, dt):
        if self.whoosh_sound:
            self.whoosh_sound.play()    
