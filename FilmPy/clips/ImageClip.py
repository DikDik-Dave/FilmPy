from pydoc import classname
from PIL import Image
import numpy

from .Clip import Clip

class ImageClip(Clip):
    """
    An image clip is a clip comprised of a single image
    """
    def __init__(self,
                 image_path:str=None,  # A path to an image file
                 clip_end_time=None,
                 clip_height=None,
                 clip_start_time: float = 0,
                 clip_pixel_format='rgb24',
                 clip_width=None,
                 video_fps=None,
                 video_frames=None,  # An array of video frames that comprise this Image
                 **kwargs):
        """
        Instantiate an ImageClip

        :param image_path: Optional path to an image file
        :param clip_end_time: Optional end time for the clip
        :param clip_height: Height of the clip. If image_path was provided, it will be retrieved from the image
        :param clip_start_time:
        :param clip_width: Width of the clip. If image_path was provided, it will be retrieved from the image.
        :param video_fps:
        :param video_frames:
        :param kwargs:

        :raises ValueError: When image_path and video_frames are both None
        :raises ValueError: When video_frames and image_path are both specified (potentially conflicting data)
        :raises ValueError: When video_frames is not None, but is not a list as expected
        """

        # Make sure we have some either an image file path or the video frames themselves
        if (image_path is None) and (video_frames is None):
            msg = (f"Invalid input received. "
                   f"{classname(self)}: Either image_path or video_frames must be provided.")
            raise ValueError(msg)

        # Make sure we do not have potentially conflicting image data
        if image_path and video_frames:
            msg = (f"Conflicting input parameters to {type(self).__name__}. "
                   f"Either provide image_path or video_frames, not both.")
            raise ValueError(msg)

        # Video frames must be a list of ndarray objects
        if (video_frames is not None) and (not isinstance(video_frames, list)):
            msg = f"video_frames parameter is expected to be a list, not {type(video_frames)}"
            raise ValueError(msg)

        # We were given a path to an image file
        if image_path and (video_frames is None):
            # Open the image file with PIL
            img = Image.open(image_path)
            clip_width = img.size[0]
            clip_height = img.size[1]
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


        # Instantiate ClipBase
        super().__init__(video_frames=video_frames,  # Frames for this clip
                         clip_start_time=clip_start_time,
                         clip_end_time=clip_end_time,
                         video_fps=video_fps,
                         clip_include_audio=False,
                         clip_width=clip_width,
                         clip_height=clip_height,
                         clip_pixel_format=clip_pixel_format,
                         **kwargs)