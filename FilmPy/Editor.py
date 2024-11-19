from FilmPy.library import *
import numpy as np

from FilmPy.library.ImageClip import ImageClip


class Editor:
    """
    Editor class, meant to be the primary import for editing videos
    """

    ##################################
    # Object Instantiation Functions #
    ##################################
    @classmethod
    def color_clip(cls,
                   color:tuple,
                   frame_width:int,
                   frame_height:int,
                   end_time:float,
                   video_fps:float
                   ) -> ColorClip:
        """
        Instantiate a ColorClip object

        :param video_fps:
        :param color: RGB tuple of the color to be displayed
        :param frame_width: Frame Width
        :param frame_height: Frame Height
        :param end_time: End time in seconds of the clip
        :return:
        """
        return ColorClip(color,frame_width, frame_height, video_fps, end_time)

    @classmethod
    def image_clip(cls, **kwargs):
        return ImageClip(**kwargs)

    @classmethod
    def sequence(cls) -> Sequence:
        """
        Instantiate a Sequence object
        :return:  Sequence
        """
        return Sequence()

    @classmethod
    def video_file_clip(cls, clip_path):
        """
        Instantiate a VideoFileClip object

        :return: VideoFileClip
        """
        return VideoFileClip(clip_path)


    ##################
    # Public Methods #
    ##################
    @classmethod
    def concatenate(cls, clips) -> Sequence:
        """
        Concatenate the clips into a single sequence

        :param clips:
        :return: Sequence - The clips combined into a single sequence
        """
        return Sequence(clips)


    # @classmethod
    # def concatenate(cls, clips):
    #     """
    #     Concatenate Video Clips
    #
    #     :param clips:
    #     :return:
    #     """
    #     timings = np.cumsum([0] + [clip.video_duration for clip in clips])
    #     print(timings)
    #
    #     timings = np.cumsum([clip.video_duration for clip in clips])
    #     print(timings)
    #     max_width = max([clip.video_width for clip in clips])
    #     max_height = max([clip.video_height for clip in clips])
    #     print(max_width)
    #     print(max_height)
    #
    #     timings = np.maximum(0, timings + padding * np.arange(len(timings)))
    #     timings[-1] -= padding  # Last element is the duration of the whole
    #     #
    #     # if method == "chain":
    #     #
    #     #     def make_frame(t):
    #     #         i = max([i for i, e in enumerate(timings) if e <= t])
    #     #         return clips[i].get_frame(t - timings[i])
    #     #
    #     #     def get_mask(clip):
    #     #         mask = clip.mask or ColorClip([1, 1], color=1, is_mask=True)
    #     #         if mask.duration is None:
    #     #             mask.duration = clip.duration
    #     #         return mask
    #     #
    #     result = VideoClip(is_mask=is_mask, make_frame=make_frame)
    #     if any([clip.mask is not None for clip in clips]):
    #         masks = [get_mask(clip) for clip in clips]
    #         result.mask = concatenate_videoclips(masks, method="chain", is_mask=True)
    #         result.clips = clips



        #
        # timings = np.cumsum([0] + [clip.duration for clip in clips])
        #
        # sizes = [clip.size for clip in clips]
        #
        # w = max(size[0] for size in sizes)
        # h = max(size[1] for size in sizes)
        #
        # timings = np.maximum(0, timings + padding * np.arange(len(timings)))
        # timings[-1] -= padding  # Last element is the duration of the whole
        #
        # if method == "chain":
        #
        #     def make_frame(t):
        #         i = max([i for i, e in enumerate(timings) if e <= t])
        #         return clips[i].get_frame(t - timings[i])
        #
        #     def get_mask(clip):
        #         mask = clip.mask or ColorClip([1, 1], color=1, is_mask=True)
        #         if mask.duration is None:
        #             mask.duration = clip.duration
        #         return mask
        #
        #     result = VideoClip(is_mask=is_mask, make_frame=make_frame)
        #     if any([clip.mask is not None for clip in clips]):
        #         masks = [get_mask(clip) for clip in clips]
        #         result.mask = concatenate_videoclips(masks, method="chain", is_mask=True)
        #         result.clips = clips
        # elif method == "compose":
        #     result = CompositeVideoClip(
        #         [
        #             clip.with_start(t).with_position("center")
        #             for (clip, t) in zip(clips, timings)
        #         ],
        #         size=(w, h),
        #         bg_color=bg_color,
        #         is_mask=is_mask,
        #     )
        # else:
        #     raise Exception(
        #         "MoviePy Error: The 'method' argument of "
        #         "concatenate_videoclips must be 'chain' or 'compose'"
        #     )
        #
        # result.timings = timings
        #
        # result.start_times = timings[:-1]
        # result.start, result.duration, result.end = 0, timings[-1], timings[-1]
        #
        # audio_t = [
        #     (clip.audio, t) for clip, t in zip(clips, timings) if clip.audio is not None
        # ]
        # if audio_t:
        #     result.audio = CompositeAudioClip([a.with_start(t) for a, t in audio_t])
        #
        # fpss = [clip.fps for clip in clips if getattr(clip, "fps", None) is not None]
        # result.fps = max(fpss) if fpss else None
        # return result

        #     def make_frame(t):
        #         i = max([i for i, e in enumerate(timings) if e <= t])
        #         return clips[i].get_frame(t - timings[i])
        #
        #     def get_mask(clip):
        #         mask = clip.mask or ColorClip([1, 1], color=1, is_mask=True)
        #         if mask.duration is None:
        #             mask.duration = clip.duration
        #         return mask
        #