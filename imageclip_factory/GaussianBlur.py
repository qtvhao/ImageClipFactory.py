from moviepy.Effect import Effect
from moviepy.Clip import Clip
import cv2
from typing import Union, Callable

class GaussianBlur(Effect):
    """
    Effect that applies a Gaussian blur to a clip, with optional dynamic blur radius.

    Parameters
    ----------
    blur_radius : int, float, or callable
        The radius (sigma) of the Gaussian blur. If callable, should be a function of time (t).
    apply_to : str or tuple
        Whether to apply the blur to 'video', 'mask', or both (tuple: ('video', 'mask')).
    """

    def __init__(
        self,
        blur_radius: Union[int, float, Callable[[float], float]] = 5,
        apply_to: str = "video"
    ):
        self.blur_radius = blur_radius
        self.apply_to = apply_to

    def apply(self, clip: Clip) -> Clip:
        """Apply the Gaussian blur effect to the clip."""

        def blur_frame(get_frame, t):
            # Compute the blur radius at time t (dynamic or static)
            current_radius = (
                self.blur_radius(t) if callable(self.blur_radius) else self.blur_radius
            )

            # Ensure radius is valid and compute kernel size
            current_radius = max(0, current_radius)
            ksize = max(3, int(current_radius) * 2 + 1)  # Kernel size must be odd and > 1

            # Get the frame at time t
            frame = get_frame(t)

            # Apply Gaussian blur (grayscale or color)
            if frame.ndim == 2:
                blurred = cv2.GaussianBlur(frame, (ksize, ksize), 0)
            else:
                blurred = cv2.GaussianBlur(frame, (ksize, ksize), 0)

            return blurred

        return clip.transform(blur_frame, apply_to=self.apply_to)
