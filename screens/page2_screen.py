from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

class Page2Screen(Screen):
    video_sources=[
        
    ]
    # def on_enter(self):
    #     self.ids.loading_spinner.active = True
    #     Clock.schedule_once(self.show_button, 20)
    #     # self.carousel_interval = Clock.schedule_interval(self.automate_carousel, 8)
    #     self.update_video_states()

    # def on_leave(self):
    #     if hasattr(self, 'carousel_interval'):
    #         Clock.unschedule(self.carousel_interval)

        # for slide in self.ids.carousel.slides:
        #     video = slide.children[0]
        #     video.state = "pause"

    # def show_button(self, dt):
    #     self.ids.loading_spinner.active = False
    #     self.manager.current = "result"
    #     self.manager.transition.direction = 'left'

    # def automate_carousel(self, dt):
    #     carousel = self.ids.carousel
    #     next_index = (carousel.index + 1) % len(carousel.slides)
    #     carousel.load_slide(carousel.slides[next_index])
    #     self.update_video_states()

    # def update_video_states(self):
    #     carousel = self.ids.carousel
    #     current_slide = carousel.current_slide

    #     for slide in carousel.slides:
    #         video = slide.children[0]
    #         video.state = "play" if slide == current_slide else "pause"

    # def stop_auto_carousel(self):
    #     """Stop the automatic carousel when user interacts manually."""
    #     if hasattr(self, 'carousel_interval'):
    #         Clock.unschedule(self.carousel_interval)
    #         del self.carousel_interval  # Clean up the attribute
