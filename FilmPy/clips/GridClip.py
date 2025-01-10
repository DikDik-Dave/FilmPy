from .Clip import Clip
from FilmPy.constants import PIXEL_FORMATS
import numpy


class GridClip(Clip):
    def __init__(self,
                 video_end_time=300, # TODO: remove the need to have this set, this is a hack to make it work
                                     # TODO: There is no 'video' for a composite clip so some upstream clip property is wrong
                 clip_end_time=300,
                 clips=None):
        """
        Composite all the clips into a grid showing all the videos at once

        :param clip_end_time: End time in seconds for the clip
        :param clips: Array of clips
        """
        # Initialize ClipBase
        super().__init__(
            clip_end_time=clip_end_time,
            video_end_time=video_end_time)

        # Calculate the cell size for each clip
        cell_size = [0,0]
        max_rows_cols =  [0,0]
        all_frames = {}
        for x in range(len(clips)):
            for j in range(len(clips[x])):
                # Get the clip for this cell
                clip = clips[x][j]
                all_frames[x,j] = clip.get_video_frames()

                # Determine max number of rows and columns
                if x > max_rows_cols[0]:
                    max_rows_cols[0] = x

                if j > max_rows_cols[1]:
                    max_rows_cols[1] = j

                # Determine the cell size
                w,h = clip.size
                if w > cell_size[0]:
                    cell_size[0] = w
                if h > cell_size[1]:
                    cell_size[1] = h



        # TODO: switch to adding/using self.background_color
        number_components = PIXEL_FORMATS[self.pixel_format]['nb_components']
        if number_components == 3:
            bg_pixel = (0,0,0)
        elif number_components == 4:
            bg_pixel = (0,0,0,1)

        #TODO: determine the real number frames
        composited_frames = []

        clip_size = ((max_rows_cols[0]+1)*cell_size[1], cell_size[0]*(max_rows_cols[1]+1))
        for frame_index in range(241):
            frame = (numpy.tile(bg_pixel, clip_size[0] * clip_size[1])
                     .reshape(clip_size[0], clip_size[1], number_components))

            # Composite each clip onto the frame
            for key,clip_frames in all_frames.items():
                try:
                    # Get the frame for this clip
                    clip_frame = clip_frames[frame_index]
                except IndexError:
                    # This clip has no frame for this frame index, go onto the next frame
                    continue


                # Determine where in the clip it should go
                x = key[0] * cell_size[1]
                y = key[1] * cell_size[0]

                # Project the clip_frame onto the frame
                frame[x:(x+cell_size[1]), y:(y+cell_size[0])] = clip_frame
                frame = frame.astype('uint8')

            # Add the frame to the list of composited frames
            composited_frames.append(frame)

        # Set the width and height of the clip
        self.width = clip_size[1]
        self.height = clip_size[0]

        # Set the frames for this clip
        self.set_video_frames(composited_frames)