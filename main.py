%%writefile main.py
import os
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
import yt_dlp

class BannaPlayer(App):
    def build(self):
        self.sound = None
        self.music_dir = "./BannaOfflineMusic"
        if not os.path.exists(self.music_dir):
            os.makedirs(self.music_dir)

        Window.clearcolor = (0.04, 0.04, 0.04, 1) # Spotify Dark Theme
        main_layout = BoxLayout(orientation='vertical', padding=25, spacing=15)

        title_lbl = Label(text="BANNA PLAYER 🎵", font_size='28sp', bold=True, color=(0.11, 0.72, 0.33, 1), size_hint_y=None, height=60)
        main_layout.add_widget(title_lbl)

        self.search_input = TextInput(hint_text="Artist, gaana ya album khojein...", multiline=False, size_hint_y=None, height=50, font_size='16sp', background_color=(0.12, 0.12, 0.12, 1), foreground_color=(1, 1, 1, 1), hint_text_color=(0.5, 0.5, 0.5, 1))
        main_layout.add_widget(self.search_input)

        self.play_online_btn = Button(text="▶ Play Online (No Download)", background_color=(0.11, 0.72, 0.33, 1), font_size='16sp', bold=True, background_normal='', size_hint_y=None, height=50)
        self.play_online_btn.bind(on_press=self.start_online_thread)
        main_layout.add_widget(self.play_online_btn)

        self.download_btn = Button(text="📥 Download to Offline Storage", background_color=(0.2, 0.2, 0.2, 1), font_size='16sp', bold=True, background_normal='', size_hint_y=None, height=50)
        self.download_btn.bind(on_press=self.start_download_thread)
        main_layout.add_widget(self.download_btn)

        self.play_offline_btn = Button(text="📁 Play Downloaded Songs", background_color=(0.3, 0.3, 0.3, 1), font_size='16sp', bold=True, background_normal='', size_hint_y=None, height=50)
        self.play_offline_btn.bind(on_press=self.play_offline_logic)
        main_layout.add_widget(self.play_offline_btn)

        self.status_lbl = Label(text="Status: Banna Player Taiyar Hai.", font_size='14sp', color=(0.7, 0.7, 0.7, 1), halign='center', size_hint_y=None, height=40)
        main_layout.add_widget(self.status_lbl)
        
        self.stop_btn = Button(text="Stop Music", background_color=(0.8, 0.2, 0.2, 1), bold=True, background_normal='', size_hint_y=None, height=45)
        self.stop_btn.bind(on_press=self.stop_music)
        main_layout.add_widget(self.stop_btn)

        return main_layout

    def update_status(self, text):
        self.status_lbl.text = f"Status: {text}"

    def start_online_thread(self, instance):
        song_name = self.search_input.text.strip()
        if not song_name:
            self.update_status("Kripya gane ka naam likhein!")
            return
        self.update_status("Searching online stream...")
        threading.Thread(target=self.play_online_logic, args=(song_name,)).start()

    def play_online_logic(self, song_name):
        try:
            ydl_opts = {'format': 'bestaudio/best', 'noplaylist': True, 'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{song_name}", download=False)
                video_url = info['entries'][0]['url']
                self.update_status(f"Streaming: {info['entries'][0]['title'][:25]}...")
                self.play_audio(video_url)
        except Exception as e:
            self.update_status("Streaming fail! Network check karein.")

    def start_download_thread(self, instance):
        song_name = self.search_input.text.strip()
        if not song_name:
            self.update_status("Pehle gane ka naam toh likho!")
            return
        self.update_status("Downloading started...")
        threading.Thread(target=self.download_logic, args=(song_name,)).start()

    def download_logic(self, song_name):
        try:
            ydl_opts = {'format': 'bestaudio/best', 'outtmpl': os.path.join(self.music_dir, '%(title)s.%(ext)s'), 'noplaylist': True, 'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{song_name}", download=True)
                self.update_status(f"💾 Saved Offline:\n{info['entries'][0]['title'][:25]}")
        except Exception as e:
            self.update_status("Download nahi ho paya.")

    def play_offline_logic(self, instance):
        songs = os.listdir(self.music_dir)
        if not songs:
            self.update_status("Koyi offline song nahi mila!")
            return
        latest_song_path = os.path.join(self.music_dir, songs[-1])
        self.update_status(f"🎵 Playing Offline:\n{songs[-1][:25]}")
        self.play_audio(latest_song_path)

    def play_audio(self, path_or_url):
        if self.sound: self.sound.stop()
        self.sound = SoundLoader.load(path_or_url)
        if self.sound: self.sound.play()

    def stop_music(self, instance):
        if self.sound:
            self.sound.stop()
            self.update_status("Music Stopped.")

if __name__ == '__main__':
    BannaPlayer().run()
