import logging
import subprocess
import os
from logging import getLogger
from subprocess import DEVNULL, PIPE

import numpy
from PIL import Image

from FilmPy.constants import *
import numpy as np

class ClipBase:
    """
    Base class for all clips.
    """

    def __init__(self,
                 audio_avg_frame_rate=None,
                 audio_bits_per_sample=None,
                 audio_bit_rate=None,
                 audio_channels=None,
                 audio_channel_layout=None,
                 audio_codec_name=None,
                 audio_codec_long_name=None,
                 audio_codec_tag_string=None,
                 audio_disposition=None,
                 audio_duration=None,
                 audio_duration_ts=None,
                 audio_frames=None,
                 audio_get_frame=None,
                 audio_nb_frames=None,
                 audio_profile=None,
                 audio_r_frame_rate=None,
                 audio_sample_fmt=None,
                 audio_sample_rate=None,
                 audio_start_pts=None,
                 audio_start_time=None,
                 audio_time_base=None,
                 clip_behavior=Behavior.ENFORCE_LIMIT.value,
                 clip_end_time=None,
                 clip_fps=None,
                 clip_start_time=0,
                 clip_width=None,
                 file_path=None,
                 clip_height=None,
                 clip_include_audio=None,
                 clip_position=(0,0),
                 clip_pixel_format='rgb24',
                 mask_frames=None,
                 mask_behavior=Behavior.LOOP_FRAMES.value,
                 video_avg_frame_rate=None,
                 video_bit_rate=None,
                 video_bits_per_raw_sample=None,
                 video_chroma_location=None,
                 video_closed_captions=None,
                 video_codec_long_name=None,
                 video_codec_name=None,
                 video_codec_tag_string=None,
                 video_coded_height=None,
                 video_coded_width=None,
                 video_color_primaries=None,
                 video_color_range=None,
                 video_color_space=None,
                 video_color_transfer=None,
                 video_disposition=None,
                 video_duration=None,
                 video_duration_ts=None,
                 video_has_b_frames=None,
                 video_height=None,
                 video_is_avc=None,
                 video_end_time=None,
                 video_fps=None,
                 video_frames=None,
                 video_level=None,
                 video_nal_length_size=None,
                 video_nb_frames=None,
                 video_pix_fmt=None,
                 video_profile=None,
                 video_r_frame_rate=None,
                 video_refs=None,
                 video_start=None,
                 video_start_pts=None,
                 video_start_time=None,
                 video_time_base=None,
                 video_tbr=None,
                 video_width=None,
                 **kwargs
                 ):
        """
        Base class for all Clip classes.
        Stores all common logic / attributes of a clip.
        It is not meant to be instantiated directly.

        :param audio_avg_frame_rate:
        :param audio_bits_per_sample:
        :param audio_bit_rate:
        :param audio_channels:
        :param audio_channel_layout:
        :param audio_codec_name:
        :param audio_codec_long_name:
        :param audio_codec_tag_string:
        :param audio_disposition:
        :param audio_duration:
        :param audio_duration_ts:
        :param audio_frames:
        :param audio_nb_frames:
        :param audio_r_frame_rate:
        :param audio_sample_fmt:
        :param audio_sample_rate:
        :param audio_start_pts:
        :param audio_start_time:
        :param audio_time_base:
        :param clip_behavior: How should we behave when the end time exceeds the clip frames we have.
        :param clip_end_time:
        :param clip_fps:
        :param clip_start_time:
        :param clip_width:
        :param file_path:
        :param clip_height:
        :param clip_include_audio:
        :param clip_position:
        :param clip_pixel_format:
        :param mask_frames:
        :param mask_behavior:
        :param video_avg_frame_rate:
        :param video_bit_rate:
        :param video_bits_per_raw_sample:
        :param video_chroma_location:
        :param video_closed_captions:
        :param video_codec_long_name:
        :param video_codec_name:
        :param video_codec_tag_string:
        :param video_coded_height:
        :param video_coded_width:
        :param video_disposition:
        :param video_duration:
        :param video_duration_ts:
        :param video_has_b_frames:
        :param video_height:
        :param video_is_avc:
        :param video_end_time:
        :param video_fps:
        :param video_frames:
        :param video_level:
        :param video_nal_length_size:
        :param video_nb_frames:
        :param video_number_frames:
        :param video_pix_fmt:
        :param video_profile:
        :param video_r_frame_rate:
        :param video_refs:
        :param video_start:
        :param video_start_pts:
        :param video_start_time:
        :param video_time_base:
        :param video_tbr:
        :param video_width:
        :param kwargs: Catchall for unexpected keyword arguments

        :raises ValueError: When invalid clip_pixel_format received
        """
        # Get a logger
        logger = getLogger(__name__)
        self._all_attributes = ('_audio','_clip','_environment','_mask','_file')

        # Environment Attributes / Check for .filmpy.env :
        # TODO: check for FILMPY_* environment variables
        self._environment = {}
        if os.path.exists(ENVIRONMENT_FILE):
            with open(ENVIRONMENT_FILE) as f:
                for line in f.readlines():
                    key, val = line.split('=')
                    self._environment[key] = val

        # Warn the user they sent an argument we are not expecting
        for kw_arg, kw_value in kwargs.items():
            logger.warning(f'{type(self).__name__}({kw_arg}={kw_value} ...) is an unknown argument')

        # Ensure the clip pixel format is valid
        if clip_pixel_format not in PIXEL_FORMATS.keys():
            raise ValueError(f"'{clip_pixel_format}' is not a valid value for clip_pixel_format.")

        audio_frames_initialized = True if audio_frames else False
        # Audio Specific Attributes
        self._audio = { 'average_frame_rate': audio_avg_frame_rate,
                        'bits_per_sample': audio_bits_per_sample,
                        'bit_rate': audio_bit_rate,
                        'codec_name': audio_codec_name,
                        'codec_long_name': audio_codec_long_name,
                        'codec_tag_string': audio_codec_tag_string,
                        'channel_layout': audio_channel_layout,
                        'channels': audio_channels,
                        'disposition': audio_disposition,
                        'duration': audio_duration,
                        'duration_ts': audio_duration_ts,
                        'get_frame': audio_get_frame,
                        'frames': audio_frames,
                        'frames_initialized': audio_frames_initialized,
                        'number_frames': audio_nb_frames,
                        'profile': audio_profile,
                        'r_frame_rate': audio_r_frame_rate,
                        'sample_format': audio_sample_fmt,
                        'start_pts': audio_start_pts,
                        'start_time': audio_start_time,
                        'time_base': audio_time_base,
                        }
        if audio_sample_rate:
            self.audio_sample_rate = audio_sample_rate

        # Clip specific attributes
        self._clip = {
                           'behavior': clip_behavior,
                           'end_time': clip_end_time,                     # End time of the clip itself
                           'fps': clip_fps,                               # Frames per second for the clip
                           'height': clip_height,                         # Height (in pixels) of the clip
                           'include_audio': clip_include_audio,           # Should the audio be included when rendered
                           'pixel_format': clip_pixel_format,             # Pixel format to use while video processing
                           'number_frames': None,                         # Number of video frames in the clip
                           'position_x': int(clip_position[0]),           # x coordinate for the clip
                           'position_y': int(clip_position[1]),           # y coordinate for the clip
                           'start_time': clip_start_time,                 # Start time in seconds
                           'width': clip_width,                           # Width (in pixels) of the clip
                      }

        # Video specific attributes
        video_frames, video_frames_initialized = ([],False) if not video_frames else (video_frames,True)
        self._video = {     'average_frame_rate': video_avg_frame_rate,
                            'bit_rate': video_bit_rate,
                            'bits_per_raw_sample': video_bits_per_raw_sample,
                            'chroma_location': video_chroma_location,
                            'closed_captions': video_closed_captions,
                            'codec_long_name': video_codec_long_name,
                            'codec_name': video_codec_name,
                            'codec_tag_string': video_codec_tag_string,
                            'coded_height': video_coded_height,
                            'coded_width': video_coded_width,
                            'color_primaries': video_color_primaries,
                            'color_range': video_color_range,
                            'color_space': video_color_space,
                            'color_transfer': video_color_transfer,
                            'disposition': video_disposition,
                            'duration': video_duration,
                            'duration_ts': video_duration_ts,
                            'end_time': video_end_time,                      # Duration of the video
                            'fps': video_fps,                                # FPS for the underlying video
                            'frames': video_frames,                          # Frames for the underlying video
                            'frames_initialized':  video_frames_initialized, # Do we have the frames already?
                            'has_b_frames': video_has_b_frames,
                            'is_avc': video_is_avc,
                            'height': video_height,
                            'level': video_level,
                            'nal_length_size': video_nal_length_size,
                            'pixel_format': video_pix_fmt,
                            'profile': video_profile,
                            'refs': video_refs,
                            'r_frame_rate': video_r_frame_rate,
                            'start': video_start,
                            'start_pts': video_start_pts,
                            'start_time': video_start_time,
                            'time_base': video_time_base,
                            'tbr': video_tbr,
                            'width': video_width}
        self.video_number_frames = video_nb_frames
        # File specific attributes
        self._file_path = file_path  # Path to whatever file is associated to this clip

        # Mask specific attributes
        self._mask = {'frames':mask_frames,
                      'behavior': mask_behavior,
                      'initialized': False}
        if isinstance(self._mask['behavior'], Enum):
            self._mask['behavior'] = self._mask['behavior'].value

        ###########################################
        # Post array initialization, logic checks #
        ###########################################
        if (self.end_time > self.video_end_time) and (self.behavior == Behavior.ENFORCE_LIMIT.value):
            raise ValueError(f"{type(self).__name__} end time {self.end_time} "
                             f"exceeds video length of {self.video_end_time}. "
                             f"Change clip_behavior parameter to allowing for looping or padding of the video")


    ############################
    # Property Methods - Audio #
    ############################
    @property
    def audio_channels(self):
        """
        Number of audio channels for the audio
        :return:
        """
        return self._audio['channels']

    @audio_channels.setter
    def audio_channels(self, value):
        """
        set the number of audio channels
        :param value:
        :return:
        """
        self._audio['channels'] = int(value)

    @property
    def audio_number_frames(self):
        """
        Number of audio frames in this clip
        """
        return self._audio['number_frames']

    @audio_number_frames.setter
    def audio_number_frames(self, value):
        """
        Set the number of audio frames in this clip
        """
        self._audio['number_frames'] = int(value)

    @property
    def audio_profile(self):
        return self._audio['profile']

    @property
    def audio_sample_rate(self) -> int:
        """
        Audio Sample Rate for the audio
        :return:
        """

        # If we already have audio sample rate, just return it
        if 'sample_rate' in self._audio:
            return self._audio['sample_rate']

        # Audio Sample Rate was not set, fall back to the default sample rate
        self.audio_sample_rate = DEFAULT_SAMPLE_RATE

        return self._audio['sample_rate']


    @audio_sample_rate.setter
    def audio_sample_rate(self, value):
        """
        Set the audio sample rate
        :param value: audio sample rate value
        """
        try:
            value = int(value) if value else value
        except TypeError:
            logger = getLogger(__name__)
            logger.warning(f"{type(self).__name__}.audio_sample_rate='{value}' is invalid. "
                           f"{type(self).__name__}.audio_sample_rate has not been modified.")

        self._audio['sample_rate'] = value

    @property
    def audio_end_index(self) -> int:
        """
        Audio data index corresponding to the start_time of the clip
        """
        return int(self.audio_sample_rate * self.end_time)

    @property
    def audio_start_index(self) -> int:
        """
        Audio data index corresponding to the end_time of the clip
        """
        return int(self.audio_sample_rate * self.start_time)

    ###########################
    # Property Methods - Clip #
    ###########################
    @property
    def ffmpeg_binary(self):
        """
        Path to the ffmpeg binary to use
        """
        if 'FFMPEG_BINARY' in self._environment:
            return self._environment['FFMPEG_BINARY']

        return FFMPEG_BINARY

    @property
    def ffprobe_binary(self):
        """
        Path to the ffprobe binary to use
        """
        if 'FFPROBE_BINARY' in self._environment:
            return self._environment['FFPROBE_BINARY']

        return FFPROBE_BINARY

    @property
    def ffplay_binary(self):
        """
        Path to the ffprobe binary to use
        """
        if 'FFPLAY_BINARY' in self._environment:
            return self._environment['FFPLAY_BINARY']

        return FFPLAY_BINARY

    @property
    def default_frame_rate(self):
        """
        Default Frame Rate value for clips
        """
        if 'DEFAULT_FRAME_RATE' in self._environment:
            return self._environment['DEFAULT_FRAME_RATE']

        return DEFAULT_FRAME_RATE

    @property
    def behavior(self) -> int:
        """
        Governs how the clip should behave when given an end time that is out of bounds
        """
        if isinstance(self._clip['behavior'], Behavior):
            self.behavior = self._clip['behavior'].value

        return int(self._clip['behavior'])

    @behavior.setter
    def behavior(self, value):
        """
        Set the behavior attribute
        :param value:
        """
        self._clip['behavior'] = int(value)

    @property
    def duration(self) -> int:
        """
        Duration of the clip
        """
        return self.end_time - self.start_time

    @property
    def end_frame(self) -> int:
        """
        Frame index corresponding the end time of the clip
        """
        return int(self.end_time * self.fps)

    @property
    def end_time(self):
        """
        End time of the clip in seconds
        """
        # If the end time for the clip has already been set, return it
        if ('end_time' in self._clip) and self._clip['end_time']:
            return self._clip['end_time']

        # Default the end_time of the clip to the video end time
        self.end_time = self.video_end_time

        # Return the end time of the clip
        return self._clip['end_time']

    @end_time.setter
    def end_time(self, value):
        """
        Set the end time for the clip

        :param value: End time of the clip in seconds
        :raises ValueError: When end time is longer than the clip AND clip behavior is set to ENFORCE_LIMIT
        """
        self._clip['end_time'] = float(value)

    @property
    def fps(self):
        """
        Frames per second of the clip itself
        """
        # If frames per second is already set, return it
        if self._clip['fps']:
            return self._clip['fps']

        # Default it to video frames per second
        self._clip['fps'] = self.video_fps

        # return frames per second
        return self._clip['fps']

    @fps.setter
    def fps(self, value):
        """
        Set frames per second for the clip itself
        :param value:
        """
        self._clip['fps'] = float(value)

    @property
    def has_audio(self):
        """
        Does the clip have audio

        :return: True if the clip has audio data, False otherwise
        """
        return bool(self.audio_number_frames and (self.audio_number_frames > 0))

    @property
    def has_video(self):
        """
        Does the clip have video frames
        """
        return bool(self.video_number_frames and (self.video_number_frames > 0))

    @property
    def height(self) -> int:
        """
        Height of the clip itself, will default to video_height if not set

        :return height: height of the clip
        """
        # If height has already been set, return it
        if ('height' in self._clip) and self._clip['height']:
            return self._clip['height']

        # Default height to the video's height
        self._clip['height'] = self.video_height

        # Return height
        return self._clip['height']

    @height.setter
    def height(self, value):
        """
        Set the height of the clip itself

        :param value: height value
        """
        self._clip['height'] = int(value)

        # Update the clip's resolution
        self._clip['resolution'] = f"{self.width}x{self.height}"

    @property
    def pixel_format(self) -> str:
        """
        Pixel format to be used when reading in this clip (if it was from disk)
        """
        return self._clip['pixel_format']

    @pixel_format.setter
    def pixel_format(self, value):
        """
        Set the pixel format input value
        """
        # Ensure we have a valid pixel format
        if value not in PIXEL_FORMATS.keys():
            raise ValueError(f"'{value}' is not a valid pixel format.")

        self._clip['pixel_format'] = value

    @property
    def number_frames(self) -> int:
        """
        Number of frames in the clip
        """
        if self._clip['number_frames']:
            return self._clip['number_frames']

        # Default to number of frames in the video
        self._clip['number_frames'] = self.video_number_frames

        # Return the number of frames
        return self._clip['number_frames']


    @number_frames.setter
    def number_frames(self, value):
        """
        Set the number of frames of the clip itself
        :param value:
        :return:
        """
        self._clip['number_frames'] = int(value)

    @property
    def position(self) -> tuple:
        """
        (x,y) coordinates for the clip (only used if the clip is composited)
        """
        return self._clip['position_x'], self._clip['position_y']

    @position.setter
    def position(self, value):
        """
        Set the (x,y) coordinates for the clip
        :param value:
        """
        self.x = value[0]
        self.y = value[1]

    @property
    def resolution(self) -> str | None:
        """
        Resolution of the clip
        :return:
        """
        # If clip resolution is already set, return it
        if 'resolution' in self._clip:
            return self._clip['resolution']

        # Set resolution to the width x height of the clip
        self._clip['resolution'] = f"{self.width}x{self.height}"

        return self._clip['resolution']

    @property
    def size(self):
        """
        Size (width,height) of the clip
        """
        return self.width, self.height

    @size.setter
    def size(self, value):
        self.width = value[0]
        self.height = value[1]

    @property
    def start_frame(self) -> int:
        """
        Get the frame index for the start of the clip
        :return:
        """
        return int(self.fps * self.start_time)

    @property
    def start_time(self) -> float:
        """
        Retrieves the start time of the clip

        :return: start time of the clip in seconds
        """
        return self._clip['start_time']

    @start_time.setter
    def start_time(self, value):
        """
        Set the start time for the clip

        :param value: Value of start time in seconds, must be able to be cast into a float
        """
        self._clip['start_time'] = float(value)

    @property
    def width(self) -> int | None:
        """
        Width of the clip itself
        :return:
        """
        # If width has already been set, return it
        if ('width' in self._clip) and self._clip['width']:
            return self._clip['width']

        # Default width if not set to the video's width
        self._clip['width'] = self.video_width

        return self._clip['width']

    @width.setter
    def width(self, value):
        """
        Set the width of the clip itself
        :param value:
        :return:
        """
        self._clip['width'] = int(value)

        # Update the clip's resolution
        self._clip['resolution'] = f"{self._clip['width']}x{self._clip['height']}"


    @property
    def x(self):
        """
        x coordinate of the clip itself
        """
        return self._clip['position_x']

    @x.setter
    def x(self, value):
        """
        Set the x coordinate
        :param value:
        """
        self._clip['position_x'] = int(value)

    @property
    def y(self):
        """
        y coordinate of the clip itself
        """
        return self._clip['position_x']

    @y.setter
    def y(self, value):
        """
        Set the y coordinate
        :param value:
        """
        self._clip['position_y'] = int(value)

    #######################################
    # Property Methods - Video Attributes #
    #######################################
    @property
    def video_height(self) -> int:
        """
        Height of the underlying video associated to this clip

        :raises ValueError: Video info has no height attribute
        """
        if 'height' not in self._video:
            raise ValueError(f'{type(self).__name__}.video_height cannot be None.')
        return self._video['height']

    @property
    def video_number_frames(self) -> int:
        """
        Number of frames in the underlying video associated to this clip

        :raises ValueError:  Number of video frames is None (which should never be true)
        """
        return self._video['number_frames']

    @video_number_frames.setter
    def video_number_frames(self, value):
        value = 0 if value is None else value
        self._video['number_frames'] = int(value)

    @property
    def video_width(self) -> int:
        """
        Width of the underlying video associated to this clip

        :raises ValueError: Video info has no width attribute
        """
        if 'width' not in self._video:
            raise ValueError(f'{type(self).__name__}.video_width cannot be None.')
        return self._video['width']

    @property
    def file_path(self):
        """
        Path to the video file

        :returns:
            None - No video file is associated with this clip
            str - Path to the video file
        """
        return self._file_path

    @property
    def video_color_primaries(self):
        """
        Color Primaries of the video
        """
        return self._video['color_primaries']

    @property
    def video_color_range(self):
        """
        Color Range of the video
        """
        return self._video['color_range']

    @property
    def video_color_transfer(self):
        """
        Color transfer of the video
        """
        return self._video['color_transfer']

    @property
    def video_duration(self) -> float:
        """
        Duration in seconds of the video
        """
        return self._video['duration']

    @property
    def video_end_time(self):
        """
        End time of the video itself
        """
        # Has end time for the video already been set, if so return it
        if self._video['end_time']:
            return self._video['end_time']

        # Default to video duration
        self.video_end_time = self.video_duration

        # Return the video duration
        return self._video['end_time']

    @video_end_time.setter
    def video_end_time(self, value):
        """
        Set the video_end_time attribute
        """
        self._video['end_time'] = float(value)

    @property
    def video_fps(self):
        """
        Frames per second of the associated video
        :returns:
            int - Frames per second for the video
        """
        # If already set, just return it
        if self._video['fps']:
            return self._video['fps']

        # No video fps was set, default it to our default frame rate (30)
        self._video['fps'] = DEFAULT_FRAME_RATE

        # Return the video frames per second
        return self._video['fps']

    @video_fps.setter
    def video_fps(self, fps):
        """
        Set video_fps
        :param fps:
        :return:
        """
        if not isinstance(fps, (int,float)):
            raise TypeError(f"{type(self).__name__}.video_fps must be an integer or a float")
        self._video['fps'] = fps

    @property
    def video_resolution(self) -> str:
        if 'resolution' not in self._video:
            raise TypeError(f'{type(self).__name__}.video_resolution is None.')
        return self._video['resolution']

    @property
    def include_audio(self):
        """
        Should the audio of this clip be included
        :return:
        """
        if self._clip['include_audio'] is None:
            raise ValueError(f'{type(self).__name__}.include_audio cannot be None.')
        return self._clip['include_audio']

    ###################
    # Private Methods #
    ###################

    def _read_audio(self,
                    file_path=None,
                    audio_channels=None,
                    audio_sample_rate=None,
                    ffmpeg_log_level='error'):
        """
        Read audio from a file, via ffmpeg
        """
        logger = getLogger(__name__)
        logger.debug(f'{type(self).__name__}._read_audio(file_path=\'{file_path}\', audio_channels={audio_channels}, '
                     f'audio_sample_rate={audio_sample_rate}, ffmpeg_log_level=\'{ffmpeg_log_level}\')')
        ffmpeg_command = [self.ffmpeg_binary,
                          '-i'        , file_path,
                          '-vn'       ,
                          '-loglevel' , ffmpeg_log_level,
                          '-f'        , 's%dle' % (8 * audio_channels),
                          '-acodec'   , 'pcm_s%dle' % (8 * audio_channels),
                          '-ar'       , '%d' % audio_sample_rate,
                          '-ac'       , '%d' % audio_channels,
                          '-'
                          ]

        logger.debug(f"Calling ffmpeg to get audio \"{' '.join(ffmpeg_command)}\"")
        completed_process = subprocess.run(ffmpeg_command, capture_output=True)

        # return completed_process.stdout
        dt = {1: 'int16', 2: 'int16', 4: 'int32'}[audio_channels]
        return np.fromstring(completed_process.stdout, dtype=dt).reshape(-1, audio_channels)

    def _write_audio(self,
                     file_path=None,
                     ffmpeg_log_level='error'
                     ):
        """
        Write audio for this clip to file

        :param file_path        : Path to the filename to write the audio
        :param ffmpeg_log_level : sets the log level to be sent to ffmpeg
        """
        logger = getLogger(__name__)

        audio_data = self.get_audio_frames()

        # FFMPEG Command to write audio to a file
        audio_codec = 'pcm_u8' if self.audio_channels == 1 else 'pcm_s%dle' % (8 * self.audio_channels)
        audio_file_format = 's8' if self.audio_channels == 1 else 's%dle' % (8 * self.audio_channels)

        ffmpeg_command = [
            self.ffmpeg_binary, '-y',
            '-loglevel', ffmpeg_log_level,                          # Set ffmpeg's log level accordingly
            "-f", audio_file_format,
            "-acodec", audio_codec,
            '-ar', "%d" % self.audio_sample_rate,
            '-ac', "%d" % self.audio_channels,
            '-i', '-',
            file_path]

        # Log the ffmpeg call we will make
        logger.debug(f"Calling ffmpeg to write audio \"{' '.join(ffmpeg_command)}\"")

        # Write all the data (via ffmpeg) to the temp file
        process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, bufsize=10 ** 8)
        logger.debug( f'Writing {audio_data.shape[0]} audio frames, {audio_data.shape[1]} channels. '
                      f'({type(audio_data).__name__}, {audio_data.dtype})')

        # Write the audio data to stdin
        process.stdin.write(audio_data.tobytes())
        process.stdin.close()
        process.wait()

    ##################
    # Public Methods #
    ##################
    def add_colors(self,
                       red_addend:int=0,
                       green_addend:int=0,
                       blue_addend:int=0,
                       luminance:int=0):
        """
        Increase or decrease each color channel and the images luminosity

        :param red_addend: Addend for the red channel, defaults to 0 (no change)
        :param green_addend: Addend for the green channel, defaults to 0 (no change)
        :param blue_addend: Addend for blue channel, defaults to 0 (no change)
        :param luminance: Addend for luminance
        :return:
        """
        logger = getLogger(__name__)
        logger.debug(f"{type(self).__name__}.add_colors(red_addend={red_addend}, green_added={green_addend}, "
                     f"blue_added={blue_addend}, luminance={luminance})")

        # If all the multipliers are 1, we have no work to do
        if red_addend == green_addend == blue_addend == luminance == 0:
            logger.warning(f"All addends are 0. No work needed.")
            return self

        # Add colors in each frame
        altered_frames = []
        luminance_array = np.array([luminance, luminance, luminance])
        red_addend_array = np.array([red_addend, green_addend, blue_addend])
        for frame in self.get_video_frames():
            altered_frames.append((frame + red_addend_array + luminance_array).astype('uint8'))

        # Replace the existing frames
        self.set_video_frames(altered_frames)

        # Return this object to enable method chaining
        return self

    def add_sound(self,
                        sound_time,
                        sound_audio_frames=None,
                        file_path=None):
        """
        Add
        :param sound_time: Sound time
        :param file_path: Path to the audio file
        """
        if file_path:
            sound_audio_frames = self._read_audio(file_path,
                                                  audio_channels=self.audio_channels,
                                                  audio_sample_rate=self.audio_sample_rate)

        # Get the existing audio frames
        audio_frames = self.get_audio_frames()

        # Insert the audio at the specified time (frame index)
        audio_frame_index = int(sound_time * self.audio_sample_rate)
        audio_frames[audio_frame_index:audio_frame_index+sound_audio_frames.shape[0]] = sound_audio_frames

        # Replace the audio frames with the newly generated audio frames
        self.set_audio_frames(audio_frames)

        # Return this object to enable method chaining
        return self


    def audio_fade_in(self, duration):
        """
        Apply a fade in to the audio track

        :param duration: Duration, in seconds, that the fade in will last for
        :return self: This object, to allow for method chaining
        """
        # Get the audio frames
        audio_frames = self.get_audio_frames()

        # Get the end frame for the audio fade in
        end_frame = int(self.audio_sample_rate * duration)

        # TODO: Implement Logarithmic fade in
        # Amplitude = Initial Amplitude * (1 - log(1 - (time / fade duration)))

        # Generate the multipliers for affected audio frames
        multipliers = [((index / self.audio_sample_rate) / duration) for index in range(end_frame)]

        # Update the audio frames in quest
        for audio_channel in range(audio_frames.shape[1]):
            audio_frames[0:end_frame,audio_channel] = audio_frames[0:end_frame,audio_channel] * multipliers

        # Replace the audio frames with the modified frames
        self.set_audio_frames(audio_frames)

        return self

    def audio_fade_out(self, duration):
        """
        Apply a gradual decrease to the level of the audio signal

        :param duration: Duration, in seconds, that the fade in will last for

        :return self: This object, to allow for method chaining
        """

        # Get the audio frames
        audio_frames = self.get_audio_frames()

        # Get the starting frame for the audio fade out
        start_frame = int(self.audio_sample_rate * duration)

        # Generate the multipliers for affected audio frames
        multipliers = [((index / self.audio_sample_rate) / duration) for index in range(start_frame, self.number_frames)]

        # Update the audio frames in quest
        for audio_channel in range(audio_frames.shape[1]):
            audio_frames[start_frame:,audio_channel] = audio_frames[start_frame:,audio_channel] * multipliers

        # Replace the audio frames with the modified frames
        self.set_audio_frames(audio_frames)

        # Allow for method chaining
        return self

    def audio_initialize(self, duration, audio_channels):
        """
        Initialize audio
        """
        logger = getLogger(__name__)
        logger.debug(f'{type(self).__name__}.audio_initialize(duration={duration},audio_channels={audio_channels})')

        # Calculate the number of frames we need
        number_frames = int(self.audio_sample_rate * duration)

        # Set the number of audio channels we have
        self.audio_channels = audio_channels

        # Set the audio frames
        audio_frames = (np.tile(np.zeros(audio_channels), number_frames)
                        .reshape(number_frames, audio_channels).astype('int16'))
        self.set_audio_frames(audio_frames)

        return self

    def audio_peak_normalize(self):
        """
        Normalize the audio track volume
        :return self: This object, to allow for method chaining
        """
        logger = getLogger()
        logger.warning(f'{type(self).__name__}.audio_peak_normalize() has not been implemented yet.')

        audio = self.get_audio_frames()

        # value_dBFS = 20*log10(rms(signal) * sqrt(2))

        return self

    def audio_stereo_volume(self, left_multiplier:float, right_multiplier:float):
        """
        Multiplies the volume of each track independently for stereo audio
        :param left_multiplier: Left track multiplier
        :param right_multiplier: Right track multiplier
        :return:
        """
        if not self.has_audio:
            raise AttributeError(f"{type(self).__name__} does not have associated audio.")


        # Ensure we have stereo data
        audio_frames = self.get_audio_frames()
        if audio_frames.shape[1] != 2:
            raise ValueError(f"Audio frames are not stereo")

        # Set the new audio frame data
        self.set_audio_frames((audio_frames * (left_multiplier, right_multiplier)).astype(np.int16))

        # Return this object to enable method chaining
        return self

    def audio_volume(self, multiplier:float) -> object:
        """
        Adjust the volume level of the audio

        :param multiplier: value to multiply the audio by
        :return self: This object (allows for method chaining)
        """
        # Make sure the clip in question has audio
        if not self.has_audio:
            raise AttributeError(f"{type(self).__name__} does not have associated audio.")

        # Set the new audio data
        audio_frames = self.get_audio_frames() * multiplier
        self.set_audio_frames(audio_frames)

        # Return this object to enable method chaining
        return self

    def bilevel(self):
        """
        Converts the video frames to a bilevel (black and white)
        :return:
        """

        altered_frames = []
        for frame in self.get_video_frames():
            image = Image.fromarray(frame).convert(ImageModes.BLACK_AND_WHITE.value)
            frame = np.stack((np.array(image), np.array(image), np.array(image)), axis=2).astype('uint8')
            altered_frames.append(frame)

        # Replace the clip frames with the now rotated frames
        self.set_video_frames(altered_frames)

        # Return this object to enable method chaining
        return self

    def blink(self,
              duration_on=2,
              duration_off=2,
              start_frame=None,
              start_frame_time=None,
              end_frame=None,
              end_frame_time=None):
        """
        Make the footage blink. This is done, by replacing the 'blinking frames' with blank frames

        :param duration_on: Duration in seconds, that the clip will blink for
        :param duration_off: Duration in seconds, that the clip will not blink for
        :param start_frame: Frame index of when the overall blinking should start
        :param start_frame_time: Time in seconds of the frame when the overall blinking should start
        :param end_frame: Frame index of when the overall blinking should end
        "param end_frame_time: Time in seconds of the frame when the overall blinking should end
        """
        logger = getLogger(__name__)
        logger.debug(f'{type(self).__name__}.blink(duration_on={duration_on},duration_off={duration_off}, '
                     f'start_frame={start_frame},start_frame_time={start_frame_time}, end_frame={end_frame},'
                     f'end_frame_time={end_frame_time})')


        # Set the start frame according to user input
        if not start_frame_time and not start_frame:
            start_frame = 0
        elif start_frame_time and start_frame:
            logger.warning('start_frame_time and start_frame supplied, start_frame_time will be ignored.')
        elif start_frame_time and not start_frame:
            start_frame = int(self.fps * start_frame_time)

        # Set the end frame according to user input
        if not end_frame_time and not end_frame:
            end_frame = self.number_frames
        elif end_frame_time and end_frame:
            logger.warning('end_frame_time and end_frame both supplied, start_frame_time will be ignored.')
        elif start_frame_time and not start_frame:
            end_frame = int(self.fps * start_frame_time)

        # Calculate blink on/off frames
        blink_on_frames_duration = int(self.fps * duration_on)
        blink_off_frames_duration = int(self.fps * duration_off)
        # Get the video frames
        current_frames = self.get_video_frames()

        # Iterate through the frames and create new list of frames
        new_frames = []
        blink = {'blink':True, 'number_frames':blink_on_frames_duration}
        for i in range(len(current_frames)):
            # We are outside the effect range, so the frame is not modified
            if (i < start_frame) or (i >= end_frame):
                new_frames.append(current_frames[i])
            elif blink['blink']:
                # Create / add the blank frame
                blank_frame = numpy.tile(numpy.array((0,0,0)), self.height*self.width).reshape(self.height, self.width, 3)
                new_frames.append(blank_frame)

                # Decrement the amount of blinking frames we need
                blink['number_frames'] -= 1

                # we added all the blinking frames, switch blink state
                if blink['number_frames'] == 0:
                    blink = {'blink':False, 'number_frames': blink_off_frames_duration}
            else:
                # Add the frame, as we're not blinking
                new_frames.append(current_frames[i])

                # Decrement the amount of non-blinking frames we need
                blink['number_frames'] -= 1

                # we added all the non-blinking frames, switch blink state
                if blink['number_frames'] == 0:
                    blink = {'blink':False, 'number_frames': blink_off_frames_duration}

        self.set_video_frames(new_frames)

        # Enables object method chaining
        return self

    def border(self,
               border:int=0,
               border_left:int=0,
               border_right:int=0,
               border_top:int=0,
               border_bottom:int=0,
               fill_color=(255,255,0)):
        """
        Add a border (could be thought of as a margin or frame as well).
        Basically add X pixels around the existing image in the requested color.

        :param border        : Border in pixels to create around the existing frames
        :param border_left   : Left border to create around the frame (will be added to border if specified)
        :param border_right  : Right border to create around the frame (will be added to border if specified)
        :param border_top    : Top border to create around the frame (will be added to border if specified)
        :param border_bottom : Bottom border to create around the frame (will be added to border if specified)
        :param fill_color    : Color to use for the border
        """
        # Determine the border sizes
        border_left = border + border_left
        border_right = border + border_right
        border_top = border + border_top
        border_bottom = border + border_bottom

        # Generate the border arrays
        border_height = border_top+self.height+border_bottom
        left_column = np.tile(np.array(fill_color), border_height*border_left).reshape(border_height, border_left, 3)
        right_column = np.tile(np.array(fill_color), border_height*border_right).reshape(border_height, border_right, 3)
        top_row = np.tile(np.array(fill_color), border_top*self.width).reshape(border_top, self.width, 3)
        bottom_row = np.tile(np.array(fill_color), border_bottom*self.width).reshape(border_bottom, self.width, 3)

        # Update the frames
        altered_frames = []
        new_frame = None
        for frame in self.get_video_frames():
            new_frame = np.concatenate((top_row, frame, bottom_row), axis=0)           # Concatenate Rows
            new_frame = np.concatenate((left_column, new_frame, right_column), axis=1) # Concatenate Columns
            altered_frames.append(new_frame.astype('uint8')) # Add to our list of altered frames

        # Set the new frame shape
        self.height = new_frame.shape[0]
        self.width = new_frame.shape[1]

        # Set the new frames for this video
        self.set_video_frames(altered_frames)

        # Enable method chaining
        return self

    def pixelate(self, pixel_size=32):
        """
        Convert the footage to game console footage

        :param pixel_size: What video game console should the footage resemble
        :return self: Enables method chaining
        """
        logger = getLogger()
        logger.debug(f"{type(self).__name__}.consolize(pixel_size={pixel_size})")

        altered_frames = []
        for frame in self.get_video_frames():
            image = Image.fromarray(frame)

            # Resize smoothly down
            image_small = image.resize((pixel_size, pixel_size), resample=Image.Resampling.BILINEAR)

            # Scale back up using NEAREST to original size, and add it to the altered frames
            altered_frames.append(np.array(image_small.resize(self.size, Image.Resampling.NEAREST)))

        # Update clip frames
        self.set_video_frames(altered_frames)

        # Enable method chaining
        return self


    def crop(self,
             top_left_x:int=0,
             top_left_y:int=0,
             bottom_right_x:int=None,
             bottom_right_y:int=None,
             center_x:int=None,
             center_y:int=None,
             height:int=None,
             width:int=None
             ):
        # Get a logger to, well uhm, log stuff
        logger = getLogger(__name__)

        # Calculate the top level & bottom right position of the area to be cropped
        if width and top_left_x:
            bottom_right_x = int(top_left_x + width)
        elif width and bottom_right_x:
            top_left_x = int(bottom_right_x - width)

        if height and top_left_y and (not center_y):
            bottom_right_y = int(top_left_y + height)
        elif height and bottom_right_y and (not center_y):
            top_left_y = int(bottom_right_y - height)

        if center_x:
            top_left_x = int(center_x - width / 2)
            bottom_right_x = int(center_x + width / 2)

        if center_y:
            top_left_y = int(center_y - height / 2)
            bottom_right_y = int(center_y + height / 2)

        bottom_right_x = int(bottom_right_x or self.width)
        bottom_right_y = int(bottom_right_y or self.height)

        # Update the height and width of the clip now that we cropped the image
        self.height = bottom_right_y - top_left_y
        self.width = bottom_right_x - top_left_x

        # Get the frames to be processed
        frames = self.get_video_frames()

        # Crop the frames
        logger.debug(f"Cropping image from ({top_left_x},{top_left_y}) to ({bottom_right_x},{bottom_right_y})")
        cropped_frames = []
        for frame in frames:
            cropped_frame = frame[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
            cropped_frames.append(cropped_frame)

        logger.debug(f"{len(cropped_frames)} frames cropped")

        # Replace the frames with the new frames
        self.set_video_frames(cropped_frames)

        # Enable method chaining
        return self

    def cut(self, start_time=None, end_time=None):
        """
        Cuts the requested time out of the clip.
        Will reset

        :param start_time: frames earlier than this time will be excluded from the clip
        :param end_time: frames later than this time will be excluded from the clip
        :return self: Enables method chaining
        """
        logger = getLogger(__name__)

        # Let the user no that they called trim without purpose
        logger.debug(f"{type(self).__name__}.trim(start_time={start_time}, end_time={end_time})")
        if not start_time and not end_time:
            logger.warning(f"Nothing to cut")


        # Alter the video frames accordingly
        if self.has_video:
            # Get the frames
            frames = self.get_video_frames()

            # Determine the cut frame indices
            start_index = int(self.fps * start_time)
            end_index = int(self.fps * end_time)

            # Cut out the frames of the clip we don't want
            frames = frames[0:start_index] + frames[end_index:]

            # Update the clip attributes
            self.set_video_frames(frames)
            self.number_frames = len(frames)

            # Should this line, be outside the if block??
            self.end_time = len(frames) / self.fps

        # Alter the audio data accordingly
        if self.has_audio:
            # Get the audio frames
            audio_frames = self.get_audio_frames()

            # Determine the cut frame indices
            start_index = int(self.audio_sample_rate * start_time)
            end_index = int(self.audio_sample_rate * end_time)

            # Cut out the frames of the clip we don't want
            audio_frames = np.concatenate([audio_frames[0:start_index],audio_frames[end_index:]], axis=0)
            self.set_audio_frames(audio_frames)

        # Enable method chaining
        return self

    def divide_colors(self,
                       red_divisor:float=1,
                       green_divisor:float=1,
                       blue_divisor:float=1,
                       luminance:float=1):
        """
        Divides each color channel and the image's luminosity

        :param red_divisor: Multiplier for the red channel
        :param green_divisor: Multiplier for the green channel
        :param blue_divisor: Multiplier for blue channel
        :param luminance: Multiplier for luminance

        :raises ValueError: A divisor with the value of 0 was supplied as an input

        :return self: Enables method chaining
        """
        logger = getLogger(__name__)

        # If all the multipliers are 1, we have no work to do
        if red_divisor == green_divisor == blue_divisor == luminance == 1:
            logger.warning(f"All divisors, set to 1. No work needed.")
            return self

        if red_divisor or green_divisor or blue_divisor or luminance == 0:
            raise ValueError(f"divisor can not be zero.")

        # Multiply colors in each frame
        logger.debug(f"Color Divisors : Red x {red_divisor}, Green x {green_divisor}, "
                     f"Blue x {blue_divisor}, Luminance={luminance}")
        altered_frames = []
        luminance_array = np.array([luminance, luminance, luminance])
        for frame in self.get_video_frames():
            altered_frames.append((frame / (red_divisor, green_divisor, blue_divisor) / luminance_array).astype('uint8'))

        # Replace the existing frames
        self.set_video_frames(altered_frames)

        # Return this object to enable method chaining
        return self

    def invert_colors(self):
        """
        Invert colors of the footage

        :return self: Enables method chaining
        """
        logger = getLogger(__name__)

        # Invert colors of each frame
        logger.debug(f"Inverting colors")
        altered_frames = []
        for frame in self.get_video_frames():
            altered_frames.append((255 - frame).astype('uint8'))

        # Replace the existing frames
        self.set_video_frames(altered_frames)

        # Return this object to enable method chaining
        return self

    def even_dimensions(self):
        """
        Trims the height and width of the clip as needed so that they are both even values
        Affects: Video

        :return self: Enables method chaining
        """
        # Debug log the method call
        logger = getLogger(__name__)
        logger.debug(f"{type(self).__name__}.even_dimensions()")

        # Check if there is any work to do
        if (self.size[0] % 2 == 0) and (self.size[1] % 2 == 0):
            logger.warning(f"The dimensions {self.size} are already even, no work needed.")
            return self

        # Get the existing frames
        video_frames = self.get_video_frames()

        # Trim 1 pixel from height and/or width as needed
        altered_frames = []
        for frame in video_frames:
            # The height of the frame is odd
            if frame.shape[0] % 2 == 1:
                frame = frame[:-1, :, :]

            # The width of the frame is odd
            if frame.shape[1] % 2 == 1:
                frame = frame[:,:-1,:]

            altered_frames.append(frame)

        # Replace the existing frames with the newly generated ones
        self.set_video_frames(altered_frames)

        # Enable method chaining
        return self

    def fade_in(self,
                duration,
                fade_in_color=(0,0,0)):
        """
        Fade in from fade in color to the footage over the duration color
        Affects: Video

        :param duration:
        :param fade_in_color:
        """
        pass

    def fade_out(self,
                 duration,
                 fade_out_color=(0,0,0)):
        """
        Fade out from the footage to the fade out color over the duration
        Affects: Video

        :param duration:
        :param fade_out_color:
        :return:
        """
        pass

    def freeze(self,
               time:float,
               duration:float
               ):
        """
        Freeze the clip at `time` for `duration` seconds
        """
        # Debug logging for the call itself
        logger = getLogger(__name__)
        logger.debug(f"{type(self).__name__}.freeze(time={time},duration={duration})")

        # Get the video frames
        video_frames = self.get_video_frames()
        logger.debug(f"{len(video_frames)} frames detected")

        # Determine where to start the freeze, and for how long
        duration_frames = int(duration * self.fps)
        freeze_index = int(time * self.fps)
        logger.debug(f"Freezing frame {freeze_index} for {duration_frames} frames (fps={self.fps})")

        freeze_frames = [video_frames[freeze_index]] * duration_frames

        # Build the new list of video frames
        new_video_frames = (video_frames[0:freeze_index]
                            + freeze_frames
                            + video_frames[freeze_index+duration_frames:len(video_frames)])
        logger.debug(f"{len(new_video_frames)} frames, after freeze applied")

        # Replace the video frames with the newly altered frames
        self.set_video_frames(new_video_frames)

        # Enable method chaining
        return self

    def freeze_region(self, time:float, duration:float, inside=None,outside=None):
        """
        Freeze a region of the clip at `time` for `duration`.

        :param time: Time, in seconds, to start freezing the region
        :param duration, Duration, in seconds, that the region should be frozen for
        :param inside: (x1,y1,x2,y2) boundaries for the region to be frozen
        :param outside (x1,y1,x2,y2) boundaries for the region that will not be frozen

        :return self: Enables method chaining
        """
        logger = getLogger(__name__)
        logger.debug(f'{type(self).__name__}.freeze_region(time={time}, duration={duration}, '
                     f'inside={inside}, outside={outside})')

        if (not inside) and (not outside):
            logger.warning(f'No region provided. Nothing to do.')
            return self

        if inside and outside:
            logger.warning(f'inside and outside provided. Only inside={inside} will be used')

        # Get the video frames
        video_frames = self.get_video_frames()
        logger.debug(f"{len(video_frames)} frames detected")

        # Determine where to start the freeze, and for how long
        duration_frames = int(duration * self.fps)
        freeze_index = int(time * self.fps)

        frozen_frame = video_frames[freeze_index]
        freeze_frames = []
        for i in range(duration_frames):
            frame = video_frames[freeze_index + i]
            new_frame = None
            if inside:
                new_frame = frame
                new_frame[inside[0]:inside[2], inside[1]:inside[3]] = frozen_frame[inside[0]:inside[2], inside[1]:inside[3]]
            elif outside:
                new_frame = frozen_frame
                new_frame[outside[0]:outside[2], outside[1]:outside[3]] = frame[outside[0]:outside[2], outside[1]:outside[3]]

            freeze_frames.append(new_frame)

        # Build the new list of video frames
        new_video_frames = video_frames[0:freeze_index] + freeze_frames + video_frames[freeze_index:len(video_frames)]
        logger.debug(f"{len(new_video_frames)} frames, after freeze applied")

        # Replace the video frames with the newly altered frames
        self.set_video_frames(new_video_frames)

        # Enables method chaining
        return self

    def gamma_correction(self,
                         gamma:float):
        """
        Gamma correction is a nonlinear operation used to encode and decode luminance values

        :param gamma: gamma value to use
        :return self: Enable method chaining
        """
        # Get a logger
        logger = getLogger(__name__)

        # Update frames
        logger.info(f"Gamma correcting footage (gamma='{gamma}')")
        altered_frames = []
        for frame in self.get_video_frames():
            new_frame = (255 * (1.0 * frame / 255) ** gamma).astype('uint8')
            altered_frames.append(new_frame)

        self.set_video_frames(altered_frames)
        logger.info(f"Finished gamma correcting footage (gamma='{gamma}')")

        # Enable method chaining
        return self

    def get_audio_frames(self):
        """
        Get audio data from an audio or video file

        :return:
        """
        logger = getLogger(__name__)
        logger.debug(f"{type(self).__name__}.get_audio_frames(), "
                     f"frames_initialized={self._audio['frames_initialized']}.")

        # We have already initialized the frames, so we can just return them
        if self._audio['frames_initialized']:
            return self._audio['frames']

        # Mark the frames as having been initialized
        self._audio['frames_initialized'] = True

        # We have a file that may have audio, and we will attempt to get the frames from it
        if self.file_path:
            audio_frames = self._read_audio(file_path=self.file_path,
                                            audio_channels=self.audio_channels,
                                            audio_sample_rate=self.audio_sample_rate)
            self.set_audio_frames(audio_frames)

        # We were given a get_frame(t) function that we can use to generate the frames
        if self._audio['get_frame']:
            logger.debug('audio_get_frame function detected. ')

            # Determine the number of audio channels that the audio frame function produces
            audio_channels = len(self._audio['get_frame'](0))

            # Set self.audio_channels, and notify the user appropriately
            if self.audio_channels is None:
                logger.debug(f"Setting {type(self).__name__}.audio_channels={audio_channels}")
                self.audio_channels = audio_channels
            elif self.audio_channels != audio_channels:
                logger.warning(f"{audio_channels} audio channels detected, "
                               f"but {type(self).__name__}.audio_channels == {self.audio_channels}. ")
                logger.warning(f"Setting {type(self).__name__}.audio_channels={audio_channels}")
                self.audio_channels = audio_channels

            # Generate the audio frames in question
            audio_frames = []
            start_frame = int(self.start_time * self.audio_sample_rate)
            end_frame = int(self.end_time * self.audio_sample_rate)
            frame_time = self.start_time
            for i in range(start_frame, end_frame):
                frame_time +=  (1 / self.audio_sample_rate)
                audio_frame = self._audio['get_frame'](frame_time)
                audio_frames.append(audio_frame)
            logger.debug(f"{len(audio_frames)}  audio frames created. Clip duration of {self.duration} second(s).")

            data_type = {1: 'int16', 2: 'int16', 4: 'int32'}[self.audio_channels]
            audio_frames = np.array(audio_frames)
            audio_frames = np.maximum(-0.99, np.minimum(0.99, audio_frames))
            audio_frames = (2 ** (8 * self.audio_channels - 1) * audio_frames).astype(data_type)

            # Set the newly created audio frames to be the audio frames for the clip
            self.set_audio_frames(audio_frames)

        # Return the audio frames
        return self._audio['frames']

    def get_mask_frames(self, pixel_format=None):
        """
        Get the mask frames for this clip
        :return:
        """

        # Previously initialized frames have been created, so return them
        if self._mask['initialized']:
            return self._mask['frames']

        # Default the pixel format to the clip's pixel_format value
        if not pixel_format:
            pixel_format = self.pixel_format

        # Generate mask cell

        # No mask exists, so we need to create one
        if not self._mask['frames']:
            number_components = PIXEL_FORMATS[pixel_format]['nb_components']
            mask_cell = np.tile(True, number_components)
            self._mask['frames'] = [np.tile(mask_cell, self.width * self.height)
                                    .reshape(self.height, self.width, number_components)]

        # If mask behavior is to loop, then create all the mask frames we need, and replace the mask frames we had
        if self._mask['behavior'] == Behavior.LOOP_FRAMES.value:
            looped_mask_frames = []
            for frame_index in range(self.number_frames):
                mask_frame_index = frame_index % len(self._mask['frames'])
                looped_mask_frames.append(self._mask['frames'][mask_frame_index])

            self._mask['frames'] = looped_mask_frames

        # Update the mask initialized flag
        self._mask['initialized'] = True

        # Return the mask frames
        return self._mask['frames']

    def get_video_frames(self, pixel_format=None):
        """
        Get the video frames list for this clip
        :param pixel_format: Pixel format of the video frames, If None will use the clip's pixel format
        :return:
        """
        # Debug message for the method call itself
        logger = getLogger(__name__)
        logger.debug(f'{type(self).__name__}.get_video_frames(pixel_format={pixel_format})')

        # We already have frames, and they are already in the right pixel format
        if self._video['frames_initialized'] and ((pixel_format is None) or (pixel_format == self.pixel_format)):
            return self._video['frames']

        # We have frames, but they are not in the right pixel format and convert to rgba
        if self._video['frames_initialized'] and pixel_format == 'rgba' and self.pixel_format == 'rgb24':
            logger.debug(f'Converting {len(self._video['frames'])} video frames to {pixel_format}')
            # Create the new frame data
            new_frames = []
            for frame in self._video['frames']:
                new_frame = []
                flattened_frame = frame.flatten()
                for i in range(0, len(flattened_frame), 3):
                    pixel = (flattened_frame[i:i+3][0],flattened_frame[i:i+3][1],flattened_frame[i:i+3][2],1)
                    new_frame.append(pixel)
                new_frames.append(numpy.array(new_frame).reshape(self.height, self.width, 4).astype('uint8'))

            return new_frames

        # We have rgba frames but need rgb24 frames
        if self._video['frames_initialized'] and pixel_format == 'rgb24' and self.pixel_format == 'rgba':
            logger.debug(f'Converting {len(self._video['frames'])} video frames to {pixel_format}')
            # Create the new frame data
            new_frames = []
            for frame in self._video['frames']:
                new_frame = []
                flattened_frame = frame.flatten()
                for i in range(0, len(flattened_frame), 4):
                    pixel = (flattened_frame[i:i+4][0],flattened_frame[i:i+4][1],flattened_frame[i:i+4][2])
                    new_frame.append(pixel)
                new_frames.append(numpy.array(new_frame).reshape(self.height, self.width, 4).astype('uint8'))

            return new_frames

        # No frames yet exist, default to using the video frames we have
        video_frames = self.get_video_frames_from_file(pixel_format)

        # Determine how many frames we need
        frames_needed = self.end_frame - self.start_frame

        # We need more frames than we have, and we are to enforce the limit
        if (frames_needed > self.video_number_frames) and self.behavior == Behavior.ENFORCE_LIMIT.value:
            raise ValueError(f"Frames needed ({frames_needed}) exceeds the available "
                             f"number of video frames ({self.video_number_frames})")

        # We need fewer frames than we have
        if frames_needed <= self.video_number_frames:
            self.set_video_frames(video_frames[self.start_frame:self.end_frame])
        # We need to loop over the footage till we have the amount of frames we need
        elif self.behavior == Behavior.LOOP_FRAMES.value:
            looped_frames = []

            while frames_needed > 0:
                if frames_needed > self.video_number_frames:
                    looped_frames.extend(video_frames)
                    frames_needed -= self.video_number_frames
                else:
                    looped_frames.extend(video_frames[0:frames_needed])
                    frames_needed -= frames_needed

            self.set_video_frames(looped_frames)
        # Need to pad the footage
        elif self.behavior == Behavior.PAD.value:
            color = (77, 128, 90)
            number_pad_frames = frames_needed - self.video_number_frames
            pad_frame = (np.tile(color, self.width * self.height)
                          .reshape(self.height, self.width, 3)
                          .astype('uint8'))

            video_frames.extend([pad_frame] * number_pad_frames)
            self.set_video_frames(video_frames)

        # Indicate the frames have been initialized
        self._video['frames_initialized'] = True

        # Return the frames
        return self._video['frames']

    def get_video_frames_from_file(self, pixel_format=None):
        """
        Get the video frames
        :return: List of frames
        """
        logger = getLogger(__name__)

        # Set the pixel format to either the input parameter or the class attribute
        pixel_format = pixel_format if pixel_format else self.pixel_format
        pixel_format_info = PIXEL_FORMATS[pixel_format]

        # Call ffmpeg and pipe it's output
        command = [self.ffmpeg_binary,
                   '-i', self.file_path,                        # File we will load video frames from
                   '-f', 'image2pipe',                          # Format is 'image2pipe'
                   '-pix_fmt', pixel_format,                    # Pixel format we will use internally
                   '-vcodec', 'rawvideo',                       # Set video codec to 'rawvideo'
                   '-']                                         # Pipe the output

        # Read the video data
        logger.debug(f'Calling ffmpeg to get video \"{' '.join(command)}\"')
        completed_process = subprocess.run(command, capture_output=True)

        # Get all frames
        frame_length = self._video['width'] * self._video['height'] * pixel_format_info['nb_components']
        video_frames = []
        for i in range(0, len(completed_process.stdout), frame_length):
            frame = completed_process.stdout[i:i + frame_length]
            frame = (np.fromstring(frame, dtype='uint8')
                     .reshape(self._video['height'], self._video['width'], pixel_format_info['nb_components']))


            # Store the frame in our frames list
            video_frames.append(frame)

        # Return the video frames
        return video_frames

    def get_video_frame(self,
                  frame_index:int=None,
                  frame_time:int=None,
                  loop_frames=False):
        """
        Get a specific frame from this clip

        :param frame_index: Index of the frame we want to retrieve
        :param frame_time: time in seconds of the frame to retrieve
        :param loop_frames: Should we throw an error or loop through the frames when given an out of range index
        :return:
        """
        # Get the video frames
        frames = self.get_video_frames()

        # Ensure we have valid input
        if (frame_index is None) and (frame_time is None):
            msg = f"Either frame_index or frame_time must be provided to {type(self).__name__}.get_video_frame()"
            raise ValueError(msg)
        elif frame_index and frame_time:
            msg = f"Both frame_index and frame_time cannot be simultaneously be specified. "
            raise ValueError(msg)

        # Get the frame index
        if frame_time:
            frame_index = int(self.video_fps * frame_time)

        # Do we have a negative integer, if so count from the back of the array
        if (frame_index < 0) and (abs(frame_index) <= len(frames)):
            frame_index = len(frames) + frame_index

        # If requested, loop over the frames for an out of range value
        if loop_frames:
            frame_index = frame_index % len(frames)

        # Return the requested frame
        return frames[frame_index]

    def grayscale(self):
        """
        Converts the video to grayscale

        :return self: Enables method chaining
        """
        altered_frames = []
        for frame in self.get_video_frames():
            image = Image.fromarray(frame).convert(ImageModes.GRAYSCALE.value)
            frame = np.stack((np.array(image), np.array(image), np.array(image)), axis=2).astype('uint8')
            altered_frames.append(frame)

        # Replace the clip frames with the now rotated frames
        self.set_video_frames(altered_frames)

        # Return this object to enable method chaining
        return self

    def mirror_x(self):
        """
        Flips the clip frames left to right

        :return self: Enable method chaining
        """
        flipped_frames = []
        for frame in self.get_video_frames():
            image = Image.fromarray(frame).transpose(Transpose.FLIP_LEFT_RIGHT.value)
            flipped_frames.append(np.array(image))

        # Replace the clip frames with the now rotated frames
        self.set_video_frames(flipped_frames)

        # Return this object to enable method chaining
        return self

    def mirror_y(self):
        """
        Flip the clip frames top to bottom

        :return self: Enable method chaining
        """
        flipped_frames = []
        for frame in self.get_video_frames():
            image = Image.fromarray(frame).transpose(Transpose.FLIP_TOP_BOTTOM.value)
            flipped_frames.append(np.array(image))

        # Replace the clip frames with the now rotated frames
        self.set_video_frames(flipped_frames)

        # Return this object to enable method chaining
        return self

    def multiply_colors(self,
                       red_multiplier:float=1,
                       green_multiplier:float=1,
                       blue_multiplier:float=1,
                       luminance:float=1):
        """
        Increase or decrease each color channel and the images luminosity

        :param red_multiplier: Multiplier for the red channel
        :param green_multiplier: Multiplier for the green channel
        :param blue_multiplier: Multiplier for blue channel
        :param luminance: Multiplier for luminance
        :return:
        """
        """
        Increases or Decreases a given color component of each frame
        :return:
        """
        logger = getLogger(__name__)

        # If all the multipliers are 1, we have no work to do
        if red_multiplier == green_multiplier == blue_multiplier == luminance == 1:
            logger.warning(f"All multipliers, set to 1. No work needed.")
            return self

        # Multiply colors in each frame
        logger.debug(f"Multiply Colors - Red x {red_multiplier}, Green x {green_multiplier}, "
                     f"Blue x {blue_multiplier}, Luminance={luminance}")
        altered_frames = []
        luminance_array = np.array([luminance, luminance, luminance])
        for frame in self.get_video_frames():
            altered_frames.append((frame * (red_multiplier, green_multiplier, blue_multiplier) * luminance_array).astype('uint8'))

        # Replace the existing frames
        self.set_video_frames(altered_frames)

        # Return this object to enable method chaining
        return self

    def play_audio(self, ffplay_log_level='error'):
        """
        Play the audio associated to this clip

        :param ffplay_log_level: Log level to pass to the ffplay call
        """
        logger = getLogger(__name__)
        logger.debug(f'{type(self).__name__}.play_audio()')

        # Get audio frames
        audio_data = self.get_audio_frames()

        ffplay_command = [FFPLAY_BINARY,
                          '-loglevel','error',
                          '-autoexit',
                          '-nodisp',
                          '-f','s16le',
                          '-ar', str(self.audio_sample_rate),
                          '-ac', str(self.audio_channels),
                          '-i', '-']

        # Log the ffplay call we will make
        logger.debug(f"Calling ffplay to play audio \"{' '.join(ffplay_command)}\"")

        # Call ffplay, and pipe the audio data to it
        process = subprocess.Popen(ffplay_command, stdin=subprocess.PIPE, bufsize=10 ** 8)
        process.stdin.write(audio_data.tobytes())

    def resize(self, *args, **kwargs):
        """
        Resize the video frames for the clip

        :param: args: Positional arguments. If only one supplied it will be assumed to be kwargs['multiplier']
        :param kwargs['multiplier']: Resizing multiplier
        :param kwargs['resample']: Which resampling method to use during resizing (Defaults to BICUBIC)

        :return self: (to enable method chaining)
        """
        # Instantiate local variables
        new_height = None
        new_width = None

        # We received 1 argument, treat it to be multiplier
        if len(args) == 1:
            kwargs['multiplier'] = args[0]


        # Default the resample method to BICUBIC
        if ('resample' not in kwargs) or (not kwargs['resample']):
            kwargs['resample'] = Resampling.BICUBIC.value


        if 'multiplier' in kwargs:
            new_height = int(self.height * float(kwargs['multiplier']))
            new_width =  int(self.width * float(kwargs['multiplier']))


        # Update the frames
        altered_frames = []
        for frame in self.get_video_frames():
            image = Image.fromarray(frame).resize((new_width, new_height), kwargs['resample'])
            altered_frames.append(np.array(image).astype('uint8'))

        # Adjust the size of the clip
        self.height = new_height
        self.width = new_width

        # Set the new frames for this video
        self.set_video_frames(altered_frames)

        # Return this object to enable method chaining
        return self

    def reverse_time(self):
        """
        Reverse the video frames for the clip
        :return self: (to enable method chaining)
        """

        # Reverse the footage
        self.set_video_frames(self.get_video_frames()[::-1])

        # Return this object to enable method chaining
        return self

    def rotate(self, angle) -> object:
        """
        Rotates the frames in video around the pivot point
        :param angle: Angle in degrees counter-clockwise
        :return self: (to enable method chaining)
        """

        #TODO: Add clip_start and clip_end as parameters to this method

        # Rotate each frame in the clip
        rotated_frames = []
        for frame in self.get_video_frames():
            image = Image.fromarray(frame).rotate(angle)
            rotated_frames.append(np.array(image))

        # Replace the clip frames with the now rotated frames
        self.set_video_frames(rotated_frames)

        # Return this object to enable method chaining
        return self

    def set_audio_frames(self, value):
        """
        Set the audio data for this clip

        :param value: numpy array of audio frames
        :return self: Enables method chaining
        """
        # Ensure we have an n dimensional array
        if not isinstance(value, np.ndarray):
            raise ValueError(f"{type(self).__name__}.audio_data must be an numpy array")

        # Set frames initialized to True
        self._audio['frames_initialized'] = True

        # Set self._audio['frames'] to `value`
        self._audio['frames'] = value

        # Set the number of audio frames we have
        self.audio_number_frames = value.shape[0]

        # Enable method chaining
        return self

    def set_pixel_format(self, pixel_format):
        """
        Sets the pixel format for the video frames.
        If necessary, this will cause the video frames to be converted

        :param pixel_format: Pixel format string
        """
        # Debug logging of the method call
        logger = getLogger(__name__)
        logger.debug(f'{type(self).__name__}.set_pixel_format(pixel_format={pixel_format})')

        # Make sure this is a pixel format we know how to convert
        if pixel_format not in FILMPY_SUPPORTED_PIXEL_FORMATS:
            logger.warning(f"'{pixel_format}' is not a supported pixel format")
            return self

        # Is the clip already in the format in the user requested
        if pixel_format == self.pixel_format:
            logger.warning(f"Clip is already in '{pixel_format}'. Nothing to do.")
            return self

        # Update the clip as needed
        self.set_video_frames(self.get_video_frames(pixel_format))
        self.pixel_format = pixel_format

        return self

    def set_video_frames(self, value):
        """
        Set the new clip frames
        """
        if not isinstance(value, list):
            raise ValueError(f"{type(self).__name__}.clip_frames must be a list of numpy.array objects")

        # The video frames have now been initialized
        self._video['frames_initialized'] = True

        # Set the video frames to the new list of frames
        self._video['frames'] = value

        # Update the number of frames
        self.number_frames = len(value)

        # Reset the start and end times for the clip
        self.start_time = 0
        self.end_time = float(self.number_frames / self.fps)
        
        # Enables method chaining
        return self

    def trim(self, exclude_before=None, exclude_after=None):
        """
        Trim the audio/video to exclude the requested frames

        :param exclude_before: frames earlier than this time will be excluded from the clip
        :param exclude_after: frames later than this time will be excluded from the clip
        :return self: Enables method chaining
        """
        logger = getLogger(__name__)

        # Let the user no that they called trim without purpose
        logger.debug(f"{type(self).__name__}.trim(exclude_before={exclude_before}, exclude_after={exclude_after})")
        if not exclude_before and not exclude_after:
            logger.warning(f"No trimming requested")

        # We need to trim material at the beginning of the clip
        if exclude_before:
            self.start_time = exclude_before

        # We need to trim material at the end of the clip
        if exclude_after:
            self.end_time = exclude_after

        # Alter the video frames accordingly
        if self.has_video:
            self.set_video_frames(self.get_video_frames())

        # Alter the audio data accordingly
        if self.has_audio:
            audio_frames = self.get_audio_frames()
            self.set_audio_frames(audio_frames[self.audio_start_index:self.audio_end_index])

        # Enable method chaining
        return self

    def write_audio(self, file_path:str,
                    ffmpeg_log_level='error'):
        """
        Write the audio associated to this clip to an audio file

        :param file_path: Where to write the audio file to
        :param ffmpeg_log_level: Sets the log level of ffmpeg

        :return self: Enables method chaining
        """
        logger = getLogger(__name__)

        self._write_audio(file_path=file_path,
                          ffmpeg_log_level=ffmpeg_log_level)

        logger.info(f"Audio file created '{file_path}'")

        # Enable method chaining
        return self

    def write_image(self, file_path, frame_index:int=0, frame_time:int=None) -> bool:
        """
        Write a single frame out as an image file
        :return: True, if successful
        """
        logger = getLogger(__name__)

        # Ensure we have valid input
        if (frame_index is None) and (frame_time is None):
            msg = f"Either frame_index or frame_time must be provided to {type(self).__name__}.write_image()"
            raise ValueError(msg)

        if frame_index and frame_time:
            msg = f"Both frame_index and frame_time cannot be simultaneously be specified. "
            raise ValueError(msg)

        frame = self.get_video_frame(frame_index=frame_index, frame_time=frame_time)

        command = [self.ffmpeg_binary,
                   "-y",
                   "-loglevel", "error",                # Only notify us of errors
                   "-s", self.resolution,
                   '-f','rawvideo',
                   '-pix_fmt', self.pixel_format, # Format that we will be sending the data in
                   '-i', '-',
                   file_path
                   ]


        # Call ffmpeg, and pip the data to the subprocess
        logger.debug(f"Calling ffmpeg : {' '.join(command)}")

        process = subprocess.Popen(command, stdout=DEVNULL, stdin=PIPE)
        _, process_error = process.communicate(frame.tobytes())
        if process.returncode:
            raise IOError(process_error)

        # Delete the process
        del process

        # File was successfully created
        return True

    def write_video(self,
                    file_path,
                    write_audio=True,
                    audio_codec=None,
                    file_video_codec=None,
                    file_pixel_format='yuv420p',
                    ffmpeg_log_level='error'):
        """
        Writes this clip to a video file

        :param file_path: Output video's path
        :param write_audio: Boolean, should we write the audio as well as the video. Defaults to True.
        :param audio_codec: Audio Codec to use
        :param file_video_codec: Video Codec to use when writing the file
        """
        # Get a logger
        logger = getLogger(__name__)
        logger.debug(f"{type(self).__name__}.write_video(file_path={file_path}, write_audio={write_audio}, "
                     f"audio_codec={audio_codec}, file_video_codec={file_video_codec}, "
                     f"file_pixel_format={file_pixel_format}, ffmpeg_log_level={ffmpeg_log_level})")

        # Get filename and extension from the file path
        file_name, ext = os.path.splitext(os.path.basename(file_path))
        ext = ext[1:].lower()

        # Ensure we were given a video codec or have a default for this file extension
        if (file_video_codec is None) and (ext in VIDEO_CODECS):
            file_video_codec = VIDEO_CODECS[ext][0]
        else:
            raise ValueError(f"No default video codec found for '{ext}'")

        # Ensure we were given a video codec or have a default for this file extension
        # otherwise default to 'libmp3lame'
        if (audio_codec is None) and (ext in AUDIO_CODECS):
            audio_codec = AUDIO_CODECS[ext][0]
        else:
            audio_codec = "libmp3lame"

        # Determine audio extension
        audio_extension = None
        for extension, extension_codecs in AUDIO_CODECS.items():
            if audio_codec in extension_codecs:
                audio_extension = extension

        # Write the video to the file
        command = [self.ffmpeg_binary,
                   '-y',                                     # Overwrite output file if it exists
                   '-loglevel', ffmpeg_log_level,            # Set ffmpeg's log level accordingly
                   '-f', 'rawvideo',                         # Raw video format
                   '-vcodec', 'rawvideo',                    # Video Codec
                   '-s', self.resolution,                    # size of one frame
                   '-pix_fmt', self.pixel_format,            # pixel format we used when loading in the image
                   '-r', '%d' % self.fps,                    # frames per second
                   '-i', '-',                                # the input comes from a pipe
                   ]

        # If we have an audio stream and we are to write audio
        audio_file_name = None
        if self._audio and write_audio:
            # Write the audio to disk
            audio_file_name = f"{file_name}_wvf_snd.tmp.{audio_extension}"
            self._write_audio(file_path=audio_file_name,
                              ffmpeg_log_level=ffmpeg_log_level)

            # Extend the command to pass in the audio we just recorded
            command.extend([
                '-i', audio_file_name,
                '-acodec', 'copy'
            ])

        else:
            command.extend(['-an']) # tells FFMPEG not to expect any audio

        # Parameters relating to the output/final file
        command.extend([
            '-vcodec', file_video_codec,                #
            '-preset', 'medium',                        # ???
            '-pix_fmt', file_pixel_format,              # Pixel format for the final file to write
            file_path])

        # Log the ffmpeg call we will make
        logger.debug(f"Calling ffmpeg to write video \"{' '.join(command)}\"")

        # Write all the video frame data to the PIPE's standard input
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stdin=subprocess.PIPE,  bufsize=10 ** 8)
        for frame in self.get_video_frames():
            process.stdin.write(frame.tobytes())

        process.stdin.close()
        process.wait()

        # Delete the audio temp  file we created as needed
        if audio_file_name:
            os.remove(audio_file_name)

        logger.info(f"Video written to '{file_path}'")