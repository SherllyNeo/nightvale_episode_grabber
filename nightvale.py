from pytube import Channel,YouTube
import subprocess

class nv_downloader:
    def __init__(self):
        self.channel_url = 'https://www.youtube.com/channel/UCrvuY59InDI3iKvopKT8PEw'
        self.mp4_folder = "./mp4_folder"
        self.output_folder = "./nightvale"
    def convert_mp4_to_wav(self,input_name,output_name):
        command_turn_mp4_to_wav = f"ffmpeg -i {self.mp4_folder}/{input_name} -ab 160k -ac 2 -ar 44100 -vn {self.output_folder}/{output_name}"
        subprocess.call(command_turn_mp4_to_wav, shell=True)

    def broadcast_to_fm(self,file_name):
        command_to_broadcast_to_mp4 = f""

