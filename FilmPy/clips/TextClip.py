import numpy as np
from PIL import Image, ImageDraw, ImageFont
from FilmPy.clips.ClipBase import ClipBase
from FilmPy.constants import ImageModes


class TextClip(ClipBase):
    def __init__(self,
                 font_path,
                 background_color=None,
                 font_size=None,
                 image_mode=ImageModes.RGBA.value,
                 text_color="black"):
        """
        Initialize a text clip
        """
        # Initialize the clip
        super().__init__()

        # Draw the font to an image
        width = 100
        height = 100
        font_size=12
        image = Image.new(image_mode, (width, height), color=background_color)
        font = ImageFont.truetype(font_path, font_size)
        drawing = ImageDraw.Draw(image)
        drawing.multiline_text(
            xy=(50, 50),
            text="First Test",
            fill=text_color,
            font=font,
            anchor="lm"
        )
        self.set_frames([np.array(image).astype('uint8')])
        frames = self.get_frames()
        print(frames)
        # @convert_path_to_string("filename")
        # def __init__(
        #         self,
        #         font,
        #         text=None,
        #         filename=None,
        #         font_size=None,
        #         size=(None, None),
        #         margin=(None, None),
        #         color="black",
        #         bg_color=None,
        #         stroke_color=None,
        #         stroke_width=0,
        #         method="label",
        #         text_align="left",
        #         horizontal_align="center",
        #         vertical_align="center",
        #         interline=4,
        #         transparent=True,
        #         duration=None,
        # ):

