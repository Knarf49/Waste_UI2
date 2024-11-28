from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty


class ResultScreen(Screen):
    video_source = StringProperty("")  # Initial empty video source
    obj = StringProperty('')  # Default empty object

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        self.add_widget(layout)

    def change_video(self, new_source):
        """
        Change the video source dynamically.
        """
        self.video_source = new_source
        print(f"Video source changed to: {new_source}")
