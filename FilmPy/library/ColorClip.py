from FilmPy.library.ImageClip import ImageClip
import numpy

class ColorClip(ImageClip):
    def __init__(self, rgb_color, width, height, video_fps, end_time):
        """
        Video Clip of just a single color

        :param rgb_color: (R,G,B) tuple of the color to be displayed
        :param width: Frame width
        :param height: Frame Height
        :param end_time: End Time (Duration) of the clip in seconds
        """
        # Instantiate ImageClip
        self._frame = numpy.tile(rgb_color, width * height).reshape(height, width, 3).astype('uint8')
        super().__init__(frame_data=self._frame, end_time=end_time, video_fps=video_fps)

    def get_video_frames(self):
        """
        Get the video frames for this clip
        :return:
        """
        # Calculate the number of frames we need to generate
        number_frames = int(self.video_fps * self._clip_end)

        # If we already retrieved the frames, just return them
        if self._clip_frames:
            return self._clip_frames

        # Create all the frames
        for _ in range(number_frames):
            self._clip_frames.append(self._frame)

        # Return the video frames
        return self._clip_frames


