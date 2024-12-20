import subprocess
import os
from logging import getLogger
from subprocess import DEVNULL, PIPE

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
                 audio_nb_frames=None,
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
                 clip_frames=None,
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
        :param clip_frames:
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
                        'frames': audio_frames,
                        'number_frames': audio_nb_frames,
                        'r_frame_rate': audio_r_frame_rate,
                        'sample_format': audio_sample_fmt,
                        'start_pts': audio_start_pts,
                        'start_time': audio_start_time,
                        'time_base': audio_time_base,
                        }
        if audio_sample_rate:
            self.audio_sample_rate = audio_sample_rate

        # Clip specific attributes
        clip_frames = [] if not clip_frames is None else clip_frames      # The frames of the clip itself
        self._clip = {
                           'behavior': clip_behavior,
                           'end_time': clip_end_time,                     # End time of the clip itself
                           'fps': clip_fps,                               # Frames per second for the clip
                           'frames': clip_frames,                         # Frames that comprise the clip
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
        video_frames = [] if not video_frames else video_frames         # Frames that make up the video
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
                            'disposition': video_disposition,
                            'duration': video_duration,
                            'duration_ts': video_duration_ts,
                            'end_time': video_end_time,                 # Duration of the video
                            'fps': video_fps,                           # FPS for the underlying video
                            'frames': video_frames,                     # Frames for the underlying video
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
    def audio_sample_rate(self) -> int:
        """
        Audio Sample Rate for the audio
        :return:
        """
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

    ######################################
    # Property Methods - Clip Attributes #
    ######################################
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
        return bool(self._audio)

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
    def video_pixel_format(self) -> str:
        """
        Pixel format of the underlying video
        """
        return self._video['pix_fmt']

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
        ffmpeg_command = [
            FFMPEG_BINARY, '-y',
            '-loglevel', ffmpeg_log_level,                          # Set ffmpeg's log level accordingly
            "-f", 's%dle' % (8 * self.audio_channels),
            "-acodec", 'pcm_s%dle' % (8 * self.audio_channels),
            '-ar', "%d" % self.audio_sample_rate,
            '-ac', "%d" % self.audio_channels,
            '-i', '-',
            file_path]

        # Log the ffmpeg call we will make
        logger.debug(f"Calling ffmpeg to write audio \"{' '.join(ffmpeg_command)}\"")

        # Write all the data (via ffmpeg) to the temp file
        process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, bufsize=10 ** 8)
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

        :param red_addend: Addend for the red channel
        :param green_addend: Addend for the green channel
        :param blue_addend: Addend for blue channel
        :param luminance: Addend for luminance
        :return:
        """
        logger = getLogger(__name__)

        # If all the multipliers are 1, we have no work to do
        if red_addend == green_addend == blue_addend == luminance == 0:
            logger.warning(f"All multipliers, set to 1. No work needed.")
            return self

        # Add colors in each frame
        logger.debug(f"Color Addends - Red x {red_addend}, Green x {green_addend}, "
                     f"Blue x {blue_addend}, Luminance={luminance}")
        altered_frames = []
        luminance_array = np.array([luminance, luminance, luminance])
        red_addend_array = np.array([red_addend, green_addend, blue_addend])
        for frame in self.get_frames():
            altered_frames.append((frame + red_addend_array + luminance_array).astype('uint8'))

        # Replace the existing frames
        self.set_frames(altered_frames)

        # Return this object to enable method chaining
        return self

    # TODO: add audio_fade_in(,algorithm=Fade.LINEAR) parameter
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
        for frame in self.get_frames():
            image = Image.fromarray(frame).convert(ImageModes.BLACK_AND_WHITE.value)
            frame = np.stack((np.array(image), np.array(image), np.array(image)), axis=2).astype('uint8')
            altered_frames.append(frame)

        # Replace the clip frames with the now rotated frames
        self.set_frames(altered_frames)

        # Return this object to enable method chaining
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
        for frame in self.get_frames():
            new_frame = np.concatenate((top_row, frame, bottom_row), axis=0)           # Concatenate Rows
            new_frame = np.concatenate((left_column, new_frame, right_column), axis=1) # Concatenate Columns
            altered_frames.append(new_frame.astype('uint8')) # Add to our list of altered frames

        # Set the new frame shape
        self.height = new_frame.shape[0]
        self.width = new_frame.shape[1]

        # Set the new frames for this video
        self.set_frames(altered_frames)

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
        for frame in self.get_frames():
            image = Image.fromarray(frame)

            # Resize smoothly down
            image_small = image.resize((pixel_size, pixel_size), resample=Image.Resampling.BILINEAR)

            # Scale back up using NEAREST to original size, and add it to the altered frames
            altered_frames.append(np.array(image_small.resize(self.size, Image.Resampling.NEAREST)))

        # Update clip frames
        self.set_frames(altered_frames)

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
        frames = self.get_frames()

        # Crop the frames
        logger.debug(f"Cropping image from ({top_left_x},{top_left_y}) to ({bottom_right_x},{bottom_right_y})")
        cropped_frames = []
        for frame in frames:
            cropped_frame = frame[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
            cropped_frames.append(cropped_frame)

        logger.debug(f"{len(cropped_frames)} frames cropped")

        # Replace the frames with the new frames
        self.set_frames(cropped_frames)

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
            frames = self.get_frames()

            # Determine the cut frame indices
            start_index = int(self.fps * start_time)
            end_index = int(self.fps * end_time)

            # Cut out the frames of the clip we don't want
            frames = frames[0:start_index] + frames[end_index:]

            # Update the clip attributes
            self.set_frames(frames)
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
        for frame in self.get_frames():
            altered_frames.append((frame / (red_divisor, green_divisor, blue_divisor) / luminance_array).astype('uint8'))

        # Replace the existing frames
        self.set_frames(altered_frames)

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
        for frame in self.get_frames():
            altered_frames.append((255 - frame).astype('uint8'))

        # Replace the existing frames
        self.set_frames(altered_frames)

        # Return this object to enable method chaining
        return self

    def fade_in(self,
                duration,
                fade_in_color=(0,0,0)):
        """
        Fade in from fade in color to the footage over the duration color

        :param duration:
        :param fade_in_color:
        """
        pass

    def fade_out(self,
                 duration,
                 fade_out_color=(0,0,0)):
        """
        Fade out from the footage to the fade out color over the duration
        :param duration:
        :param fade_out_color:
        :return:
        """
        pass

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
        for frame in self.get_frames():
            new_frame = (255 * (1.0 * frame / 255) ** gamma).astype('uint8')
            altered_frames.append(new_frame)

        self.set_frames(altered_frames)
        logger.info(f"Finished gamma correcting footage (gamma='{gamma}')")

        # Enable method chaining
        return self

    def get_audio_frames(self):
        """
        Get audio data from an audio or video file

        :return:
        """
        logger = getLogger(__name__)

        # self._file_path, fps, number_bytes, number_channels
        if self._audio['frames'] is not None:
            return self._audio['frames']

        ffmpeg_command = [FFMPEG_BINARY,
                          '-i', self.file_path, '-vn',
                          '-loglevel', 'error',
                          '-f', 's%dle' % (8 * self.audio_channels),
                          '-acodec', 'pcm_s%dle' % (8 * self.audio_channels),
                          '-ar', '%d' % self.audio_sample_rate,
                          '-ac', '%d' % self.audio_channels,
                          '-'
                          ]

        logger.debug(f"Calling ffmpeg to get audio \"{' '.join(ffmpeg_command)}\"")
        completed_process = subprocess.run(ffmpeg_command, capture_output=True)

        # return completed_process.stdout
        dt = {1: 'int8', 2: 'int16', 4: 'int32'}[self.audio_channels]
        self._audio['frames'] = np.fromstring(completed_process.stdout, dtype=dt).reshape(-1, self.audio_channels)
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

    def get_frames(self):
        """
        Get the video frames list for this clip
        :return:
        """
        # logger = getLogger(__name__)
        # logger.debug("Getting frames")
        # Return the already created frames
        if self._clip['frames']:
            return self._clip['frames']

        # No frames yet exist, default to using the video frames we have
        video_frames = self.get_video_frames()

        # Determine how many frames we need
        frames_needed = self.end_frame - self.start_frame

        # We need more frames than we have, and we are to enforce the limit
        if (frames_needed > self.video_number_frames) and self.behavior == Behavior.ENFORCE_LIMIT.value:
            raise ValueError(f"Frames needed ({frames_needed}) exceeds the available "
                             f"number of video frames ({self.video_number_frames})")

        # We need fewer frames than we have
        if frames_needed <= self.video_number_frames:
            self.set_frames(video_frames[self.start_frame:self.end_frame])
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

            self.set_frames(looped_frames)
        # Need to pad the footage
        elif self.behavior == Behavior.PAD.value:
            color = (77, 128, 90)
            number_pad_frames = frames_needed - self.video_number_frames
            pad_frame = (np.tile(color, self.width * self.height)
                          .reshape(self.height, self.width, 3)
                          .astype('uint8'))

            video_frames.extend([pad_frame] * number_pad_frames)
            self.set_frames(video_frames)

        # Return the frames
        return self._clip['frames']

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
        frames = self.get_frames()

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

    def get_video_frames(self):
        """
        Get the underlying video frames

        :return: List frames from the underlying video
        """
        return self._video['frames']

    def grayscale(self):
        """
        Converts the video to grayscale

        :return self: Enables method chaining
        """
        altered_frames = []
        for frame in self.get_frames():
            image = Image.fromarray(frame).convert(ImageModes.GRAYSCALE.value)
            frame = np.stack((np.array(image), np.array(image), np.array(image)), axis=2).astype('uint8')
            altered_frames.append(frame)

        # Replace the clip frames with the now rotated frames
        self.set_frames(altered_frames)

        # Return this object to enable method chaining
        return self

    def mirror_x(self):
        """
        Flips the clip frames left to right

        :return self: Enable method chaining
        """
        flipped_frames = []
        for frame in self.get_frames():
            image = Image.fromarray(frame).transpose(Transpose.FLIP_LEFT_RIGHT.value)
            flipped_frames.append(np.array(image))

        # Replace the clip frames with the now rotated frames
        self.set_frames(flipped_frames)

        # Return this object to enable method chaining
        return self

    def mirror_y(self):
        """
        Flip the clip frames top to bottom

        :return self: Enable method chaining
        """
        flipped_frames = []
        for frame in self.get_frames():
            image = Image.fromarray(frame).transpose(Transpose.FLIP_TOP_BOTTOM.value)
            flipped_frames.append(np.array(image))

        # Replace the clip frames with the now rotated frames
        self.set_frames(flipped_frames)

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
        for frame in self.get_frames():
            altered_frames.append((frame * (red_multiplier, green_multiplier, blue_multiplier) * luminance_array).astype('uint8'))

        # Replace the existing frames
        self.set_frames(altered_frames)

        # Return this object to enable method chaining
        return self

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
        for frame in self.get_frames():
            image = Image.fromarray(frame).resize((new_width, new_height), kwargs['resample'])
            altered_frames.append(np.array(image).astype('uint8'))

        # Adjust the size of the clip
        self.height = new_height
        self.width = new_width

        # Set the new frames for this video
        self.set_frames(altered_frames)

        # Return this object to enable method chaining
        return self

    def reverse_time(self):
        """
        Reverse the video frames for the clip
        :return self: (to enable method chaining)
        """

        # Reverse the footage
        self.set_frames(self.get_frames()[::-1])

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
        for frame in self.get_frames():
            image = Image.fromarray(frame).rotate(angle)
            rotated_frames.append(np.array(image))

        # Replace the clip frames with the now rotated frames
        self.set_frames(rotated_frames)

        # Return this object to enable method chaining
        return self

    def set_audio_frames(self, value):
        """
        Set the audio data for this clip
        :return:
        """
        if not isinstance(value, np.ndarray):
            raise ValueError(f"{type(self).__name__}.audio_data must be an numpy array")

        self._audio['frames'] = value.astype(np.int16)

    def set_frames(self, value):
        """
        Set the new clip frames
        """
        if not isinstance(value, list):
            raise ValueError(f"{type(self).__name__}.clip_frames must be a list of numpy.array objects")

        self._clip['frames'] = value

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
            self.set_frames(self.get_frames())

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

        command = [FFMPEG_BINARY,
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
        command = [FFMPEG_BINARY,
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
        logger.debug(f"ffmpeg command \"{' '.join(command)}\"")

        # Write all the video frame data to the PIPE's standard input
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stdin=subprocess.PIPE,  bufsize=10 ** 8)
        for frame in self.get_frames():
            process.stdin.write(frame.tobytes())

        process.stdin.close()
        process.wait()

        # Delete the audio temp  file we created as needed
        if audio_file_name:
            os.remove(audio_file_name)

        logger.info(f"Video written to '{file_path}'")