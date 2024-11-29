from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.uix.video import Video  # Import Video widget to display the video
from kivy.uix.button import Button  # Import button widget to interact
from kivy.uix.label import Label


class ResultScreen(Screen):
    video_source = StringProperty("")  # Initial empty video source
    obj = StringProperty('')  # Default empty object

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Create the video player and set it up
        self.video_player = Video(source=self.video_source, state='play', options={'eos': 'loop'})
        self.video_player.size_hint = (1, 1)
        self.video_player.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Add video player to layout
        layout.add_widget(self.video_player)

        # Add a label to display which object is detected
        self.object_label = Label(text=f"Detected: {self.obj}", size_hint=(None, None), size=(200, 50))
        self.object_label.pos_hint = {'center_x': 0.5, 'y': 0.05}
        layout.add_widget(self.object_label)

        # Add a button to return to the previous screen or go to endcredits
        self.end_button = Button(text="End Credits", size_hint=(None, None), size=(200, 50))
        self.end_button.pos_hint = {'center_x': 0.5, 'y': 0.1}
        self.end_button.bind(on_press=self.on_end_button_click)
        layout.add_widget(self.end_button)

        # Add the layout to the screen
        self.add_widget(layout)

    def change_video(self, new_source, detected_obj):
        """
        Change the video source dynamically and update the object label.
        """
        self.video_source = new_source
        self.obj = detected_obj
        self.video_player.source = new_source  # Set the new video source
        self.video_player.play()  # Start the video playback
        self.object_label.text = f"Detected: {detected_obj}"  # Update the detected object label
        print(f"Video source changed to: {new_source}")

    def on_end_button_click(self, instance):
        """
        Switch to the 'endcredit' screen when the button is clicked.
        """
        print("End credits button clicked!")
        self.manager.current = "endcredit"  # Navigate to 'endcredit' screen
