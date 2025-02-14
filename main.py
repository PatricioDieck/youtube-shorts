from pytube import YouTube
from moviepy.editor import VideoFileClip
import os

def download_video(url, output_path='downloads'):
    try:
        # Create downloads directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Download the video
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video_path = video.download(output_path)
        return video_path
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return None

def trim_video(video_path, start_time, end_time, output_path='downloads'):
    try:
        # Load the video
        video = VideoFileClip(video_path)
        
        # Trim the video
        trimmed_video = video.subclip(start_time, end_time)
        
        # Generate output filename
        output_filename = os.path.join(output_path, f"trimmed_{os.path.basename(video_path)}")
        
        # Save the trimmed video
        trimmed_video.write_videofile(output_filename)
        
        # Close the video files
        video.close()
        trimmed_video.close()
        
        return output_filename
    except Exception as e:
        print(f"Error trimming video: {str(e)}")
        return None

def main():
    # Get user input
    url = input("Enter YouTube URL: ")
    start_time = float(input("Enter start time (in seconds): "))
    end_time = float(input("Enter end time (in seconds): "))

    # Download the video
    video_path = download_video(url)
    if video_path:
        print(f"Video downloaded successfully to: {video_path}")
        
        # Trim the video
        trimmed_path = trim_video(video_path, start_time, end_time)
        if trimmed_path:
            print(f"Trimmed video saved to: {trimmed_path}")
        else:
            print("Failed to trim video")
    else:
        print("Failed to download video")

if __name__ == "__main__":
    main()

# download youtube video from url








