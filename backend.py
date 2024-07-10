import re
from pytube import Playlist, YouTube
from moviepy.editor import *
import os


class YoutubeDownloader:

    def single_video_download(url, save_path):
        try:
            yt = YouTube(url)
            stream = yt.streams.filter(file_extension="mp4").get_highest_resolution()
            print(f"Video title: {yt.title}")

            # Set the save path and filename
            # filename = (
            #     yt.title.replace("/", "_")
            #     .replace("\\", "_")
            #     .replace(":", "_")
            #     .replace("*", "_")
            #     .replace("?", "_")
            #     .replace('"', "_")
            #     .replace("<", "_")
            #     .replace(">", "_")
            #     .replace("|", "_")
            #     .replace("&", "_")
            #     .replace("%", "_")
            #     .replace("#", "_")
            #     .replace("{", "_")
            #     .replace("}", "_")
            #     .replace("[", "_")
            #     .replace("]", "_")
            #     .replace("=", "_")
            #     .replace("+", "_")
            #     .replace("-", "_")
            #     .replace("--", "_")
            #     .replace(";", "_")
            #     .replace("!", "_")
            #     .replace("@", "_")
            #     .replace("$", "_")
            #     .replace("^", "_")
            #     .replace("`", "_")
            #     .replace("~", "_")
            #     .replace(",", "_")
            #     .replace(".", "_")
            #     .replace(" ", "_")
            # )

            function_patterns = [
                r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)',
                r"\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)",
                r"\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)",
            ]

            for pattern in function_patterns:
                regex = re.compile(pattern)
                modified_title = regex.sub("replacement_string", yt.title)

            filename = modified_title

            # Download with specified filename
            stream.download(output_path=save_path, filename=filename)
            print(f"Download completed! Video saved as -> {filename} in {save_path}")

            # Adding .mp4 extension to the downloaded file
            new_ext = ".mp4"
            sep = "/"

            full_path = save_path + sep + filename

            if not os.path.exists(full_path):
                print(f"File {filename} does not exist.")

            new_full_path = full_path + new_ext

            os.rename(full_path, new_full_path)
            print(f"File renamed to: {new_full_path}")

        except Exception as e:
            print(f"Error occurred while downloading video: {e}")

    def playlist_download(url, save_path):
        try:
            p = Playlist(url)
            for video_url in p.video_urls:
                print(f"Downloading video: {video_url}")
                YoutubeDownloader.single_video_download(video_url, save_path)

            print("All videos has been downloaded successfully")
        except Exception as e:
            print(f"Error occurred while downloading playlist: {e}")

    def video_as_audio_download(url, save_path):
        try:
            yt = YouTube(url)
            print(f"Downloading audio from : {yt.title}")

            stream_audio = yt.streams.filter(only_audio=True).first()
            if not stream_audio:
                print(f"No audio stream found")
                return

            # Download the audio stream
            output_file = stream_audio.download(output_path=save_path)
            print(f"Downloaded audio: {output_file}")

            # Convert the audio stream to MP3 format
            new_file = os.path.splitext(output_file)[0] + ".mp3"
            print(f"Converting file to MP3.....")
            audioClip = AudioFileClip(output_file)
            audioClip.write_audiofile(new_file, codec="mp3")
            audioClip.close()

            # Remove the original download
            os.remove(output_file)
            print(f"Conversion complete. Saved as: {new_file}")

        except Exception as e:
            print(f"Error occurred while downloading audio: {e}")

    def playlist_as_mp3_download(url, save_path):
        try:
            p = Playlist(url)
            for video_url in p.video_urls:
                print(f"Downloading audio: {video_url}")
                YoutubeDownloader.video_as_audio_download(video_url, save_path)
            print(f"All videos have been downloaded and converted to MP3....")

        except Exception as e:
            print(f"Error occurred while downloading audio: {e}")


# a = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
# b = "D:\project\Yotube-Video-Downloader-FAST_API\output"
# YoutubeDownloader.single_video_download(a, b)

# x = "https://www.youtube.com/playlist?list=PL9bw4S5ePsEFSSvWQ2ukqHoxC4YvN4gsJ"
# y = 'D:\project\Yotube-Video-Downloader-FAST_API\output'
# YoutubeDownloader.playlist_download(x, y)

c = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
d = "D:\project\Yotube-Video-Downloader-FAST_API\output"

YoutubeDownloader.video_as_audio_download(c, d)

# o = "https://www.youtube.com/playlist?list=PL9bw4S5ePsEFSSvWQ2ukqHoxC4YvN4gsJ"
# p = 'D:\project\Yotube-Video-Downloader-FAST_API\output'

# YoutubeDownloader.playlist_as_mp3_download(o, p)
