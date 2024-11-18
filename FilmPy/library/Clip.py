from pydoc import classname
import subprocess
import os
from FilmPy.library.constants import AUDIO_CODECS, FFMPEG_BINARY, VIDEO_CODECS


class Clip:
    """
    Base class for all clips.
    """

    def __init__(self,
                 clip_fps=None,
                 end_time=None,
                 frame_width=None,
                 frame_height=None,
                 start_time=0,
                 video_fps=None,
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
        self._clip_end = end_time       # End time in seconds
        self._clip_start = start_time   # Start time in seconds
        self._clip_frames = []          # Frames for the whole clip
        self._clip_fps = clip_fps       # Frames per second for the clip

        # Video specific attributes
        self._video_info = {'height': frame_height, 'width': frame_width, 'fps': video_fps} # Video metadata
        #TODO: Remove references to _video_frame_* and use _video_info
        self._video_frame_height = frame_height
        self._video_frame_width = frame_width

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
        raise NotImplementedError(f"{classname(self)}._get_audio_data() has not been implemented. Bad Developer.")

    def get_video_frames(self):
        """
        Get the video frame data associated to this clip

        :return: array of RGB frame data
        """
        raise NotImplementedError(f"{classname(self)}.get_video_frames has not been implemented")

    ####################
    # Property Methods #
    ####################
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

    @property
    def video_frame_height(self):
        if 'height' not in self._video_info:
            raise TypeError(f'{classname(self)}.video_frame_height is None.')
        return self._video_info['height']


    @property
    def video_frame_width(self):
        return self._video_frame_width

    @property
    def write_audio(self):
        if self._include_audio is None:
            raise TypeError(f'{classname(self)}.write_audio is None.')
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

        :returns
            None, If there is no video file associated to the clip
            str, Video file path
        """
        return self._video_file_path

    ##################
    # Public Methods #
    ##################
    def set_start_time(self, start_time):
        """
        Set the start time for the clip
        :param start_time:
        """
        self._clip_start = start_time

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