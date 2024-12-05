from FilmPy.clips.ImageClip import ImageClip
from FilmPy.constants import DEFAULT_FRAME_RATE
import numpy

class ColorClip(ImageClip):
    def __init__(self,
                 size:tuple=None,
                 end_time:int=None,
                 fps:int=DEFAULT_FRAME_RATE,
                 color=(57, 255, 20),
                 **kwargs):
        """
        Clip containing a single color

        :param size: (width, height) of the clip
        :param color: Color to make the clip, defaults to a neon green
        :param kwargs: Keyword arguments to pass on to ImageClip & BaseClip

        :raises ValueError: When size is not a tuple or list
        :raises ValueError: When end_time is not a number
        """
        # Ensure size is a list or a tuple
        if not isinstance(size, (tuple, list) or (len(size) != 2)):
            raise ValueError(f"{type(self).__name__}(size=) must be an a tuple or a list of (width, height)")

        # Ensure end_time is a number
        if not isinstance(end_time, (int, float)):
            raise ValueError(f'{type(self).__name__}(end_time=) must be a number')

        # Create the necessary frames
        video_frames = []
        frame = numpy.tile(color, size[0] * size[1]).reshape(size[1], size[0], 3).astype('uint8')
        for x in range(int(fps * end_time)):
            video_frames.append(frame)

        # Instantiate ImageClip
        super().__init__(video_frames=video_frames,
                         clip_end_time=end_time,
                         clip_width=size[0],
                         clip_height=size[1],
                         clip_fps=fps,
                         **kwargs)