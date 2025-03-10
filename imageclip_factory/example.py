import requests
from pathlib import Path
from moviepy import VideoClip
from .image_clip_factory import ImageClipFactory  # Assuming this is your module

# Step 1: Download the image
def download_image(url, save_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Python script)"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Image downloaded and saved as {save_path}")
        return save_path
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        return None

# Step 2: Use ImageClipFactory to create an image clip
def create_clip_from_image(image_path):
    # Assuming create_image_clip accepts a file path and duration
    image_clip = ImageClipFactory.create_image_clip(image_path, 10)
    
    if image_clip:
        print("Image clip created!")
    else:
        print("Failed to create image clip.")
    
    return image_clip

# Step 3: Save the clip into a video file
def save_clip_to_video(clip: VideoClip, output_path):
    try:
        clip.write_videofile(
            output_path,
            fps=24,
            codec='libx264',   # Common codec for MP4
            audio=False        # No audio since it's just an image
        )
        print(f"Video saved successfully as {output_path}")
    except Exception as e:
        print(f"Failed to save video: {e}")

# Main workflow
if __name__ == "__main__":
    image_url = "https://http-fotosutokku-kiban-production-80.schnworks.com/search?query=Nanotechnology&limit=10&output=image&index=4"
    output_file = Path("nanotechnology_image.jpg")
    video_output_file = Path("nanotechnology_clip.mp4")

    downloaded_image_path = download_image(image_url, output_file)
    
    if downloaded_image_path:
        clip = create_clip_from_image(downloaded_image_path)
        
        if clip:
            save_clip_to_video(clip, video_output_file)
