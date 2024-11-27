from kivy.core.text import LabelBase
from kivymd.app import MDApp
from managers.screen_manager import MyScreenManager,FadeTransition
from kivy.lang import Builder
from kivy.core.window import Window

Window.size = (1024, 600)
# Register fonts globally
LabelBase.register(name='Cooper-B', fn_regular='fonts/cooper/CooperHewitt-Bold.otf')
LabelBase.register(name='Cooper-M', fn_regular='fonts/cooper/CooperHewitt-Medium.otf')
LabelBase.register(name='prompt-R', fn_regular='fonts/Prompt/Prompt-Regular.ttf')
LabelBase.register(name='prompt-B', fn_regular='fonts/Prompt/Prompt-Bold.ttf')
LabelBase.register(name='prompt-Semi', fn_regular='fonts/Prompt/Prompt-SemiBold.ttf')

Builder.load_file("kv/idle.kv")
Builder.load_file("kv/page2.kv")
Builder.load_file("kv/result.kv")
Builder.load_file("kv/mascot.kv")
Builder.load_file("kv/mascot2.kv")
Builder.load_file("kv/showbin.kv")
Builder.load_file("kv/Endcredit.kv")

class MyApp(MDApp):
    def build(self):
        return MyScreenManager()

if __name__ == "__main__":
    MyApp().run()
