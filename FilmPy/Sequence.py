import os
import subprocess
from FilmPy.constants import AUDIO_CODECS, FFMPEG_BINARY, VIDEO_CODECS

class Sequence:
    """
    Sequence of clips, aka the film
    """
    def __init__(self,
                 clips:list=None,
                 transitions:dict=None):
        """
        Creates a sequence of clips (aka concatenation)
        :param clips: Clips that comprise the sequence
        :param transitions: A dictionary (int -> Transition objects) of clip transitions.
        """
        if clips:
            self._clips = clips
        else:
            self._clips = []

        self.frame_width = 0

        self.frame_height = 0

        # Frames per second of the sequence
        self.fps = 0

        # Loop over the clips and determine the fps, and resolution for the sequence
        for clip in clips:
            if clip.video_fps > self.fps:
                self.fps = clip.video_fps

            if self.frame_width < clip.video_width:
                self.frame_width = clip.video_width

            if self.frame_height < clip.video_height:
                self.frame_height = clip.video_height
        self.frame_size = f"{self.frame_width}x{self.frame_height}"
    ##################
    # Public Methods #
    ##################
    def add_clip(self, clip, position=None):
        """
        Add a clip to this sequence

        :param clip: Clip to be added to the sequence
        :param position: Position to insert the clip into the sequence
        """
        if position:
            self._clips.insert(position, clip)
        else:
            self._clips.append(clip)


    def write_video_file(self,
                         file_path,
                         write_audio=True,
                         output_audio_codec=None,
                         output_video_codec=None):
        """
        Writes this clip to a video file

        :param file_path: Output video's file path
        :param write_audio: Should we write the audio as well as the video? Default is True.
        :param output_audio_codec: Audio Codec to use when writing the file
        :param output_video_codec: Video Codec to use when writing the file
        """
        # Get filename and extension from the file path
        file_name, ext = os.path.splitext(os.path.basename(file_path))
        ext = ext[1:].lower()

        # Ensure we were given a video codec or have a default for this file extension
        if (output_video_codec is None) and (ext in VIDEO_CODECS):
            output_video_codec = VIDEO_CODECS[ext][0]
        else:
            raise ValueError(f"No default video codec found for '{ext}'")

        # Ensure we were given an audio codec or have a default for this file extension
        # otherwise default to 'libmp3lame'
        if (output_audio_codec is None) and (ext in AUDIO_CODECS):
            output_audio_codec = AUDIO_CODECS[ext][0]
        else:
            output_audio_codec = "libmp3lame"

        # Determine audio extension
        audio_extension = None
        for extension, extension_codecs in AUDIO_CODECS.items():
            if output_audio_codec in extension_codecs:
                audio_extension = extension

        # Write the video to the file
        command = [FFMPEG_BINARY,
                   '-y',                                    # Overwrite output file if it exists
                   '-f', 'rawvideo',                        #
                   '-vcodec', 'rawvideo',                   #
                   '-s', self.frame_size,                   # size of one frame, use the Sequence's fps value
                   '-pix_fmt', 'rgb24',                     # pixel format
                   '-r', '%f' % self.fps,                   # frames per second of the sequence
                   '-i', '-',                               # the input comes from a pipe
                   '-an']                                   # tells FFMPEG not to expect any audio

        # If we have an audio stream and we are to write audio
        if write_audio:
            # TODO: Pull this data from audio_stream or somewhere...
            # Audio Info
            fps = 44100
            number_channels = 2
            number_bytes = 2

            audio_data = []
            for clip in self._clips:
                # If the clip has audio and the audio should be written add it to the array
                # of audio data we will write
                if clip.has_audio and clip.include_audio:
                    audio_data.extend(clip.get_audio_frames(clip.file_path, fps, number_bytes, number_channels))

            temp_audio_file_name = f"{file_name}_wvf_snd.tmp.{audio_extension}"

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
            for ad in audio_data:
                process.stdin.write(ad.tobytes())
            process.stdin.close()
            process.wait()

            # Extend the command to pass in the audio we just recorded
            command.extend([
                '-i', temp_audio_file_name,
                '-acodec', 'copy'
            ])

        video_frames = []
        for clip in self._clips:
            video_frames.extend(clip.get_video_frames())

        # Parameters relating to the final outputted file
        command.extend([
            '-preset', 'medium',
            '-pix_fmt', 'yuv420p',
            file_path])

        # Write all the video frame data to the PIPE's standard input
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stdin=subprocess.PIPE,  bufsize=10 ** 8)
        for frame in video_frames:
            process.stdin.write(frame.tobytes())
        process.stdin.close()
        process.wait()