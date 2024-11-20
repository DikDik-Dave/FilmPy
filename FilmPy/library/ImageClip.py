from pydoc import classname
from PIL import Image
from PIL.ExifTags import TAGS
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

        # Set local variables
        frame_width = None
        frame_height = None

        # We were given a path to an image file
        if image_path and (video_frames is None):
            # Open the image file with PIL
            img = Image.open(image_path)
            frame_width = img.size[0]
            frame_height = img.size[1]
            video_frames = [numpy.array(img)]

            # TODO: Test & store exif data

            # exifdata = img.getexif()
            # print(exifdata)
            # # iterating over all EXIF data fields
            # for tag_id in exifdata:
            #     # get the tag name, instead of human unreadable tag id
            #     tag = TAGS.get(tag_id, tag_id)
            #     data = exifdata.get(tag_id).decode("utf-16")
            #     print(f"{tag:25}: {data}")

        super().__init__(frames=video_frames,       # Frames for this clip
                         start_time=start_time,
                         end_time=end_time,
                         video_fps=video_fps,
                         include_audio=False,
                         frame_width=frame_width,
                         frame_height=frame_height,
                         video_frames=video_frames)


    ##################
    # Public Methods #
    ##################
    def get_clip_frames(self):
        # Return the already created frames
        if self._clip_frames:
            return self._clip_frames

        # No frames yet exist, copy the video data
        # TODO: respect clip start, end, etc
        self._clip_frames = self.get_video_frames()

        return self._clip_frames

    def get_video_frames(self):
        return self._video_frames
