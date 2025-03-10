import requests
from pathlib import Path
from tempfile import gettempdir
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
    image_clip = ImageClipFactory.create_image_clip(image_path, 5)  # Duration per image
    
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
            codec='libx264',
            audio=False
        )
        print(f"Video saved successfully as {output_path}")
    except Exception as e:
        print(f"Failed to save video: {e}")

# Main workflow
if __name__ == "__main__":
    base_url = "https://http-fotosutokku-kiban-production-80.schnworks.com/search?query=Nanotechnology&limit=10&output=image&index={index}"
    downloaded_images = []

    # Get the temporary directory
    tmp_dir = Path(gettempdir())
    print(f"Using temporary directory: {tmp_dir}")

    # Download images from index 1 to index 4
    for i in range(1, 3):
        image_url = base_url.format(index=i)
        output_file = tmp_dir / f"nanotechnology_image_{i}.jpg"
        downloaded_image_path = download_image(image_url, output_file)
        
        if downloaded_image_path:
            downloaded_images.append(str(downloaded_image_path))
    
    # Create slideshow clip from downloaded images
    if downloaded_images:
        slideshow_clip = ImageClipFactory.create_slideshow_clip(downloaded_images, duration_per_image=6, effects=[
            'center_foreground,2880,1920,300'
        ])
        
        if slideshow_clip:
            video_output_file = Path("nanotechnology_slideshow.mp4")
            save_clip_to_video(slideshow_clip, video_output_file)
        else:
            print("Failed to create slideshow clip.")
    else:
        print("No images downloaded, slideshow not created.")
