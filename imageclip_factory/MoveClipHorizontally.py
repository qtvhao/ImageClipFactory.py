from moviepy.Effect import Effect
from moviepy.Clip import Clip


class MoveClipHorizontally(Effect):
    """
    Effect that moves a clip horizontally from left to right (or right to left)
    over time.

    Parameters
    ----------
    w : int, optional
        Width of the final displayed window (defaults to clip.w).

    h : int, optional
        Height of the final displayed window (defaults to clip.h).

    x_speed : float
        Horizontal speed of movement. Positive values move right, negative move left.

    x_start : int
        Starting x position of the clip.

    apply_to : str or tuple, optional
        Whether to apply the effect to 'video', 'mask', or both (default is 'mask').
    """

    def __init__(self, w=None, h=None, x_speed=0, x_start=0, apply_to="mask"):
        self.w = w
        self.h = h
        self.x_speed = x_speed
        self.x_start = x_start
        self.apply_to = apply_to

    def apply(self, clip: Clip) -> Clip:
        """
        Apply the horizontal move effect to the clip.
        """
        w = self.w if self.w is not None else clip.w
        h = self.h if self.h is not None else clip.h

        x_max = clip.w - w

        def filter(get_frame, t):
            # Calculate new horizontal position over time
            x = int(max(0, min(x_max, self.x_start + (self.x_speed * t))))
            print(f"{x} {t}")
            print(f"x: {x} {x_max}")
            y = 0  # Keep y fixed at the top

            # Extract the frame window
            return get_frame(t)[y : y + h, x : x + w]

        return clip.transform(filter, apply_to=self.apply_to)
