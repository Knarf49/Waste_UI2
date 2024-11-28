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

    def on_video_click(self, instance, touch):
        # Check if the touch event was inside the video area
        if instance.collide_point(*touch.pos):  # Check if the click is inside the video widget
            print("Video clicked!")
            self.manager.current = "endcredit"  # Switch to the 'endcredit' screen