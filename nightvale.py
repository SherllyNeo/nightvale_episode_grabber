from pytube import YouTube
import subprocess
import feedparser
import sys
import os

class nv_downloader:
    def __init__(self):
        self.channel_id = 'UCrvuY59InDI3iKvopKT8PEw'
        self.newsfeed = feedparser.parse(f"https://www.scriptbarrel.com/xml.cgi?channel_id={self.channel_id}")
        self.mp4_folder = "./mp4_folder"
        self.output_folder = "./nightvale"
    
    
    def verify_title(self,title):
        """ worlds ugliest title verification """
        try:
            numbers = title.split("-")[0].strip()
            try:
                int(numbers)
                print(f"title {title} is in the correct format of a nightvale episode")
                return True
            except:
                return False
        except:
            return False


    def download_latest_video(self):
        """ goes through recent rss episodes and downloads the most recent 
        if it is the correct nightvale format """
        i = 1
        most_recent_video_link = self.newsfeed.entries[0]['link']
        video = YouTube(most_recent_video_link)
        
        while not self.verify_title(video.title):
            most_recent_video_link = self.newsfeed.entries[i]['link']
            video = YouTube(most_recent_video_link)
            print(f"{i} did not work, trying previous video")
            i +=1
            if i>=len(self.newsfeed.entries):
                print("no recent videos to download")
                sys.exit()
        download_title = video.title.split('-')[0].strip()
        video.streams.filter(progressive = True, 
        file_extension = "mp4").first().download(output_path = self.mp4_folder, 
        filename = f"{download_title}.mp4")
        return download_title

    def convert_mp4_to_wav(self,input_name,output_name):
        """ uses sox to convert the video to wav file only """
        os.system(f'mkdir -p {self.output_folder}')
        command_turn_mp4_to_wav = f"sox {self.mp4_folder}/{input_name}.mp4 -r 22050 -c 1 -b 16 -t wav {self.output_folder}{output_name}"
        subprocess.call(command_turn_mp4_to_wav, shell=True)

    def download_most_recent_50(self):
        for video_url in self.newsfeed.entries:
            
            yt_vid = YouTube(video_url.link)
            if self.verify_title(yt_vid.title):
                download_title = yt_vid.title.split('-')[0].strip()
                yt_vid.streams.filter(progressive = True, 
                file_extension = "mp4").first().download(output_path = self.mp4_folder, 
                filename = f"{download_title}.mp4")
                print(f"downloading {download_title}")
                self.convert_mp4_to_wav(download_title,download_title+"_wav.wav")
                os.remove(f"{self.mp4_folder}/{download_title}.mp4")
                print("converted to wav...")
            
    def main(self):
        """ main function to download a nightvale episode and convert it to audio only """
        ep = self.download_latest_video()
        self.convert_mp4_to_wav(ep,ep+"_wav.wav")
        os.remove(f"{self.mp4_folder}/{ep}.mp4")
        print("fin")


def entrypoint():
    nightvale_downloader = nv_downloader()
    nightvale_downloader.download_most_recent_50()
entrypoint()
