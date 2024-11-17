from FilmPy.library import Clip
import numpy

class ColorClip(Clip):
    def __init__(self, rgb_color, width, height, video_fps, end_time):
        """
        Video Clip of just a single color

        :param rgb_color: (R,G,B) tuple of the color to be displayed
        :param width: Frame width
        :param height: Frame Height
        :param end_time: End Time (Duration) of the clip in seconds
        """
        # Instantiate Clip
        super().__init__(frame_width=width, frame_height=height,start_time=0,
                         end_time=end_time, video_fps=video_fps, write_audio=False)

        # Create the frame
        self._frame = numpy.tile(rgb_color, width * height).reshape(height, width, 3).astype('uint8')

    def get_video_frames(self):
        """
        Get the video frames for this clip
        :return:
        """
        # Calculate the number of frames we need to generate
        number_frames = int(self.video_fps * self._end_time)

        # If we already retrieved the frames, just return them
        if self._video_frames:
            return self._video_frames

        # Create all the frames
        for _ in range(number_frames):
            self._video_frames.append(self._frame)

        # Return the video frames
        return self._video_frames


