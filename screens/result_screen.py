from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.uix.video import Video
from kivymd.uix.button import MDRaisedButton
from kivy.core.audio import SoundLoader

class ResultScreen(Screen):
    video_source = StringProperty("")
    obj = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_sounds()
        self._init_ui()

    def _init_sounds(self):
        """Initialize sound files"""
        self.button_sound = SoundLoader.load('sound/button_sound.mp3')
        self.voice_sound = SoundLoader.load('sound/plastic.m4a')
        if self.voice_sound:
            self.voice_sound.volume = 1.0

    def _init_ui(self):
        """Initialize UI components"""
        layout = FloatLayout()

        # Video player setup
        self.video_player = Video(
            source=self.video_source,
            state='play',
            options={'eos': 'loop'},
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        layout.add_widget(self.video_player)

        # Home button setup
        home_button = self._create_home_button()
        layout.add_widget(home_button)

        self.add_widget(layout)

    def _create_home_button(self):
        """Create and return the home button"""
        button = MDRaisedButton(
            text="กลับสู่หน้าหลัก",
            font_name='prompt-B',
            font_size="40sp",
            size_hint=(None, None),
            size=("850dp", "450dp"),
            pos_hint={"center_x": 0.85, "center_y": 0.2},
            md_bg_color=[0.85, 1, 0.85, 1],
            text_color=[0, 0, 0, 1],
            line_color=[0, 0, 0, 1],
            line_width=2,
            elevation=2,
            ripple_color=[0.9, 0.9, 0.9, 1],
        )
        button.bind(on_release=self.play_button_sound)
        button.bind(on_release=self.go_to_endcredit)
        return button

    def change_video(self, new_source, detected_obj):
        """Change video source and handle object detection"""
        try:
            self.video_source = new_source
            self.obj = detected_obj
            self.video_player.source = new_source
            self.video_player.state = 'play'
            
            if detected_obj == 'plastic_bottle':
                if self.voice_sound:
                    self.voice_sound.play()
            
            print(f"Video changed for detected object: {detected_obj}")
            
        except Exception as e:
            print(f"Error changing video: {e}")

    def play_button_sound(self, *args):
        """Play button click sound"""
        if self.button_sound:
            self.button_sound.play()

    def go_to_endcredit(self, *args):
        """Navigate to end credit screen"""
        if self.voice_sound:
            self.voice_sound.stop()
        self.manager.current = "endcredit"

    def on_leave(self):
        """Cleanup when leaving screen"""
        if self.voice_sound:
            self.voice_sound.stop()
        if self.button_sound:
            self.button_sound.stop()
        if self.video_player:
            self.video_player.state = 'stop'