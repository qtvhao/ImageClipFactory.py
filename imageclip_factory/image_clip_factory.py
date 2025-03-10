from moviepy import vfx
from moviepy import ImageClip
from moviepy import concatenate_videoclips

class ImageClipFactory:
    """
    Factory class for creating and processing image clips.
    """

    @staticmethod
    def create_image_clip(image_path, duration):
        """
        Create an ImageClip from the given image path with the specified duration.

        :param image_path: Path to the image file.
        :param duration: Duration of the clip in seconds.
        :return: An ImageClip object.
        """
        try:
            clip: ImageClip = ImageClip(image_path).with_duration(duration)
            
            clip = clip.with_effects([vfx.EvenSize()])
            return clip
        except Exception as e:
            print(f"Error creating ImageClip: {e}")
            return None

    @staticmethod
    def create_slideshow_clip(image_paths, duration_per_image):
        """
        Create a slideshow video clip from multiple image paths.

        :param image_paths: List of image file paths.
        :param duration_per_image: Duration for each image clip in seconds.
        :return: A concatenated video clip of all images.
        """
        clips = []
        
        for path in image_paths:
            clip = ImageClipFactory.create_image_clip(path, duration_per_image)
            if clip:
                clips.append(clip)
            else:
                print(f"Skipping invalid image: {path}")
        
        if not clips:
            print("No valid image clips to create slideshow.")
            return None
        
        try:
            slideshow = concatenate_videoclips(clips, method="compose")
            return slideshow
        except Exception as e:
            print(f"Error creating slideshow clip: {e}")
            return None
