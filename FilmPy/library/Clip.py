from pydoc import classname
import subprocess
import os
from FilmPy.library.constants import AUDIO_CODECS, FFMPEG_BINARY, VIDEO_CODECS


class Clip:
    """
    Base class for all clips.
    """

    def __init__(self, frame_width, frame_height, start_time, end_time, video_fps):
        """
        Initialize this Clip

        :param start_time:
        :param end_time:
        :param video_fps: Video's frames per second
        """
        # Primary Audio Stream Attributes
        self._audio_stream = None

        # Primary Audio Data
        self._audio_data = None

        # Set the amount of frames per second
        self.video_fps = video_fps

        # When to start the clip
        self._start_time = start_time

        # When to end the clip
        self._end_time = end_time

        self._video_frame_height = frame_height

        # Width of a Single Frame
        self._video_frame_width = frame_width

        # The path to the video file in question
        self._video_file_path = None

        # Primary Video Stream information
        self._video_stream = None

        # RGB Frame Data
        self._video_frames = []


    def _get_audio_data(self,
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
        raise NotImplementedError(f"{classname(self)}.get_frames has not been implemented")


    ####################
    # Property Methods #
    ####################
    @property
    def video_frame_height(self):
        return self._video_frame_height

    @property
    def video_frame_width(self):
        return self._video_frame_width

    def set_end_time(self, end_time):
        """
        Set the end time for the clip

        :param end_time: End time of the clip in seconds
        :return:
        """
        self._end_time = end_time



    ##################
    # Public Methods #
    ##################
    def set_start_time(self, start_time):
        """
        Set the start time for the clip
        :param start_time:
        """
        self._start_time = start_time

    def start_time(self):
        """
        Retrieves the start time of the clip
        :return: start time of the clip in seconds
        """
        return self._start_time

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
                   '-y',                                    # Overwrite output file if it exists
                   '-f', 'rawvideo',                        #
                   '-vcodec', 'rawvideo',                   #
                   '-s', self._video_stream['resolution'],  # size of one frame
                   '-pix_fmt', 'rgb24',                     # pixel format
                   '-r', '%d' % self.video_fps,             # frames per second
                   '-i', '-',                               # the input comes from a pipe
                   '-an']                                   # tells FFMPEG not to expect any audio

        # If we have an audio stream and we are to write audio
        if self._audio_stream and write_audio:
            # TODO: Pull this data from audio_stream or somewhere...
            # Audio Info
            fps = 44100
            number_channels = 2
            number_bytes = 2
            temp_audio_file_name = f"{file_name}_wvf_snd.tmp.{audio_extension}"
            audio_data = self._get_audio_data(self._video_file_path, fps, number_bytes, number_channels)

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
            '-pix_fmt', self._video_stream['pix_fmt'],
            file_path])

        # Write all the video frame data to the PIPE's standard input
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stdin=subprocess.PIPE,  bufsize=10 ** 8)
        for frame in self.get_video_frames():
            process.stdin.write(frame.tobytes())
        process.stdin.close()
        process.wait()