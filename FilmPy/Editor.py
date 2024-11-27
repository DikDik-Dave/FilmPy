import os

from FilmPy.library import *
from FilmPy.library.CompositeClip import CompositeClip
from FilmPy.library.constants import *

class Editor:
    """
    Editor class, meant to be the primary import for editing videos
    """

    ##################################
    # Object Instantiation Functions #
    ##################################
    @classmethod
    def color_clip(cls,
                   color:tuple,
                   frame_width:int,
                   frame_height:int,
                   end_time:float,
                   video_fps:float
                   ) -> ColorClip:
        """
        Instantiate a ColorClip object

        :param video_fps:
        :param color: RGB tuple of the color to be displayed
        :param frame_width: Frame Width
        :param frame_height: Frame Height
        :param end_time: End time in seconds of the clip
        :return:
        """
        return ColorClip(color,frame_width, frame_height, video_fps, end_time)

    @classmethod
    def composite_clip(cls, *args, **kwargs):
        """
        Instantiate a CompositeClip

        :param args: Arguments to pass to Composite Clip, See CompositeClip for the exact arguments
        :param kwargs: Keyword arguments to pass to Composite Clip, See CompositeClip for the exact arguments

        :return CompositeClip: Instantiated composite clip
        """
        return CompositeClip(*args, **kwargs)

    @classmethod
    def image_clip(cls, **kwargs) -> ImageClip:
        """
        Instantiates a clip from an image (via data or path to file)

        :param kwargs: Keyword arguments that will be passed to ImageClip.

        :return:
        """
        return ImageClip(**kwargs)

    @classmethod
    def sequence(cls) -> Sequence:
        """
        Instantiate a Sequence object
        :return:  Sequence
        """
        return Sequence()

    @classmethod
    def text_clip(cls, *args, **kwargs):
        """
        Instantiate a clip from a piece of text
        :param args:
        :param kwargs:
        :return:
        """
        return TextClip(*args, **kwargs)

    @classmethod
    def video_clip(cls, *args, **kwargs):
        """
        Instantiate a VideoClip object
        Can be instantiated via the following inputs
        video_clip(filename) --> {video_path = filename }
        video_clip(video_path=XXX, arg2=YYY) --> {video_path = XXX, arg2 = YYY}

        :return: VideoClip
        """
        # Were a given a single argument, treat it as the video_path
        if len(args) == 1:
            kwargs.update({'file_path':args[0]})

        return VideoClip(**kwargs)

    @classmethod
    def video_clips(cls, *args, **kwargs):
        """
        Instantiate multiple video clips, useful when you need multiple versions of the same clip
        :param args:
        :param kwargs:
        :return:
        """

        # Ensure we have 'count' as a keyword argument
        if 'count' not in kwargs:
            raise KeyError(f'{type(cls).__name__}.video_clips expects count as a keyword argument.')

        # Get the count, and remove it as a keyword argument
        count = int(kwargs['count'])
        del kwargs['count']

        # Get the requested number of video clips
        objects = []

        for _ in range(count):
            objects.append(VideoClip(**kwargs))

        return objects

    ##################
    # Public Methods #
    ##################
    @classmethod
    def get_installed_fonts(cls) -> dict:
        """
        Windows specific function for getting fonts.
        :return font_map: Dictionary of fonts installed
        """
        font_map = {}
        font_directory = 'C:\\Windows\\Fonts'
        for file in os.listdir(font_directory):
            # Get the name and extension
            parts = file.split('.')
            name = parts[0]
            extension = parts[-1]

            # If it is a font file, add it to the list
            if extension in FONT_EXTENSIONS:
                font_map[name] = f"{font_directory}\\{file}"

        # Return the font map
        return font_map

    @classmethod
    def concatenate(cls, clips) -> Sequence:
        """
        Concatenate the clips into a single sequence

        :param clips:
        :return: Sequence - The clips combined into a single sequence
        """
        return Sequence(clips)