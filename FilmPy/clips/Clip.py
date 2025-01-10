from FilmPy.clips.ClipBase import ClipBase


class Clip(ClipBase):
    """
    Video Clip from a file
    """
    def __init__(self,
                 file_path=None,
                 clip_size=(None,None),
                 **kwargs):
        """
        Initialize a VideoClip from either a file or via direct frame data

        :param file_path: path to the video file associated with this clip
        :param clip_start_time: When does the clip start
        :param clip_end_time: When does the clip end
        :param clip_include_audio: Should the audio be written for this clip
        """
        # Check to make sure we did not receive potentially conflicting inputs
        # if video_frames and file_path:
        #     msg = (f" {type(self).__name__} - Conflicting input received. "
        #            f"Either provide frames or video_path, not both.")
        #     raise ValueError(msg)
        # elif (not video_frames) and (not file_path):
        #     msg = (f" {type(self).__name__} - Invalid input received. "
        #            f"Either provide frames or video_path.")
        #     raise ValueError(msg)

        # If the clip is associated to a file, load information about the file
        if file_path:
            kwargs.update(self._set_file_information(file_path))

        # Initialize Clip, we will set the frame_width, frame_height, and video_fps values
        # after we have processed the metadata for this clip
        super().__init__(clip_width=clip_size[0],
                         clip_height=clip_size[1],
                         file_path=file_path,
                         **kwargs)