import os

from logging import getLogger, getLevelNamesMapping, INFO, StreamHandler, FileHandler, Formatter

from FilmPy.clips import ChessClip, ColorClip, CompositeClip, Clip, ImageClip, TextClip
from FilmPy.Sequence import Sequence
from FilmPy.clips.GridClip import GridClip
from FilmPy.constants import *


class Editor:
    """
    Editor class, meant to be the primary import for editing videos
    """

    ##################################
    # Object Instantiation Functions #
    ##################################
    @classmethod
    def chess_clip(cls, *args, **kwargs) -> ChessClip:
        """
        Instantiate a ChessClip object

        :param args:
        :param kwargs:
        :return:
        """
        # We have one argument, treat it as file_path
        if len(args) == 1:
            kwargs['file_path'] = args[0]

        return ChessClip(**kwargs)

    @classmethod
    def color_clip(cls,
                    *args,
                   **kwargs,
                   ) -> ColorClip:
        """
        Instantiate a ColorClip object.

        :param args: Positional arguments to be passed to ColorClip
        :param color: Keyword arguments to be passed to ColorClip

        :return ColorClip: a clip containing a single color
        """

        # Process positional arguments
        for arg in args:
            # We got a two element tuple, treat it to be the size parameter
            if isinstance(arg, (tuple,list)) and len(arg) == 2:
                kwargs.update({'size': arg})
            # We got a tuple with either 3 or 4 elements, treat it to be the color parameter
            if isinstance(arg, (tuple,list)) and len(arg) in (3,4):
                kwargs.update({'color': arg})

        return ColorClip(**kwargs)

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
    def grid_clip(cls, **kwargs) -> GridClip:
        """
        Instantiate and return a GridClip object

        :param kwargs: Keyword arguments for GridClip
        :return GridClip: GridClip object
        """
        return GridClip(**kwargs)

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
    def clip(cls, *args, **kwargs):
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

        return Clip(**kwargs)

    @classmethod
    def clips(cls, *args, **kwargs):
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
            objects.append(Clip(**kwargs))

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

    @classmethod
    def configure_logging(cls,
                          *args,
                          date_format='%Y-%m-%d %H:%M:%S',
                          file_path: str = None,
                          log_level:int=INFO,
                          stream_format:str='%(asctime)s - %(name)-25s - %(levelname)s - %(message)s',
                          file_format:str=None):
        """
        Configure the logging for the FilmPy library
        Default behavior is to stream info level and above logs but not write them to disk.
        If not called, only warning or above gets displayed to the console

        :param date_format   : How should dates be displayed
        :param file_path     : Where should the log file be written to, default is FilmPy.log in current directory
        :param file_format   : Format for the file handler, if set to None, no file handler will be added
        :param log_level     : Python logging level
        :param stream_format : Format for the stream handler, if set to None, no stream handler will be added
        """

        # We received a single integer argument, treat it as the log_level
        if (len(args) == 1) and isinstance(args[0], int):
            log_level = args[0]
        elif (len(args) == 1) and isinstance(log_level, str):
            log_level = getLevelNamesMapping()[str.upper(args[0])]

        # Get the root level logger for FilmPy
        logger = getLogger(__name__.split('.')[0])

        # Set the log level to the requested level
        logger.setLevel(log_level)

        # Attach the stream handler as needed
        if stream_format:
            stream_handler = StreamHandler()
            handler_formatter = Formatter(stream_format, datefmt=date_format)
            stream_handler.setFormatter(handler_formatter)
            logger.addHandler(stream_handler)

        # No file path was provided, set it to the default
        if not file_path:
            file_path = LOG_FILENAME

        # Attach the log handler as needed
        if file_format:
            file_handler = FileHandler(file_path)
            handler_formatter = Formatter(file_format)
            file_handler.setFormatter(handler_formatter)
            logger.addHandler(file_handler)