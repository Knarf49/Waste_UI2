from kivy.core.text import LabelBase
from kivymd.app import MDApp
from managers.screen_manager import MyScreenManager, FadeTransition
from kivy.lang import Builder
from kivy.core.window import Window

# Set fullscreen
Window.fullscreen = 'auto'  # หรือใช้ Window.fullscreen = True
# Window.size = (1024, 600)  # ไม่จำเป็นต้องกำหนดขนาดเมื่อใช้ fullscreen

# Register fonts globally
LabelBase.register(name='Cooper-B', fn_regular='fonts/cooper/CooperHewitt-Bold.otf')
LabelBase.register(name='Cooper-M', fn_regular='fonts/cooper/CooperHewitt-Medium.otf')
LabelBase.register(name='prompt-R', fn_regular='fonts/Prompt/Prompt-Regular.ttf')
LabelBase.register(name='prompt-B', fn_regular='fonts/Prompt/Prompt-Bold.ttf')
LabelBase.register(name='prompt-Semi', fn_regular='fonts/Prompt/Prompt-SemiBold.ttf')

#TODO ทำให้ปุ่มกดไวขึ้น
#TODO เพิ่มเสียงตอนกดปุ่ม / 

# Load KV files
Builder.load_file("kv/idle.kv")
Builder.load_file("kv/page2.kv")
Builder.load_file("kv/result.kv")
Builder.load_file("kv/mascot.kv")
Builder.load_file("kv/mascot2.kv")
Builder.load_file("kv/showbin.kv")
Builder.load_file("kv/endcredit.kv")
Builder.load_file("kv/scan.kv")

class MyApp(MDApp):
    def build(self):
        # ผูกการกดปุ่ม Esc กับการออกจาก fullscreen
        Window.bind(on_keyboard=self.on_keyboard)
        Window.fullscreen = 'auto'
        return MyScreenManager()

    def on_keyboard(self, window, key, *args):
        # กด Esc เพื่อออกจาก fullscreen
        if key == 27:  # 27 คือรหัสปุ่ม Esc
            Window.fullscreen = False
            return True  # ป้องกันการปิดแอพ
        return False

if __name__ == "__main__":
    MyApp().run()