from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from green_screen import process_green_screen

# Load the KV file
# Builder.load_file('mascot.kv')  # Ensure mascot.kv is in the same directory

class MascotScreen(Screen):
    process_green_screen("video/mascot_green.mp4", "video/processed_mascot.mp4")
