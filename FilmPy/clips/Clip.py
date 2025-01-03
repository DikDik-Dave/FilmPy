from logging import getLogger
from ffmpeg import FFmpeg

import json
import subprocess
from FilmPy.constants import FFMPEG_BINARY, FFPROBE_BINARY
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




    ###################
    # Private Methods #
    ###################
    @classmethod
    def _set_file_information(cls, video_path):
        """
        Set the video information about video files

        :param video_path: Path to the video

        :returns keyword_arguments: Keyword arguments that were found parsing the metadata
        """
        # Get a logger
        logger = getLogger(__name__)

        # Initialize the dictionary of values
        keyword_arguments = {}

        # Call ffprobe to get information about the file
        logger.debug(f"Retrieving data from ffprobe")
        ffprobe = FFmpeg(executable="ffprobe").input(
            video_path,
            print_format="json",  # ffprobe will output the results in JSON format
            show_streams=None,
        )

        # Build the keyword arguments dictionary
        ignore_keys = ['index', 'codec_type', 'codec_tag', 'tags']
        media = json.loads(ffprobe.execute())
        for stream in media['streams']:
            for key, value in stream.items():
                if key not in ignore_keys:
                    new_key = f"{stream['codec_type']}_{key}"
                    keyword_arguments[new_key] = value

        # Call ffmpeg to get additional information about the file
        ffmpeg_info_command = [FFMPEG_BINARY, "-hide_banner", "-i", video_path]
        logger.debug(f'Calling ffmpeg "{' '.join(ffmpeg_info_command)}"')
        completed_process = subprocess.run(ffmpeg_info_command, capture_output=True)
        for line in completed_process.stderr.splitlines()[1:]:
            if b'Duration: ' in line:
                duration, start, bit_rate = line.split(b',')

                # Process video start
                keyword_arguments['video_start'] = float(start.split(b':')[1])

                # Process video bit rate
                keyword_arguments['video_bit_rate'] = bit_rate.split(b': ')[1].decode('utf8')
            elif b'Stream #0:0(und): Video' in line:
                # Set the video_fps attribute
                value_end = line.find(b' fps')
                value_start = line[:value_end].rfind(b', ')
                keyword_arguments['video_fps'] = float(line[value_start + 2:value_end])

                # Set the video_tbr attribute
                value_end = line.find(b' tbr,')
                value_start = line[:value_end].rfind(b', ')
                keyword_arguments['video_tbr'] = float(line[value_start + 2:value_end])
            elif (b'Stream #0' in line) and (b'Audio:' in line):
                pass

        # Check that we have the video number of frames, if we have it, we are done
        if 'video_nb_frames' in keyword_arguments:
            return keyword_arguments

        # Get the number of frames for the video
        ffprobe_command = [FFPROBE_BINARY,
                           '-v', 'error',
                           '-select_streams', 'v:0',
                           '-count_frames',
                           '-show_entries',
                           'stream=nb_read_frames',
                           '-of', 'csv=p=0',
                           video_path]
        logger.debug(f'Calling ffprobe to get number frames - "{' '.join(ffprobe_command)}"')
        completed_process = subprocess.run(ffprobe_command, capture_output=True)
        keyword_arguments['video_nb_frames'] = int(completed_process.stdout)
        return keyword_arguments