from logging import getLogger

from FilmPy.clips.ClipBase import ClipBase
import numpy

from FilmPy.constants import PIXEL_FORMATS


class CompositeClip(ClipBase):
    """
    CompositeClip is a clip that is created from a composition of other clips
    """
    def __init__(self, clips:list,
                 clip_background_color=None,
                 clip_end_time=None,
                 clip_height=None,
                 clip_width=None):
        """
        Instantiate a composite clip from other clips

        :param clips: A list of clips to be composited. Clips are assumed to be in the order they are to be composited.
        :param clip_background_color: Background color to use for the clip, will default to black if not provided
        :param clip_end_time:
        :param clip_height:
        :param clip_width:
        """
        """
        Instantiate a composite clip from other clips

        :param clips: list of clips to Composite. Element 0 is the base layer
        """
        logger = getLogger(__name__)

        # Ensure we have valid data type
        if not isinstance(clips, list):
            raise ValueError(f"{type(self).__name__} expects clips to be a list.")

        # Ensure we have at least two clips
        if len(clips) <= 1:
            raise ValueError(f"{type(self).__name__} expects clips to contain at least two clip objects.")


        # CompositeClip specific attributes
        self._clips = clips

        # Load clip data needed to composite the clip
        clip_data = {}
        number_frames = 0
        max_width = 0
        max_height = 0
        pixel_format_input = 'rgb24'
        for i in range(len(clips)):
            # Add the new clip to our clip data
            clip_data[i] = {'mask_frames': None, 'frames': None}

            # Load frames for the ith clip
            clip_data[i]['frames'] = self._clips[i].get_frames()

            # Load the mask for the ith clip
            clip_data[i]['mask_frames'] = self._clips[i].get_mask_frames()

            # Set the max frames for this clip
            if self._clips[i].number_frames > number_frames:
                number_frames = self._clips[i].number_frames

            max_width = self._clips[i].width if self._clips[i].width > max_width else max_width
            max_height = self._clips[i].height if self._clips[i].height > max_height else max_height
            pixel_format_input = 'rgba' if self._clips[i].pixel_format_input == 'rgba' else pixel_format_input

        # Either use the provided size for the clip or if none was provided, use the calculated dimensions
        clip_height = max_height if clip_height is None else clip_height
        clip_width = max_width if clip_width is None else clip_width

        # Get the number of components for this pixel format
        number_components = PIXEL_FORMATS[pixel_format_input]['nb_components']

        # Set the background color as needed
        if clip_background_color is None:
            clip_background_color = numpy.tile(0,number_components)

        # Generate the blank frame
        blank_frame = (numpy.tile(clip_background_color, clip_width * clip_height).
               reshape(clip_height, clip_width, number_components).astype('uint8'))

        # Composite the frames
        composited_frames = []

        for frame_index in range(number_frames):
            # We are starting a new frame, so reset the composited frame
            composited_frame = None

            # Loop through the clips and composite them for this frame
            for clip_index in range(len(clips)):
                # Get the clip frame, skip to the next clip if there is no frame for this clip
                try:
                    clip_frame = clip_data[clip_index]['frames'][frame_index]
                    clip_mask = clip_data[clip_index]['mask_frames'][frame_index]
                except IndexError:
                    continue

                # Composite this clip onto the frame
                if composited_frame is not None:
                    composited_frame = numpy.where(clip_mask, clip_frame, composited_frame)
                else:
                    composited_frame = numpy.where(clip_mask, clip_frame, blank_frame)

            # Add it to our list of frames
            composited_frames.append(composited_frame)

        # Instantiate the Clip
        super().__init__(clip_end_time=clip_end_time,
                         clip_height=clip_height,
                         clip_pixel_format_input=pixel_format_input,
                         clip_width=clip_width,
                         video_frames=composited_frames)
    ####################
    # Property Methods #
    ####################
    @property
    def clips(self) -> list:
        """
        Clips array for this composite clip
        :return:
        """
        return self._clips

    @property
    def fps(self):
        """
        Frames per second of the clip itself
        """
        # If frames per second is already set, return it
        if self._clip['fps']:
            return self._clip['fps']

        # Default it to max fps from it's clips
        max_fps = 0
        for clip in self._clips:
            if clip.fps > max_fps:
                max_fps = clip.fps

        self._clip['fps'] = max_fps

        # return frames per second
        return self._clip['fps']

    @property
    def height(self):
        """
        Height of the clip itself
        """
        # If the height has already been set, return it
        if self._clip['height']:
            return self._clip['height']

        # Default to the max height from it's clips
        max_height = 0
        for clip in self._clips:
            if clip.height > max_height:
                max_height = clip.height

        self._clip['height'] = max_height

        # Update the clip's resolution
        self._clip['resolution'] = f"{self._clip['width']}x{self._clip['height']}"

        # Return the height of the clip
        return self._clip['height']

    @property
    def width(self):
        """
        Width of the clip itself
        """

        # If the width has already been set, return it
        if self._clip['width']:
            return self._clip['width']

        # Default to the max width from its clips
        max_width = 0
        for clip in self._clips:
            if clip.width > max_width:
                max_width = clip.width

        # Update the clip's width
        self._clip['width'] = max_width

        # Update the clip's resolution
        self._clip['resolution'] = f"{self._clip['width']}x{self._clip['height']}"

        # Return the height of the clip
        return self._clip['width']

    ##################
    # Public Methods #
    ##################