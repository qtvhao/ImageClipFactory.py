from moviepy.Effect import Effect
from moviepy.Clip import Clip
import cv2

class GaussianBlur(Effect):
    """
    Effect that applies a Gaussian blur to a clip.

    Parameters
    ----------
    blur_radius : int
        The radius (sigma) of the Gaussian blur. Higher values mean more blur.
    apply_to : str or tuple
        Whether to apply the blur to 'video', 'mask', or both (tuple: ('video', 'mask')).
    """

    def __init__(self, blur_radius: int = 5, apply_to: str = "video"):
        self.blur_radius = blur_radius
        self.apply_to = apply_to

    def apply(self, clip: Clip) -> Clip:
        """Apply the Gaussian blur effect to the clip."""

        # Kernel size must be odd and greater than 1
        ksize = max(3, int(self.blur_radius) * 2 + 1)

        def blur_frame(get_frame, t):
            frame = get_frame(t)

            # Handle grayscale (mask) and color frames
            if frame.ndim == 2:  # Grayscale (mask)
                blurred = cv2.GaussianBlur(frame, (ksize, ksize), 0)
            else:  # Color (RGB or RGBA)
                blurred = cv2.GaussianBlur(frame, (ksize, ksize), 0)

            return blurred

        return clip.transform(blur_frame, apply_to=self.apply_to)
