from FilmPy.clips.ImageClip import ImageClip
import numpy

class ColorClip(ImageClip):
    def __init__(self,
                 size:tuple,
                 color=(57,255,20),
                 **kwargs):
        """
        Clip containing a single color

        :param size: (width, height) of the clip
        :param color: Color to make the clip, defaults to a neon green
        :param kwargs: Keyword arguments to pass on to ImageClip & BaseClip

        :raises ValueError: When size is not a tuple or list
        """
        # Ensure size is a list or a tuple
        if not isinstance(size, (tuple, list)):
            raise ValueError(f"size parameter must be an a tuple or a list")

        # Create a frame of the appropriate size
        frame = numpy.tile(color, size[0] * size[1]).reshape(size[1], size[0], 3).astype('uint8')

        # Instantiate ImageClip
        super().__init__(video_frames=[frame],
                         clip_width=size[0],
                         clip_height=size[1],
                         **kwargs)