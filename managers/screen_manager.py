from kivy.uix.screenmanager import ScreenManager, FadeTransition
from screens.EndCredit import EndCreditScreen
from screens.page2_screen import Page2Screen
from screens.result_screen import ResultScreen
from screens.mascot_page import MascotScreen
from screens.mascot2_page import Mascot2Screen
from screens.ShowBin import ShowbinScreen
from screens.Scan_page import ScanScreen

class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add screens to the ScreenManager
        self.add_widget(MascotScreen(name="mascot"))
        self.add_widget(Mascot2Screen(name="mascot2"))
        self.add_widget(ShowbinScreen(name="showbin"))
        self.add_widget(Page2Screen(name="page2"))
        self.add_widget(ScanScreen(name="scan"))
        self.add_widget(ResultScreen(name="result"))
        self.add_widget(EndCreditScreen(name="endcredit"))