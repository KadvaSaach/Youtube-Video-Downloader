from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.lang import Builder

# Custom styles using Kivy’s Builder for rounded corners and background styles
Builder.load_string(
    """
<ButtonStyle>:
    background_normal: ''
    background_color: (0, 0, 0, 0)
    color: (1, 1, 1, 1)
    canvas.before:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [10]
"""
)

# Importing the backend downloader
from backend import YoutubeDownloader as YTD

import tkinter as tk
from tkinter import filedialog

window = get_color_from_hex("#FFFFFF")
# window = get_color_from_hex("#000000")


class ButtonStyle(Button):
    pass


class GUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10

        self.spinner = Spinner(
            text="Select Download type....",
            values=(
                "Download Video",
                "Download Playlist of Videos",
                "Download Audio",
                "Download Playlist of Audios",
            ),
            size_hint=(1, 0.1),
            background_color=get_color_from_hex("#1E88E5"),
            background_normal="",
        )
        self.add_widget(self.spinner)

        self.url_input = TextInput(
            size_hint=(1, 0.2),
            multiline=False,
            hint_text="Please Enter YouTube URL ",
            background_normal="",
            background_color=get_color_from_hex("#333333"),
            foreground_color=(1, 1, 1, 1),
        )
        self.add_widget(self.url_input)

        self.path_input = TextInput(
            size_hint=(1, 1.5),
            multiline=False,
            readonly=True,
            hint_text="Enter the path to save your file ",
            background_normal="",
            background_color=get_color_from_hex("#333333"),
            foreground_color=(1, 1, 1, 1),
        )
        self.add_widget(self.path_input)

        # Browse button with custom style
        self.path_button = ButtonStyle(
            text="Browse",
            size_hint=(1, 0.1),
            background_color=get_color_from_hex("#4CAF50"),  # Green
        )
        self.path_button.bind(on_press=self.open_file_dialog)
        self.add_widget(self.path_button)

        # Download button with custom style
        self.download_button = ButtonStyle(
            text="Download",
            size_hint=(1, 0.1),
            background_color=get_color_from_hex("#E53935"),  # Red
        )
        self.download_button.bind(on_press=self.start_download)
        self.add_widget(self.download_button)

        self.message_label = Label(
            size_hint=(1, 0.1), color=get_color_from_hex("#BDBDBD")
        )
        self.add_widget(self.message_label)

    def open_file_dialog(self, instance):
        root = tk.Tk()
        root.withdraw()
        path_dir = filedialog.askdirectory()
        if path_dir:
            self.path_input.text = path_dir

    def start_download(self, instance):
        print(f"User pressed the download button")
        download_type = self.spinner.text
        url = self.url_input._get_text()
        print("----------------------------")
        print(f"URL : {url}")
        print("----------------------------")
        save_path = self.path_input.text.strip()

        if not url:
            self.message_label.text = "Please enter a valid URL...."
            return

        if not save_path:
            self.message_label.text = (
                "You must choose a file path for your download...."
            )
            return

        downloader = YTD()

        try:
            if download_type == "Download Video":
                YTD.single_video_download(url, save_path)
            elif download_type == "Download Playlist of Videos":
                YTD.playlist_download(url, save_path)
            elif download_type == "Download Audio":
                YTD.video_as_audio_download(url, save_path)
            elif download_type == "Download Playlist of Audios":
                YTD.playlist_as_mp3_download(url, save_path)

            self.message_label.text = (
                "Download started! Check your downloads folder.....!!!"
            )
        except Exception as e:
            self.message_label.text = f"Error: {str(e)}"
            print("Error details:", str(e))


class YTDAPP(App):
    def build(self):
        return GUI()


if __name__ == "__main__":
    YTDAPP().run()
