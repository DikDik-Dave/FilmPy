from pydoc import classname
from PIL import Image
import numpy

from FilmPy.clips.ClipBase import ClipBase
class ImageClip(ClipBase):
    """
    An image clip is a clip comprised of a single image
    """
    def __init__(self,
                 image_path:str=None,  # A path to an image file
                 video_frames:[]=None,  # An array of video frames that comprise this Image
                 clip_start_time:float=0,
                 clip_end_time=None,
                 video_fps=None):
        """
        :param image_path: Path to an image file
        :param video_frames: Image Data (e.g. a single video frame)
        :param clip_start_time: Start of time of the clip in seconds
        :param clip_end_time: End time of the clip in seconds
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

        super().__init__(clip_frames=video_frames,  # Frames for this clip
                         clip_start_time=clip_start_time,
                         clip_end_time=clip_end_time,
                         video_fps=video_fps,
                         clip_include_audio=False,
                         clip_width=frame_width,
                         clip_height=frame_height,
                         video_frames=video_frames)


    ##################
    # Public Methods #
    ##################
    def get_video_frames(self):
        return self._video_frames
