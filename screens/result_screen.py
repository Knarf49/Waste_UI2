from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.uix.video import Video
from kivymd.uix.button import MDRaisedButton
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Line

class ResultScreen(Screen):
    video_source = StringProperty("")
    obj = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Create the video player and set it up
        self.video_player = Video(source=self.video_source, state='play', options={'eos': 'loop'})
        self.video_player.size_hint = (1, 1)
        self.video_player.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # โหลดไฟล์เสียง
        self.sound = SoundLoader.load(r"C:\Users\Frank\Downloads\มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี 3.m4a")
        if self.sound:
            self.sound.volume = 1.0

        # Add video player to layout
        layout.add_widget(self.video_player)

        # สร้างปุ่มกลับสู่หน้าหลักด้วยสไตล์ใหม่
        home_button = MDRaisedButton(
            text="กลับสู่หน้าหลัก",
            font_name='prompt-B',
            font_size="40sp",
            size_hint=(None, None),
            size=("850dp", "450dp"),
            pos_hint={"center_x": 0.85, "center_y": 0.2},
            md_bg_color= [0.85, 1, 0.85, 1],  # สีเขียวอ่อน
            text_color=[0, 0, 0, 1],   # ตัวอักษรสีดำ
            line_color=[0, 0, 0, 1],   # เส้นขอบสีดำ
            line_width=2,              # ความหนาของเส้นขอบ
            elevation=2,               # เงาบางๆ
            ripple_color=[0.9, 0.9, 0.9, 1],  # สีเมื่อกดปุ่ม
        )
        home_button.bind(on_release=self.go_to_endcredit)
        layout.add_widget(home_button)

        # Add the layout to the screen
        self.add_widget(layout)

    def change_video(self, new_source, detected_obj):
        self.video_source = new_source
        self.obj = detected_obj
        self.video_player.source = new_source
        self.video_player.state = 'play'
        
        if detected_obj == 'Bottle':
            if self.sound:
                self.sound.play()
        
        print(f"Video source changed to: {new_source}")

    def go_to_endcredit(self, instance):
        if self.sound:
            self.sound.stop()
        self.manager.current = "endcredit"

    def on_leave(self):
        if self.sound:
            self.sound.stop()