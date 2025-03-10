import logging
from moviepy import vfx
from moviepy import ImageClip, VideoClip
from moviepy import concatenate_videoclips
from moviepy import CompositeVideoClip
from .MoveClipHorizontally import MoveClipHorizontally
from .GaussianBlur import GaussianBlur

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ImageClipFactory:
    """
    Factory class for creating and processing image clips.
    """

    @staticmethod
    def create_image_clip(image_path, duration, effects=None):
        """
        Create an ImageClip from the given image path with the specified duration.
        Optionally apply a list of effects.
        """
        logger.debug(f"Creating image clip for path: {image_path}, duration: {duration}, effects: {effects}")
        
        clip: ImageClip = ImageClip(image_path).with_duration(duration)

        if effects:
            logger.debug(f"Applying effects: {effects}")
            for effect in effects:
                parts = effect.split(',')
                effect_name = parts[0].strip()
                effect_params = parts[1:] if len(parts) > 1 else []

                logger.debug(f"Processing effect: {effect_name}, params: {effect_params}")

                if effect_name == 'even_size':
                    logger.info("Applying even_size effect")
                    clip = clip.with_effects([vfx.EvenSize()])
                
                elif effect_name == 'resize':
                    if effect_params:
                        try:
                            scale = float(effect_params[0])
                            logger.info(f"Resizing clip by scale: {scale}")
                            clip: VideoClip = clip.resize(scale)
                        except ValueError:
                            logger.warning(f"Invalid resize parameter for effect '{effect}'")
                    else:
                        logger.warning(f"Missing resize parameter for effect '{effect}'")

                elif effect_name == 'center_foreground':
                    if len(effect_params) >= 2:
                        try:
                            expected_width = int(effect_params[0])
                            expected_height = int(effect_params[1])

                            logger.info(f"Centering foreground on background with width: {expected_width}, height: {expected_height}")

                            clip = ImageClipFactory.create_centered_foreground_on_background(
                                clip.with_effects([
                                    GaussianBlur(55),
                                    MoveClipHorizontally(clip.w - 300, clip.h, 300 / duration, 0),
                                ]),
                                clip,
                                expected_width,
                                expected_height
                            )

                        except ValueError:
                            logger.warning(f"Invalid width/height parameters for effect '{effect}'")
                    else:
                        logger.warning(f"Missing parameters for effect '{effect}' (requires 2 params: width, height)")

                else:
                    logger.warning(f"Unknown effect: {effect_name}")

        return clip

    @staticmethod
    def create_slideshow_clip(image_paths, duration_per_image, effects=None):
        """
        Create a slideshow video clip from multiple image paths.
        """
        logger.debug(f"Creating slideshow clip. Image paths: {image_paths}, duration per image: {duration_per_image}, effects: {effects}")
        clips = []
        
        for path in image_paths:
            logger.debug(f"Creating clip for image: {path}")
            clip = ImageClipFactory.create_image_clip(path, duration_per_image, effects)
            if clip:
                logger.info(f"Adding clip for image: {path}")
                clips.append(clip)
            else:
                logger.warning(f"Skipping invalid image: {path}")
        
        if not clips:
            logger.error("No valid image clips to create slideshow.")
            return None
        
        try:
            logger.info("Concatenating clips into slideshow.")
            slideshow = concatenate_videoclips(clips, method="compose", bg_color=(255, 255, 255))
            return slideshow
        except Exception as e:
            logger.exception(f"Error creating slideshow clip: {e}")
            return None

    @staticmethod
    def resize_clip(clip: VideoClip, target_width, target_height):
        """
        Resize a clip if its dimensions are greater than or less than
        the specified target width or height, maintaining aspect ratio.
        """
        width, height = clip.size
        logger.debug(f"Resizing clip if necessary. Current size: ({width}, {height}), target size: ({target_width}, {target_height})")

        # Calculate scale factors for width and height
        width_scale = target_width / width
        height_scale = target_height / height

        # Choose the smaller scale factor to maintain aspect ratio
        scale_factor = min(width_scale, height_scale)

        # Only resize if scale_factor is not 1 (different size)
        if scale_factor != 1:
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            logger.info(f"Resizing clip from ({width}, {height}) to ({new_width}, {new_height})")

            resized_clip = clip.resized(new_size=(new_width, new_height))
            logger.debug(f"Clip resized to: {resized_clip.size}")
            return resized_clip
        else:
            logger.debug("No resizing needed for clip.")
        
        return clip

    @staticmethod
    def create_centered_foreground_on_background(background_clip: VideoClip, foreground_clip: VideoClip, expected_width, expected_height):
        """
        Overlay a foreground video centered on a background video.
        """
        logger.debug(f"Creating centered foreground on background. Expected size: ({expected_width}, {expected_height})")
        background_clip = ImageClipFactory.resize_clip(background_clip, expected_width, expected_height)

        logger.info("Positioning foreground at center of background.")
        positioned_foreground: VideoClip = foreground_clip.with_position(("center", "center"))

        logger.info("Creating composite video clip.")
        final_clip = CompositeVideoClip([background_clip, positioned_foreground])

        return final_clip
