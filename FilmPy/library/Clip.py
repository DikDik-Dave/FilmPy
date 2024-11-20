import subprocess
import os
from subprocess import DEVNULL, PIPE
from PIL import Image
from FilmPy.library.constants import AUDIO_CODECS, FFMPEG_BINARY, VIDEO_CODECS
import numpy as np

class Clip:
    """
    Base class for all clips.
    """

    def __init__(self,
                 frames=None,
                 clip_fps=None,
                 end_time=None,
                 frame_width=None,
                 frame_height=None,
                 start_time=0,
                 video_fps=None,
                 video_frames=None,
                 include_audio=None):
        """
        Initialize this Clip

        :param frame_width:
        :param frame_height:
        :param start_time:
        :param end_time:
        :param video_fps:
        """

        # Audio Specific Attributes
        self._audio_info = {}   # Audio metadata
        self._audio_data = None # Primary Audio Data

        # Clip specific attributes
        self._clip_frames = frames      # The frames of the clip itself
        self._clip_end = end_time       # End time in seconds
        self._clip_start = start_time   # Start time in seconds
        self._clip_frames = []          # Frames for the whole clip
        self._clip_fps = clip_fps       # Frames per second for the clip

        # Video specific attributes
        self._video_info = {'height': frame_height,
                            'width': frame_width,
                            'fps': video_fps,
                            'resolution': f"{frame_width}x{frame_height}"} # Video metadata
        self._video_frames = video_frames

        # File specific attributes
        self._video_file_path = None



        # Should the audio data be written for this clip
        self._include_audio = include_audio

    ####################
    # Expected Methods #
    ####################
    def get_audio_data(self,
                       file_name,
                       fps = 44100,
                       number_bytes = 2,
                       number_channels = 2
                       ):
        """
        Gets the audio data associated to this clip
        :return:
        """
        raise NotImplementedError(f"{type(self).__name__}._get_audio_data() has not been implemented. Bad Developer.")

    def get_clip_frames(self):
        """
        Get the video frame data for this clip.
        This is either a condensed or looped and editable version of the frame data

        :return: An array of NPArray objects (RGB data)
        """
        raise NotImplementedError(f"{type(self).__name__}.get_video_frames has not been implemented")

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
    # @property
    # def clip_frames(self):
    #     """
    #     The frames that comprise this clip
    #     :return: [NPArray objects]
    #     """
    #     return self.get_clip_frames()


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
    def video_frame_height(self):
        if 'height' not in self._video_info:
            raise TypeError(f'{type(self).__name__}.video_frame_height is None.')
        return self._video_info['height']


    @property
    def video_frame_width(self):
        if 'width' not in self._video_info:
            return TypeError(f'{type(self).__name__}.video_frame_width is None')
        return self._video_info['width']

    @property
    def write_audio(self):
        if self._include_audio is None:
            raise TypeError(f'{type(self).__name__}.write_audio is None.')
        return self._include_audio

    def set_end_time(self, end_time):
        """
        Set the end time for the clip

        :param end_time: End time of the clip in seconds
        """
        self._clip_end = end_time

    @property
    def video_file_path(self):
        """
        Path to the video file

        :returns:
            None - No video file is associated with this clip
            str - Path to the video file
        """
        return self._video_file_path

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
        frames = self.get_clip_frames()

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
        for frame in self.get_clip_frames():
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
        print(frame.shape)
        pixel_format = 'rgb24'
        command = [FFMPEG_BINARY,
                   "-y",
                   "-s", self.video_resolution,
                   '-f','rawvideo',
                   '-pix_fmt', pixel_format,
                   '-i', '-',
                   file_path
                   ]

        print(command)
        # Call ffmpeg, and pip the data to the subprocess
        process = subprocess.Popen(command, stdout=DEVNULL, stdin=PIPE)
        _, process_error = process.communicate(frame.tobytes())
        if process.returncode:
            raise IOError(process_error)

        # Delete the process
        del process

        # File was successfully created
        return True

    def set_frames(self, value):
        """
        Set the new clip frames
        """
        if not isinstance(value, list):
            raise ValueError(f"{type(self).__name__}.clip_frames must be a list of numpy.array objects")

        # TODO: Add check that all elements are np.array
        # if not all(isinstance(e, np.array) for e in value)):
        #     raise()
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
            number_channels = 2
            number_bytes = 2
            temp_audio_file_name = f"{file_name}_wvf_snd.tmp.{audio_extension}"
            audio_data = self.get_audio_data(self._video_file_path, fps, number_bytes, number_channels)

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
        for frame in self.get_video_frames():
            process.stdin.write(frame.tobytes())
        process.stdin.close()
        process.wait()