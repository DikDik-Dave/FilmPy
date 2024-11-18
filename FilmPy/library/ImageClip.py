from pydoc import classname

import numpy

from FilmPy.library import Clip
class ImageClip(Clip):
    """
    An image clip is a clip comprised of a single image
    """
    def __init__(self,
                 image_path:str=None,  # A path to an image file
                 video_frames:[]=None, # An array of video frames that comprise this Image
                 start_time:float=0,
                 end_time=None,
                 video_fps=None):
        """
        :param image_path: Path to an image file
        :param video_frames: Image Data (e.g. a single video frame)
        :param start_time: Start of time of the clip in seconds
        :param end_time: End time of the clip in seconds
        :param video_fps:

        :raises:
            ValueError
        """
        # Make sure we have some either an image file path or the video frames themselves
        if (image_path is None) and (video_frames is None):
            msg = (f"Invalid input received. "
                   f"{classname(self)}: Either image_path or video_frames must be provided.")
            raise ValueError(msg)

        # Make sure we do not have potentially conflicting image data
        if image_path and video_frames:
            msg = (f"Conflicting input received. "
                   f"Either provide {classname(self)}.image_path or {classname(self)}.frame_data, not both.")
            raise ValueError(msg)

        # We were given the image frame
        if video_frames and (image_path is None):
            self._video_frames = [video_frames]

        # We were given a path to an image file
        elif image_path and (video_frames is None):
            with open(image_path, 'rb') as image_file:
                self._video_frames = [numpy.asarray(image_file.read())]

        super().__init__(start_time=start_time, end_time=end_time, video_fps=video_fps, include_audio=False)
