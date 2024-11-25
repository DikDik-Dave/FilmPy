from enum import Enum
from PIL.Image import Transpose as _PilTranspose, Resampling as _PILResampling

AUDIO_CODECS = {
    'ogg': ["libvorbis"],
    'mp3': ["libmp3lame"],
    'wav': ["pcm_s16le", "pcm_s24le", "pcm_s32le"],
    'm4a': ["libfdk_aac"]
}
FFMPEG_BINARY = "ffmpeg.exe"

VIDEO_CODECS = {'mp4': ["libx264", "libmpeg4", "aac"],
                'mkv': ["libx264", "libmpeg4", "aac"],
                'ogv': ['libvorbis'],
                'webm': ["libvorbis"]
                }

# PIL Mapping Enum for Resampling, used by resize
class Resampling(Enum):
    BICUBIC  = _PILResampling.BICUBIC.value
    BILINEAR = _PILResampling.BILINEAR.value
    BOX      = _PILResampling.BOX.value
    HAMMING  = _PILResampling.HAMMING.value
    LANCZOS  = _PILResampling.LANCZOS.value
    NEAREST  = _PILResampling.NEAREST.value

# PIL Mapping Enum for Transpositions
class Transpose(Enum):
    FLIP_LEFT_RIGHT = _PilTranspose.FLIP_LEFT_RIGHT.value
    FLIP_TOP_BOTTOM = _PilTranspose.FLIP_TOP_BOTTOM.value

class Fade(Enum):
    EXPONENTIAL = 0
    LINEAR      = 1
    LOGARITHMIC = 1


# https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
class ImageModes(Enum):
    BLACK_AND_WHITE = '1'     # 1-bit pixels, black and white, stored with one pixel per byte
    GRAYSCALE       = 'L'     # 8-bit pixels, grayscale
    P               = 'P'     # 8-bit pixels, mapped to any other mode using a color palette
    RGB             = 'RGB'   # 3x8-bit pixels, true color
    RGBA            = 'RGBA'  # 4x8-bit pixels, true color with transparency mask
    CMYK            = 'CMYK'  # 4x8-bit pixels, color separation
    YCBCR           = 'YCbCr' # 3x8-bit pixels, color video format, Note that this refers to the JPEG, and not the ITU-R BT.2020, standard
    LAB             = 'LAB'   # 3x8-bit pixels, the L*a*b color space
    HSV             = 'HSV'   # 3x8-bit pixels, Hue, Saturation, Value color space. Hue’s range of 0-255 is a scaled version of 0 degrees <= Hue < 360 degrees
    I               = 'I'     # 32-bit signed integer pixels
    F               = 'F'     # 32-bit floating point pixels