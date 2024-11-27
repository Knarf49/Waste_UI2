from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

class EndCreditScreen(Screen):
    def on_enter(self):
        # Start playing the video when entering the screen
        self.ids.thankVdo.state = "play"

        # Schedule a transition after 5 seconds
        Clock.schedule_once(self.go_to_mascot, 10)

    def on_leave(self):
        # Pause the video and cancel any scheduled tasks when leaving the screen
        self.ids.thankVdo.state = "pause"
        Clock.unschedule(self.go_to_mascot)

    def go_to_mascot(self, dt):
        # Transition to the mascot page
        self.manager.current = "mascot"
        self.manager.transition.direction = "right"
