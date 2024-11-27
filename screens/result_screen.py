from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty


class ResultScreen(Screen):
    video_source = StringProperty("")  # Initial empty video source
    obj='Bottle'
    new_source = StringProperty(f'video/result/{obj}.mp4')  # Default new source

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Add the layout to the screen
        self.add_widget(layout)

        self.change_video(self.new_source)

    def change_video(self, new_source):
        """
        Change the video source dynamically.
        """
        self.video_source = new_source
        print(f"Video source changed to: {new_source}")
