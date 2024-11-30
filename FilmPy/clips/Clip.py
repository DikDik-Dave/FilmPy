import numpy as np
from logging import getLogger
from ffmpeg import FFmpeg

import json
import numpy
import subprocess
from FilmPy.constants import FFMPEG_BINARY, FFPROBE_BINARY, PIXEL_FORMATS
from FilmPy.clips.ClipBase import ClipBase


class Clip(ClipBase):
    """
    Video Clip from a file
    """
    def __init__(self, file_path=None,
                 clip_frames=None,
                 clip_start_time=0,
                 clip_end_time=None,
                 clip_include_audio=True):
        """
        Initialize a VideoClip from either a file or via direct frame data

        :param file_path: path to the video file associated with this clip
        :param clip_start_time: When does the clip start
        :param clip_end_time: When does the clip end
        :param clip_include_audio: Should the audio be written for this clip
        """
        # Check to make sure we did not recieve potentially conflicting inputs
        if clip_frames and file_path:
            msg = (f" {type(self).__name__} - Conflicting input received. "
                   f"Either provide frames or video_path, not both.")
            raise ValueError(msg)
        elif (not clip_frames) and (not file_path):
            msg = (f" {type(self).__name__} - Invalid input received. "
                   f"Either provide frames or video_path.")
            raise ValueError(msg)

        # Initialize Clip, we will set the frame_width, frame_height, and video_fps values
        # after we have processed the metadata for this clip
        super().__init__(clip_width=None, clip_height=None, clip_start_time=clip_start_time,
                         clip_end_time=clip_end_time, video_fps=None, clip_include_audio=clip_include_audio,
                         clip_frames=clip_frames, file_path=file_path)

        # If we the clip is associated to a file, load information about the file
        if file_path:
            self._set_file_information(file_path, clip_end_time)


    ###################
    # Private Methods #
    ###################
    def _set_file_information(self, video_path, end_time):
        """
        Set the video information about video files
        :param video_path: Path to the video
        :param end_time: End time of the clip
        """
        logger = getLogger(__name__)

        # Call ffprobe to get information about the file
        logger.debug(f"Retrieving data from ffprobe")
        ffprobe = FFmpeg(executable="ffprobe").input(
            video_path,
            print_format="json",  # ffprobe will output the results in JSON format
            show_streams=None,
        )

        self._media = json.loads(ffprobe.execute())
        self._video.update(self._media['streams'][0])

        # If we have audio, load its audio information
        if len(self._media['streams']) > 1:
            self._audio_info = self._media['streams'][1]
            self._audio_info['sample_rate'] = int(self._audio_info['sample_rate'])

        # Get the number of frames for the video
        logger.debug(f"Retrieving number_frames from ffprobe")
        ffprobe_command = [FFPROBE_BINARY,
                           '-v', 'error',
                           '-select_streams', 'v:0',
                           '-count_frames',
                           '-show_entries',
                           'stream=nb_read_frames',
                           '-of', 'csv=p=0',
                           video_path]

        completed_process = subprocess.run(ffprobe_command, capture_output=True)
        self._video['number_frames'] = int(completed_process.stdout)

        # Call ffmpeg to get additional information about the file

        ffmpeg_info_command = [FFMPEG_BINARY, "-hide_banner", "-i", video_path]
        logger.debug(f'Calling ffmpeg "{' '.join(ffmpeg_info_command)}"')
        completed_process = subprocess.run(ffmpeg_info_command, capture_output=True)
        for line in completed_process.stderr.splitlines()[1:]:
            if b'Duration: ' in line:
                duration, start, bit_rate = line.split(b',')

                # Process the duration
                hours, minutes, seconds = duration.strip(b'Duration: ').split(b':')
                self._video['duration'] = (int(hours) * 60 * 60) + (int(minutes) * 60) + float(seconds)

                # Process video start
                self.video_start = float(start.split(b':')[1])

                self.video_bit_rate = bit_rate.split(b': ')[1].decode('utf8')
            elif (b'Stream #0' in line) and (b'Video:' in line):
                # Set the video_fps attribute
                value_end = line.find(b' fps')
                value_start = line[:value_end].rfind(b', ')
                self._video['fps'] = float(line[value_start + 2:value_end])

                # Set the video_tbr attribute
                value_end = line.find(b' tbr,')
                value_start = line[:value_end].rfind(b', ')
                self._video['tbr'] = float(line[value_start + 2:value_end])
            elif (b'Stream #0' in line) and (b'Audio:' in line):
                pass

        # Set video stream attributes
        self._video['duration'] = float(self._video['duration'])
        self._video['height'] = int(self._video['height'])
        self._video['resolution'] = f"{self._video['width']}x{self._video['height']}"
        self._video['width'] = int(self._video['width'])

    ##################
    # Public Methods #
    ##################
    def get_video_frames_list(self):
        """
        Get the video frames
        :return: List of frames
        """
        logger = getLogger(__name__)

        # If we already loaded the frames, just return them
        if self._video_frames_list:
            return self._video_frames_list

        # Call ffmpeg and pipe it's output
        command = [FFMPEG_BINARY,
                   '-i', self._file_path,
                   '-f', 'image2pipe',
                   '-pix_fmt', 'rgb24',
                   '-vcodec', 'rawvideo',
                   '-']

        # Read the video data
        logger.debug(f'Calling ffmpeg \"{' '.join(command)}\"')
        completed_process = subprocess.run(command, capture_output=True)

        # Get all frames - Old approach
        frame_length = self._video['width'] * self._video['height'] * 3
        for i in range(0, len(completed_process.stdout), frame_length):
            frame = completed_process.stdout[i:i + frame_length]
            frame = numpy.fromstring(frame, dtype='uint8').reshape((self._video['height'],
                                                                    self._video['width'],
                                                                    3))

            # Store the frame in our frames list
            self._video_frames_list.append(frame)

        # Return the video frames
        return self._video_frames_list

    def get_video_frames(self) -> np.array:
        """
        Get the underlying video frames associated to this clip.

        :return np.array: Array of size (# frames * frame height) x (frame width) x (pixel format number components)
        """
        logger = getLogger(__name__)

        # If we have already loaded the frames, we can just return them
        if self._video['frames']:
            return self._video['frames']

        # Load all the frame data into a single ndarray
        number_components = PIXEL_FORMATS[self.processing_pixel_format]['nb_components']
        ffmpeg_command = [FFMPEG_BINARY,
                        '-i', self._file_path,
                        '-f', 'image2pipe',
                        '-pix_fmt', self.processing_pixel_format,
                        '-vcodec', 'rawvideo',
                        '-']

        # Read the video data
        logger.debug(f'Calling ffmpeg \"{' '.join(ffmpeg_command)}\"')
        completed_process = subprocess.run(ffmpeg_command, capture_output=True)

        height = self.video_number_frames * self.video_height
        self._video['frames'] = (numpy.fromstring(completed_process.stdout, dtype='uint8')
                                 .reshape(height, self.video_width, number_components))

        # return the video frames
        return self._video['frames']