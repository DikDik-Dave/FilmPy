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
                 audio_frames=None,
                 clip_end_time=None,
                 clip_fps=None,
                 clip_start_time=0,
                 clip_width=None,
                 file_path=None,
                 clip_frames=None,
                 clip_height=None,
                 clip_include_audio=None,
                 clip_position=(0,0),
                 clip_pixel_format='yuv420p',
                 mask_frames=None,
                 mask_behavior=MaskBehavior.LOOP_FRAMES,
                 video_end_time=None,
                 video_fps=None,
                 video_frames=None
                 ):
        """
        Initialize this Clip

        :param clip_width:
        :param clip_height:
        :param clip_start_time:
        :param clip_end_time:
        :param video_fps:
        """
        # Ensure the clip pixel format is valid
        if clip_pixel_format not in PIXEL_FORMATS.keys():
            raise ValueError(f"'{clip_pixel_format}' is not a valid value for clip_pixel_format.")

        # Audio Specific Attributes
        self._audio_info = {}               # Audio metadata
        self._audio_frames = audio_frames   # Primary Audio Frame Data

        # Clip specific attributes
        self._clip_audio = None                                         # The audio data of the clip itself
        self._clip_frames = [] if not clip_frames else clip_frames      # The frames of the clip itself
        self._clip_info = {'end_time': clip_end_time,                   # End time in seconds
                           'fps': clip_fps,                             # Frames per second for the clip
                           'height': None,                              # Height (in pixels) of the clip
                           'include_audio': clip_include_audio,         # Should the audio be included when rendered
                           'number_frames': None,                       # Number of video frames in the clip
                           'position_x': int(clip_position[0]),         # x coordindate for the clip
                           'position_y': int(clip_position[1]),         # y coordinate for the clip
                           'pixel_format': clip_pixel_format,           # Pixel Format
                           'resolution': None,                          # Resolution string '{width}x{height}'
                           'start_time': clip_start_time,               # Start time in seconds
                           'width': None,                               # Width (in pixels) of the clip
                           }

        # Video specific attributes
        self._video_info = {'end_time': video_end_time,
                            'height': clip_height,
                            'width': clip_width,
                            'fps': video_fps,
                            'resolution': f"{clip_width}x{clip_height}"}    # Video metadata
        self._video_frames = [] if not video_frames else video_frames       # Frames that make up the video

        # File specific attributes
        self._file_path = file_path  # Path to whatever file is associated to this clip

        # Mask specific attributes
        self._mask = {'frames':mask_frames, 'behavior': mask_behavior, 'initialized': False}
        if isinstance(self._mask['behavior'], Enum):
            self._mask['behavior'] = self._mask['behavior'].value


    ####################
    # Expected Methods #
    ####################
    def get_video_frames(self):
        """
        Get the video frame data associated to this clip
        Note, This IS NOT the same as the frames that comprise the clip, and once set is not (meant to be) mutable

        :return: array of RGB frame data
        """
        raise NotImplementedError(f"{type(self).__name__}.get_video_frames has not been implemented")

    ############################
    # Property Methods - Audio #
    ############################
    @property
    def audio_channels(self):
        """
        Number of audio channels for the audio
        :return:
        """
        return self._audio_info['channels']

    @audio_channels.setter
    def audio_channels(self, value):
        """
        set the number of audio channels
        :param value:
        :return:
        """
        self._audio_info['channels'] = int(value)

    @property
    def audio_sample_rate(self):
        """
        Audio Sample Rate for the audio
        :return:
        """
        return self._audio_info['sample_rate']

    ######################################
    # Property Methods - Clip Attributes #
    ######################################
    @property
    def end_time(self):
        """
        End time of the clip in seconds
        """
        # If the end time for the clip has already been set, return it
        if self._clip_info['end_time']:
            return self._clip_info['end_time']

        # Default the end_time of the clip to the video end time
        self.end_time = self.video_end_time

        # Return the end time of the clip
        return self._clip_info['end_time']

    @end_time.setter
    def end_time(self, value):
        """
        Set the end time for the clip

        :param value: End time of the clip in seconds
        """
        self._clip_info['end_time'] = float(value)

    @property
    def fps(self):
        """
        Frames per second of the clip itself
        """
        # If frames per second is already set, return it
        if self._clip_info['fps']:
            return self._clip_info['fps']

        # Default it to video frames per second
        self._clip_info['fps'] = self.video_fps

        # return frames per second
        return self._clip_info['fps']

    @fps.setter
    def fps(self, value):
        """
        Set frames per second for the clip itself
        :param value:
        """
        self._clip_info['fps'] = float(fps)

    @property
    def has_audio(self):
        """
        Checks if the clip in question has audio data

        :return: True if the clip has audio data, False otherwise
        """
        return bool(self._audio_info)

    @property
    def height(self) -> int:
        """
        Height of the clip itself, will default to video_height if not set

        :return height: height of the clip
        """
        # If height has already been set, return it
        if ('height' in self._clip_info) and self._clip_info['height']:
            return self._clip_info['height']

        # Default height to the video's height
        self._clip_info['height'] = self.video_height

        # Return height
        return self._clip_info['height']

    @height.setter
    def height(self, value):
        """
        Set the height of the clip itself

        :param value: height value
        """
        self._clip_info['height'] = int(value)

    @property
    def number_frames(self) -> int:
        """
        Number of frames in the clip
        """
        if self._clip_info['number_frames']:
            return self._clip_info['number_frames']

        # Default to number of frames in the video
        self._clip_info['number_frames'] = self.video_number_frames

        # Return the number of frames
        return self._clip_info['number_frames']


    @number_frames.setter
    def number_frames(self, value):
        """
        Set the number of frames of the clip itself
        :param value:
        :return:
        """
        self._clip_info['number_frames'] = int(value)

    @property
    def pixel_format(self):
        """
        Pixel format of the clip itself
        """
        return self._clip_info['pixel_format']

    @property
    def position(self) -> tuple:
        """
        (x,y) coordinates for the clip (only used if the clip is composited)
        """
        return (self._clip_info['position_x'], self._clip_info['position_y'])

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
        if self._clip_info['resolution']:
            return self._clip_info['resolution']

        self._clip_info['resolution'] = f"{self.width}x{self.height}"
        return self._clip_info['resolution']

    @property
    def start_time(self):
        """
        Retrieves the start time of the clip

        :return: start time of the clip in seconds
        """
        return self._clip_info['start_time']

    @start_time.setter
    def start_time(self, value):
        """
        Set the start time for the clip

        :param value: Value of start time in seconds, must be able to be casted into a float
        """
        self._clip_info['start_time'] = float(start_time)

    @property
    def width(self) -> int | None:
        """
        Width of the clip itself
        :return:
        """
        # If width has already been set, return it
        if ('width' in self._clip_info) and self._clip_info['width']:
            return self._clip_info['width']

        # Default width if not set to the video's width
        self._clip_info['width'] = self.video_width

        # Update the clip's resolution
        self._clip_info['resolution'] = f"{self._clip_info['width']}x{self._clip_info['height']}"
        return self._clip_info['width']

    @width.setter
    def width(self, value):
        """
        Set the width of the clip itself
        :param value:
        :return:
        """
        self._clip_info['width'] = int(value)
        self._clip_info['resolution'] = f"{self._clip_info['width']}x{self._clip_info['height']}"

    @property
    def x(self):
        """
        x coordinate of the clip itself
        """
        return self._clip_info['position_x']

    @x.setter
    def x(self, value):
        """
        Set the x coordinate
        :param value:
        """
        self._clip_info['position_x'] = int(value)

    @property
    def y(self):
        """
        y coordinate of the clip itself
        """
        return self._clip_info['position_x']

    @y.setter
    def y(self, value):
        """
        Set the y coordinate
        :param value:
        """
        self._clip_info['position_y'] = int(value)

    #######################################
    # Property Methods - Video Attributes #
    #######################################
    @property
    def video_height(self) -> int:
        """
        Height of the underlying video associated to this clip

        :raises ValueError: Video info has no height attribute
        """
        if 'height' not in self._video_info:
            raise ValueError(f'{type(self).__name__}.video_height cannot be None.')
        return self._video_info['height']

    @property
    def video_number_frames(self) -> int:
        """
        Number of frames in the underlying video associated to this clip

        :raises ValueError:  Number of video frames is None (which should never be true)
        """
        # Ensure we have a valid value
        if ('number_frames' not in self._video_info) or (self._video_info['number_frames'] is None):
            raise ValueError(f'{type(self).__name__}.video_number_frames has not been set.')

        return self._video_info['number_frames']

    @property
    def video_pixel_format(self) -> str:
        """
        Pixel format of the underlying video
        """
        return self._video_info['pix_fmt']

    @property
    def video_width(self) -> int:
        """
        Width of the underlying video associated to this clip

        :raises ValueError: Video info has no width attribute
        """
        if 'width' not in self._video_info:
            raise ValueError(f'{type(self).__name__}.video_width cannot be None.')
        return self._video_info['width']

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
        return self._video_info['duration']

    @property
    def video_end_time(self):
        """
        End time of the video itself
        """
        # Has end time for the video already been set, if so return it
        if self._video_info['end_time']:
            return self._video_info['end_time']

        # Default to video duration
        self.video_end_time = self.video_duration

        # Return the video duration
        return self._video_info['end_time']

    @video_end_time.setter
    def video_end_time(self, value):
        """
        Set the video_end_time attribute
        """
        self._video_info['end_time'] = float(value)

    @property
    def video_fps(self):
        """
        Frames per second of the associated video
        :returns:
            int - Frames per second for the video
        """
        return self._video_info['fps']

    @video_fps.setter
    def video_fps(self, fps):
        """
        Set video_fps
        :param fps:
        :return:
        """
        if not isinstance(fps, (int,float)):
            raise TypeError(f"{type(self).__name__}.video_fps must be an integer or a float")
        self._video_info['fps'] = fps

    @property
    def video_resolution(self) -> str:
        if 'resolution' not in self._video_info:
            raise TypeError(f'{type(self).__name__}.video_resolution is None.')
        return self._video_info['resolution']

    @property
    def include_audio(self):
        """
        Should the audio of this clip be included
        :return:
        """
        if self._clip_info['include_audio'] is None:
            raise ValueError(f'{type(self).__name__}.include_audio cannot be None.')
        return self._clip_info['include_audio']

    ###################
    # Private Methods #
    ###################
    @staticmethod
    def _to_radians(angle) -> float:
        """

        :param angle: Angle in degrees
        :return:
        """
        return angle * (np.pi / 180)

    ##################
    # Public Methods #
    ##################
    def audio_fade_in(self, duration, algorithm=Fade.LINEAR):
        """
        Apply a fade in to the audio track

        :param algorithm: Type of audio fade in to implement,
        :param duration: Duration, in seconds, that the fade in will last for
        :return self: This object, to allow for method chaining
        """
        # Get the audio frames
        audio_frames = self.get_audio_frames(self.file_path)

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

        :param algorithm: Type of audio fade in to implement,
        :param duration: Duration, in seconds, that the fade in will last for

        :return self: This object, to allow for method chaining
        """

        # Get the audio frames
        audio_frames = self.get_audio_frames(self.file_path)

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


    def audio_normalize(self):
        """
        Normalize the audio track volume
        :return self: This object, to allow for method chaining
        """

        #TODO: Implement the normalization

        # Allows for method chaining
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
        audio_frames = self.get_audio_frames(self.file_path, number_channels=self.audio_channels)
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
        audio_frames = self.get_audio_frames(self.file_path, number_channels=self.audio_channels) * multiplier
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
        last_frame = None
        for frame in self.get_frames():
            last_frame = frame
            new_frame = np.concatenate((top_row, frame, bottom_row), axis=0) # Concatenate Rows
            new_frame = np.concatenate((left_column, new_frame, right_column), axis=1)
            altered_frames.append(new_frame.astype('uint8')) # Concatenate Columns

        # Set the new frame shape
        self.height = new_frame.shape[0]
        self.width = new_frame.shape[1]

        # Set the new frames for this video
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

    def get_audio_frames(self,
                         file_name,
                         fps=44100,
                         number_bytes=2,
                         number_channels=2):
        """
        Get audio data from an audio or video file
        :param file_name: File containing audio to retrieve

        :param fps:
        :param number_bytes:
        :param number_channels:
        :return:
        """
        if self._audio_frames is not None:
            return self._audio_frames

        ffmpeg_command = [FFMPEG_BINARY,
                          '-i', file_name, '-vn',
                          '-loglevel', 'error',
                          '-f', 's%dle' % (8 * number_bytes),
                          '-acodec', 'pcm_s%dle' % (8 * number_bytes),
                          '-ar', '%d' % fps,
                          '-ac', '%d' % number_channels,
                          '-'
                          ]

        completed_process = subprocess.run(ffmpeg_command, capture_output=True)

        # return completed_process.stdout
        dt = {1: 'int8', 2: 'int16', 4: 'int32'}[number_bytes]
        self._audio_frames = np.fromstring(completed_process.stdout, dtype=dt).reshape(-1, number_channels)
        return self._audio_frames

    def get_mask_frames(self):
        """
        Get the
        :return:
        """

        # Previously initialized frames have been created, so return them
        if self._mask['initialized']:
            return self._mask['frames']

        # No mask exists, so we need to create one
        if not self._mask['frames']:
            self._mask['frames'] = [np.tile((True,True,True), self.width * self.height).reshape(self.height, self.width, 3)]

        # If mask behavior is to loop, then create all the mask frames we need, and replace the mask frames we had
        if self._mask['behavior'] == MaskBehavior.LOOP_FRAMES.value:
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
        Get the video frames for this clip
        :return:
        """
        # Return the already created frames
        if self._clip_frames:
            return self._clip_frames

        # No frames yet exist, copy the video data
        # TODO: respect clip start, end, etc
        self._clip_frames = self.get_video_frames()

        return self._clip_frames

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
            image = Image.fromarray(frame).transpose(Transpose.FLIP_LEFT_RIGHT)
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
            image = Image.fromarray(frame).transpose(Transpose.FLIP_TOP_BOTTOM)
            flipped_frames.append(np.array(image))

        # Replace the clip frames with the now rotated frames
        self.set_frames(flipped_frames)

        # Return this object to enable method chaining
        return self


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
            msg = f"Either frame_index or frame_time must be provided to {type(self).__name__}.write_image()"
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

    def resize(self, *args, **kwargs):
        """
        Resize the video frames for the clip
        :param: multiplier: Resizing multiplier
        :param resample: Which resampling method to use during resizing (Defaults to BICUBIC)
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

    def write_image(self, file_path, frame_index:int=None, frame_time:int=None) -> bool:
        """
        Write a single frame out as an image file
        :return: True, if successful
        """
        # Ensure we have valid input
        if (frame_index is None) and (frame_time is None):
            msg = f"Either frame_index or frame_time must be provided to {type(self).__name__}.write_image()"
            raise ValueError(msg)
        if frame_index and frame_time:
            msg = f"Both frame_index and frame_time cannot be simultaneously be specified. "
            raise ValueError(msg)

        frame = self.get_video_frame(frame_index=frame_index, frame_time=frame_time)
        pixel_format = 'rgb24'
        command = [FFMPEG_BINARY,
                   "-y",
                   "-s", self.video_resolution,
                   '-f','rawvideo',
                   '-pix_fmt', pixel_format,
                   '-i', '-',
                   file_path
                   ]


        # Call ffmpeg, and pip the data to the subprocess
        process = subprocess.Popen(command, stdout=DEVNULL, stdin=PIPE)
        _, process_error = process.communicate(frame.tobytes())
        if process.returncode:
            raise IOError(process_error)

        # Delete the process
        del process

        # File was successfully created
        return True

    def set_audio_frames(self, value):
        """
        Set the audio data for this clip
        :return:
        """
        if not isinstance(value, np.ndarray):
            raise ValueError(f"{type(self).__name__}.audio_data must be an numpy array")

        self._audio_frames = value.astype(np.int16)

    def set_frames(self, value):
        """
        Set the new clip frames
        """
        if not isinstance(value, list):
            raise ValueError(f"{type(self).__name__}.clip_frames must be a list of numpy.array objects")

        self._clip_frames = value

    def write_video_file(self,
                         file_path,
                         write_audio=True,
                         audio_codec=None,
                         file_video_codec=None):
        """
        Writes this clip to a video file

        :param file_path: Output video's path
        :param write_audio: Boolean, should we write the audio as well as the video. Defaults to True.
        :param audio_codec: Audio Codec to use
        :param file_video_codec: Video Codec to use when writing the file
        """
        logger = getLogger()
        print(__name__.split('.')[0])
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
                   '-y',  # Overwrite output file if it exists
                   '-f', 'rawvideo',                        # Indicates ??
                   '-vcodec', 'rawvideo',                   # Video Codec
                   '-s', self.resolution,                   # size of one frame
                   '-pix_fmt', 'rgb24',                     # pixel format
                   '-r', '%d' % self.fps,                   # frames per second
                   '-i', '-',                               # the input comes from a pipe
                   '-an']                                   # tells FFMPEG not to expect any audio

        # If we have an audio stream and we are to write audio
        if self._audio_info and write_audio:
            # TODO: Pull this data from audio_stream or somewhere...
            # Audio Info
            fps = 44100
            number_channels = self.audio_channels
            number_bytes = 2
            temp_audio_file_name = f"{file_name}_wvf_snd.tmp.{audio_extension}"
            audio_data = self.get_audio_frames(self._file_path, fps, number_bytes, number_channels)

            # FFMPEG Command to write audio to a file
            ffmpeg_command = [
                FFMPEG_BINARY, '-y',
                '-loglevel', 'error',
                "-f", 's%dle' % (8 * number_bytes),
                "-acodec", 'pcm_s%dle' % (8 * number_bytes),
                '-ar', "%d" % fps,
                '-ac', "%d" % number_channels,
                '-i', '-',
                temp_audio_file_name]

            # Write all the data (via ffmpeg) to the temp file
            process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, bufsize=10 ** 8)
            process.stdin.write(audio_data.tobytes())
            process.stdin.close()
            process.wait()

            # Extend the command to pass in the audio we just recorded
            command.extend([
                '-i', temp_audio_file_name,
                '-acodec', 'copy'
            ])

        # Parameters relating to the output/final file
        command.extend([
            '-vcodec', file_video_codec,
            '-preset', 'medium',
            '-pix_fmt', self.pixel_format,
            file_path])
        print(command)
        # Write all the video frame data to the PIPE's standard input
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stdin=subprocess.PIPE,  bufsize=10 ** 8)
        for frame in self.get_frames():
            process.stdin.write(frame.tobytes())
        process.stdin.close()
        process.wait()