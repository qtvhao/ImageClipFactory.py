from moviepy import AudioFileClip
from moviepy import CompositeAudioClip
from moviepy import vfx
from moviepy import ImageClip

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
            clip = ImageClip(image_path).with_duration(duration)
            return clip
        except Exception as e:
            print(f"Error creating ImageClip: {e}")
            return None
