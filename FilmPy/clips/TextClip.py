import numpy as np
from PIL import Image, ImageDraw, ImageFont
from FilmPy.clips.ImageClip import ImageClip
from FilmPy.constants import DEFAULT_FRAME_RATE

class TextClip(ImageClip):
    def __init__(self,
                 align="left",
                 background_color="green",
                 end_time: int = None,
                 fps: int = DEFAULT_FRAME_RATE,
                 fill="white",
                 font_path=None,
                 font_size=None,
                 line_spacing = 4,
                 size=None,
                 stroke_fill="black",
                 stroke_width=0,
                 text=None,
                 **kwargs):
        """
        Instantiate a clip from a piece of text..

        :param align:
        :param background_color:
        :param fill:
        :param font_path:
        :param font_size:
        :param line_spacing:
        :param size:
        :param stroke_fill:
        :param stroke_width:
        :param text: Text to be rendered
        :param kwargs: Remaining keyword arguments, will be passed to ImageClip's constructor
        """

        # Set TextClip specific attributes
        self._text = {
            'align': align,
            'fill': fill,
            'font_path': font_path,
            'font_size': font_size,
            'line_spacing': line_spacing,
            'pixel_format': 'rgba',
            'stroke_fill': stroke_fill,
            'stroke_width': stroke_width,
            'text': text
        }

        # If we were not provided the size for the clip, default it to the text size
        text_width, text_height, text_x, text_y = self._text_size()
        if not size:
            size = text_width, text_height

        # Draw the font to an image
        image = Image.new(self._text['pixel_format'].upper(), (size[0], size[1]), color=background_color)
        font = ImageFont.truetype(font_path, font_size)
        drawing = ImageDraw.Draw(image)
        drawing.multiline_text(
            align=self._text['align'],
            fill=fill,
            font=font,
            spacing=self._text['line_spacing'],
            stroke_fill=self._text['stroke_fill'],
            stroke_width=self._text['stroke_width'],
            text=text,
            xy=(text_x, text_y)
        )


        # Create a frame of the appropriate size
        video_frames = []
        frame = np.array(image).astype('uint8')
        for x in range(int(fps * end_time)):
            video_frames.append(frame)

        # Initialize the ImageClip
        super().__init__(
                         clip_height=size[1],
                         clip_pixel_format=self._text['pixel_format'],
                         clip_pixel_format_output=self._text['pixel_format'],
                         clip_width=size[0],
                         video_frames=video_frames,
                         **kwargs)

    ###################
    # Private Methods #
    ###################
    def _text_size(self) -> tuple:
        """
        Return the width and height needed for the requested text
        :return width,height,x,y: Width and Height, the x,y coordinates of where to draw the text
        """
        image = Image.new("RGB", (1,1))
        image_font = ImageFont.truetype(self._text['font_path'], self._text['font_size'])
        draw = ImageDraw.Draw(image)

        left, top, right, bottom = draw.multiline_textbbox(
            align=self._text['align'],
            font=image_font,
            spacing=self._text['line_spacing'],
            stroke_width=self._text['stroke_width'],
            text=self._text['text'],
            xy=(0,0)
            
        )

        return int(right - left), int(bottom - top), int(0 - left), int(0 - top)

    ###########################
    # Property Methods - Text #
    ###########################
    @property
    def align(self):
        """
        Text alignment of the clip
        """
        return self._text['align']

    @property
    def fill(self):
        """
        Color to use for the text
        """
        return self._text['fill']

    @property
    def font_path(self):
        """
        Full path to the image file being used
        """
        return self._text['font_path']

    @property
    def font_size(self):
        """
        Font size of the text in the clip
        """
        return self._text['font_size']