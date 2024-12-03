import numpy as np
from PIL import Image, ImageDraw, ImageFont
from FilmPy.clips.ClipBase import ClipBase

class TextClip(ClipBase):
    def __init__(self,
                 align="left",
                 background_color=None,
                 clip_end_time=10,
                 font_path=None,
                 font_size=None,
                 line_spacing = 4,
                 text_stroke_color=None,
                 size=None,
                 stroke_width=0,
                 text=None,
                 color="black",
                 **kwargs):
        """

        :param background_color:
        :param clip_end_time:
        :param font_path:
        :param font_size: Size of the font to be used
        :param line_spacing: Number of pixels to use as spacing between lines in multiline text
        :param text_stroke_color:
        :param size: Size of the clip itself, if not provided, will default to the size needed to render the text
        :param stroke_width: The width of the exterior border around each character in a font
        :param text: Actual text to display
        :param color: Color in which the text will be rendered
        """

        # Initialize the ClipBase
        super().__init__(clip_pixel_format_input='rgba',
                         clip_pixel_format_output='rgba')

        # Set TextClip specific attributes
        self._text = {
            'align': align,
            'font_path': font_path,
            'font_size': font_size,
            'line_spacing': line_spacing,
            'stroke_width': stroke_width,
            'text': text
        }

        # Set clip height, width
        if not size:
            size = self._text_size()
        self.width = size[0]
        self.height = size[1]

        # Draw the font to an image
        image = Image.new(self.pixel_format_input.upper(), (self.width, self.height), color=background_color)
        font = ImageFont.truetype(font_path, font_size)
        drawing = ImageDraw.Draw(image)
        drawing.multiline_text(
            align=self._text['align'],
            anchor="lm",
            fill=color,
            font=font,
            spacing=self._text['line_spacing'],
            stroke_width=self._text['stroke_width'],
            text=text,
            xy=(50, 50)
        )

        # Use the image we created as the frame for this clip
        self.set_frames([np.array(image).astype('uint8')])

    def _text_size(self) -> tuple:
        """
        Return the width and height needed for the requested text
        :return:
        """
        image = Image.new("RGB", (1,1))
        image_font = ImageFont.truetype(self._text['font_path'], self._text['font_size'])
        draw = ImageDraw.Draw(image)

        left, top, right, bottom = draw.multiline_textbbox(
            align=self._text['align'],
            anchor="lm",
            font=image_font,
            spacing=self._text['line_spacing'],
            stroke_width=self._text['stroke_width'],
            text=self._text['text'],
            xy=(0, 0)
            
        )

        return int(right - left), int(bottom - top)