from yt_dlp import YoutubeDL
import ffmpeg
import os
import re

def sanitize_filename(filename):
    # Remove special characters and replace spaces with underscores
    sanitized = re.sub(r'[^\w\s-]', '', filename)
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized

def download_video(url, output_path='downloads'):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Configure yt-dlp options with sanitized filename
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(output_path, '%(title).50s.%(ext)s'),
            'restrictfilenames': True,  # Restrict filenames to ASCII characters
        }
        
        # Download the video
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # Get sanitized filename
            title = sanitize_filename(info['title'])[:50]  # Limit length to 50 chars
            video_path = os.path.join(output_path, f"{title}.{info['ext']}")
            
            # If the file exists with the sanitized name, return it
            if os.path.exists(video_path):
                return video_path
            
            # If not, try to find the actual downloaded file
            for file in os.listdir(output_path):
                if file.endswith(f".{info['ext']}"):
                    return os.path.join(output_path, file)
            
            return None
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return None

def trim_video(video_path, start_time, end_time, output_path='downloads'):
    try:
        # Generate output filename
        base_name = os.path.basename(video_path)
        sanitized_name = sanitize_filename(f"trimmed_{base_name}")
        output_filename = os.path.join(output_path, sanitized_name)
        
        print(f"Input file: {video_path}")
        print(f"Output file: {output_filename}")
        
        # Verify input file exists
        if not os.path.exists(video_path):
            raise Exception(f"Input video file not found: {video_path}")
        
        # Trim the video using ffmpeg
        stream = ffmpeg.input(video_path, ss=start_time, t=end_time-start_time)
        stream = ffmpeg.output(stream, output_filename, acodec='copy', vcodec='copy')
        ffmpeg.run(stream, overwrite_output=True)
        
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








