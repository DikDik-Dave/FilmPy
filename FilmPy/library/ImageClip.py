from pydoc import classname

import numpy

from FilmPy.library import Clip
class ImageClip(Clip):
    """
    An image clip is a clip comprised of a single image
    """
    def __init__(self,
                 image_path:str=None,
                 frame_data:[]=None,
                 start_time:float=0,
                 end_time=None,
                 video_fps=None):
        """
        :param image_path: Path to an image file
        :param frame_data: Image Data (e.g. a single video frame)
        :param start_time: Start of time of the clip in seconds
        :param end_time: End time of the clip in seconds
        :param video_fps:

        :raises:
            ValueError
        """
        # Make sure we have some data to work with
        if (image_path is None) and (frame_data is None):
            msg = (f"Invalid input received. "
                   f"Either {classname(self)}.image_path or {classname(self)}.frame_data must be provided.")
            raise ValueError(msg)

        if image_path and frame_data:
            msg = (f"Conflicting input received. "
                   f"Either provide {classname(self)}.image_path or {classname(self)}.frame_data, not both.")
            raise ValueError(msg)

        # We were given the image frame
        if frame_data and (image_path is None):
            self._video_frames = [frame_data]
        elif image_path and (frame_data is None):
                with open(image_path, 'r') as image_file:
                    self._video_frames = [numpy.asarray(image_file.read())]

        super().__init__(start_time=start_time, end_time=end_time, video_fps=video_fps, include_audio=False)
