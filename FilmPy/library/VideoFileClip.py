from ffmpeg import FFmpeg

import json
import numpy
import subprocess
from FilmPy.library.constants import FFMPEG_BINARY
from FilmPy.library import Clip


class VideoFileClip(Clip):
    """
    Video Clip from a file
    """
    def __init__(self, video_file_path, start_time=0, end_time=None, include_audio=True):
        """
        Initialize a Video File Clip

        :param video_file_path: path to the video file associated with this clip
        :param start_time: When does the clip start
        :param end_time: When does the clip end
        :param include_audio: Should the audio be written for this clip
        """
        # Initialize Clip, we will set the frame_width, frame_height, and video_fps values
        # after we have processed the metadata for this clip
        super().__init__(frame_width=None, frame_height=None, start_time=start_time,
                         end_time=end_time, video_fps=None, include_audio=include_audio)

        # Call ffprobe to get information about the file
        ffprobe = FFmpeg(executable="ffprobe").input(
            video_file_path,
            print_format="json",  # ffprobe will output the results in JSON format
            show_streams=None,
        )

        ffmpeg_info_command = [FFMPEG_BINARY, "-hide_banner", "-i", video_file_path]
        completed_process = subprocess.run(ffmpeg_info_command, capture_output=True)
        for line in completed_process.stderr.splitlines()[1:]:
            if b'Duration: ' in line:
                duration, start, bit_rate = line.split( b',')

                # Process the duration
                hours, minutes, seconds = duration.strip(b'Duration: ').split(b':')
                self.video_duration = (int(hours) * 60 * 60) + (int(minutes) * 60) + float(seconds)

                # Process video start
                self.video_start = float(start.split(b':')[1])

                self.video_bit_rate = bit_rate.split(b': ')[1].decode('utf8')
            elif (b'Stream #0' in line) and (b'Video:' in line):
                # Set the video_fps attribute
                value_end = line.find(b' fps')
                value_start = line[:value_end].rfind(b', ')
                self.video_fps = float(line[value_start+2:value_end])

                # Set the video_tbr attribute
                value_end = line.find(b' tbr,')
                value_start = line[:value_end].rfind(b', ')
                self.video_tbr = float(line[value_start+2:value_end])
            elif (b'Stream #0' in line) and (b'Audio:' in line):
                # print(line)
                pass

        self._media = json.loads(ffprobe.execute())
        self._video_info = self._media['streams'][0]
        self._audio_stream = self._media['streams'][1]
        self._video_file_path = video_file_path

        # Set video stream attributes
        self._video_info['duration'] = float(self._video_info['duration'])
        self._video_info['height'] = int(self._video_info['height'])
        self._video_info['resolution'] = f"{self._video_info['width']}x{self._video_info['height']}"
        self._video_info['width'] = int(self._video_info['width'])

        # If no end_time was specified set it to be the video's duration
        if not end_time:
            self._end_time = self.video_duration

    def get_audio_data(self,
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
        acodec_param = 'pcm_s%dle' % (8 * number_bytes)

        ffmpeg_command = [FFMPEG_BINARY,
                          '-i', file_name, '-vn',
                          '-loglevel', 'error',
                          '-f', 's%dle' % (8 * number_bytes),
                          '-acodec', 'pcm_s%dle' % (8 * number_bytes),
                          '-ar', '%d' % fps,
                          '-ac', '%d' % number_channels,
                          '-'
                          ]

        # TODO: Currently returning raw binary data, need to adjust this to get audio frames at some point
        # TODO: Maybe Switch to PyAV for this low level stuff...

        completed_process = subprocess.run(ffmpeg_command, capture_output=True)

        # return completed_process.stdout
        dt = {1: 'int8', 2: 'int16', 4: 'int32'}[number_bytes]
        audio_data = numpy.fromstring(completed_process.stdout, dtype=dt).reshape(-1, number_channels)
        return audio_data

    def get_video_frames(self):
        """
        Get the video frames
        :return: List of frames
        """

        # If we already loaded the frames, just return them
        if self._clip_frames:
            return self._clip_frames

        # Call ffmpeg and pipe it's output
        command = [FFMPEG_BINARY,
                   '-i', self._video_file_path,
                   '-f', 'image2pipe',
                   '-pix_fmt', 'rgb24',
                   '-vcodec', 'rawvideo',
                   '-']

        # Read the video data
        completed_process = subprocess.run(command, capture_output=True)

        # Get all frames
        frame_length = self._video_info['width'] * self._video_info['height'] * 3
        for i in range(0, len(completed_process.stdout), frame_length):
            frame = completed_process.stdout[i:i + frame_length]
            frame = numpy.fromstring(frame, dtype='uint8').reshape((self._video_info['height'],
                                                                    self._video_info['width'],
                                                                    3))

            # Store the frame in our frames list
            self._clip_frames.append(frame)

        return self._clip_frames