from FilmPy.clips.ClipBase import ClipBase
import numpy

class CompositeClip(ClipBase):
    """
    CompositeClip is a clip that is created from a composition of other clips
    """
    def __init__(self, clips:list,
                 clip_background_color=(0,0,0),
                 clip_end_time=None,
                 clip_height=None,
                 clip_width=None):
        """
        Instantiate a composite clip from other clips

        :param clips: list of clips to Composite. Element 0 is the base layer
        """
        # Ensure we have valid data type
        if not isinstance(clips, list):
            raise ValueError(f"{type(self).__name__} expects clips to be a list.")

        # Ensure we have at least two clips
        if len(clips) <= 1:
            raise ValueError(f"{type(self).__name__} expects clips to contain at least two clip objects.")

        # Instantiate the Clip
        super().__init__(clip_end_time=clip_end_time, clip_height=clip_height, clip_width=clip_width)

        # CompositeClip specific attributes
        self._clips = clips

        # Load clip data needed to composite the clip
        clip_data = {}
        max_frames = 0
        for i in range(len(clips)):
            # Add the new clip to our clip data
            clip_data[i] = {'mask_frames': None, 'frames': None}

            # Load frames for the ith clip
            clip_data[i]['frames'] = self._clips[i].get_frames()

            # Load the mask for the ith clip
            clip_data[i]['mask_frames'] = self._clips[i].get_mask_frames()

            # Set the max frames for this clip
            if self._clips[i].number_frames > max_frames:
                max_frames = self._clips[i].number_frames

        # Composite the frames
        composited_frames = []
        blank_frame = (numpy.tile(clip_background_color, self.width * self.height).
                       reshape(self.height, self.width, 3).astype('uint8'))
        for frame_index in range(max_frames):
            # We are starting a new frame, so reset the composited frame
            composited_frame = None

            # Loop through the clips and composite this frame
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

            # Add it to our list of fames
            composited_frames.append(composited_frame)

        self.set_frames(composited_frames)

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
        if self._clip_info['fps']:
            return self._clip_info['fps']

        # Default it to max fps from it's clips
        max_fps = 0
        for clip in self._clips:
            if clip.fps > max_fps:
                max_fps = clip.fps

        self._clip_info['fps'] = max_fps

        # return frames per second
        return self._clip_info['fps']

    @property
    def height(self):
        """
        Height of the clip itself
        """
        # If the height has already been set, return it
        if self._clip_info['height']:
            return self._clip_info['height']

        # Default to the max height from it's clips
        max_height = 0
        for clip in self._clips:
            if clip.height > max_height:
                max_height = clip.height

        self._clip_info['height'] = max_height

        # Update the clip's resolution
        self._clip_info['resolution'] = f"{self._clip_info['width']}x{self._clip_info['height']}"

        # Return the height of the clip
        return self._clip_info['height']

    @property
    def width(self):
        """
        Width of the clip itself
        """

        # If the width has already been set, return it
        if self._clip_info['width']:
            return self._clip_info['width']

        # Default to the max width from it's clips
        max_width = 0
        for clip in self._clips:
            if clip.width > max_width:
                max_width = clip.width

        # Update the clip's width
        self._clip_info['width'] = max_width

        # Update the clip's resolution
        self._clip_info['resolution'] = f"{self._clip_info['width']}x{self._clip_info['height']}"

        # Return the height of the clip
        return self._clip_info['width']

    ##################
    # Public Methods #
    ##################
    def get_video_frames(self):
        """
        Get the video frame data associated to this clip
        Note, This IS NOT the same as the frames that comprise the clip, and once set is not (meant to be) mutable

        :return: array of RGB frame data
        """
        raise AttributeError(f"{type(self).__name__}.get_video_frames does not exist. "
                             f"CompositeClips are not directly associated to video footage.")