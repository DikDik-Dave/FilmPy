import subprocess
import os
from subprocess import DEVNULL, PIPE

import PIL.Image
from PIL import Image
from .constants import AUDIO_CODECS, FFMPEG_BINARY, VIDEO_CODECS, Transpose
import numpy as np

class Clip:
    """
    Base class for all clips.
    """

    def __init__(self,
                 audio_frames=None,
                 fps=None,
                 file_path=None,
                 frames=None,
                 end_time=None,
                 width=None,
                 height=None,
                 start_time=0,
                 video_fps=None,
                 video_frames=None,
                 include_audio=None):
        """
        Initialize this Clip

        :param width:
        :param height:
        :param start_time:
        :param end_time:
        :param video_fps:
        """

        # Audio Specific Attributes
        self._audio_info = {}         # Audio metadata
        self._audio_frames = audio_frames # Primary Audio Frame Data

        # Clip specific attributes
        self._clip_audio = None
        self._clip_video = [] if not frames else frames        # The frames of the clip itself
        self._clip_end = end_time                               # End time in seconds
        self._clip_start = start_time                           # Start time in seconds
        self._clip_fps = fps                               # Frames per second for the clip

        # Video specific attributes
        self._video_info = {'height': height,
                            'width': width,
                            'fps': video_fps,
                            'resolution': f"{width}x{height}"}  # Video metadata
        self._video_frames = [] if not video_frames else video_frames       # Frames that make up the video

        # File specific attributes
        self._file_path = file_path  # Path to whatever file is associated to this clip

        # Should the audio data be written for this clip
        self._include_audio = include_audio

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

    ####################
    # Property Methods #
    ####################
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
    def end_time(self):
        """
        End time of the clip
        :return : end time of the clip in seconds
        """
        return self._clip_end

    @end_time.setter
    def end_time(self, end_time):
        """
        Set the end time for the clip

        :param end_time: End time of the clip in seconds
        """
        self._clip_end = end_time

    @property
    def has_audio(self):
        """
        Checks if the clip in question has audio data

        :return: True if the clip has audio data, False otherwise
        """
        return bool(self._audio_info)

    @property
    def start_time(self):
        """
        Retrieves the start time of the clip
        :return: start time of the clip in seconds
        """
        return self._clip_start

    @start_time.setter
    def start_time(self, start_time):
        """
        Set the start time for the clip
        :param start_time:
        """
        self._clip_start = start_time

    @property
    def video_height(self):
        if 'height' not in self._video_info:
            raise TypeError(f'{type(self).__name__}.video_frame_height is None.')
        return self._video_info['height']


    @property
    def video_width(self):
        if 'width' not in self._video_info:
            return TypeError(f'{type(self).__name__}.video_frame_width is None')
        return self._video_info['width']

    @property
    def write_audio(self):
        if self._include_audio is None:
            raise TypeError(f'{type(self).__name__}.write_audio is None.')
        return self._include_audio

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

    def get_frames(self):
        """
        Get the video frames for this clip
        :return:
        """
        # Return the already created frames
        if self._clip_video:
            return self._clip_video

        # No frames yet exist, copy the video data
        # TODO: respect clip start, end, etc
        self._clip_video = self.get_video_frames()

        return self._clip_video

    def multiply_stereo_volume(self, left_multiplier:float, right_multiplier:float):
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

    def multiply_volume(self, multiplier:float) -> object:
        """

        :param multiplier: f
        :return:
        """
        # Make sure the clip in question has audio
        if not self.has_audio:
            raise AttributeError(f"{type(self).__name__} does not have associated audio.")


        # Set the new audio data
        audio_frames = self.get_audio_frames(self.file_path, number_channels=self.audio_channels) * multiplier
        self.set_audio_frames(audio_frames.astype(np.int16))

        # Return this object to enable method chaining
        return self

    def mirror_x(self):
        """
        Flips the clip frames left to right

        :return self: Enable method chaining
        """
        flipped_frames = []
        for frame in self.get_frames():
            image = Image.fromarray(frame).transpose(PIL.Image.Transpose.FLIP_LEFT_RIGHT)
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
            image = Image.fromarray(frame).transpose(PIL.Image.Transpose.FLIP_TOP_BOTTOM)
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
        self._audio_frames = value

    def set_frames(self, value):
        """
        Set the new clip frames
        """
        if not isinstance(value, list):
            raise ValueError(f"{type(self).__name__}.clip_frames must be a list of numpy.array objects")

        self._clip_video = value

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
                   '-f', 'rawvideo',  #
                   '-vcodec', 'rawvideo',  #
                   '-s', self._video_info['resolution'],  # size of one frame
                   '-pix_fmt', 'rgb24',  # pixel format
                   '-r', '%d' % self.video_fps,  # frames per second
                   '-i', '-',  # the input comes from a pipe
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
            '-pix_fmt', self._video_info['pix_fmt'],
            file_path])

        # Write all the video frame data to the PIPE's standard input
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stdin=subprocess.PIPE,  bufsize=10 ** 8)
        for frame in self.get_frames():
            process.stdin.write(frame.tobytes())
        process.stdin.close()
        process.wait()