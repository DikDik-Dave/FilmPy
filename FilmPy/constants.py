from enum import Enum
from PIL.Image import Transpose as _PilTranspose, Resampling as _PILResampling

AUDIO_CODECS = {
    'ogg': ["libvorbis"],
    'mp3': ["libmp3lame"],
    'wav': ["pcm_s16le", "pcm_s24le", "pcm_s32le"],
    'm4a': ["libfdk_aac"]
}
FONT_EXTENSIONS = ['fon','ttf']

FFMPEG_BINARY = "ffmpeg.exe"
FFPROBE_BINARY = 'ffprobe.exe'

VIDEO_CODECS = {'mp4': ["libx264", "libmpeg4", "aac"],
                'mkv': ["libx264", "libmpeg4", "aac"],
                'ogv': ['libvorbis'],
                'webm': ["libvorbis"]
                }

# Default log file name to use
LOG_FILENAME = f"{__name__.split('.')[0]}.log"

# ffmpeg pixel formats
PIXEL_FORMATS = {
    'yuv420p': { 'bitstream': False,
                  'input': True,
                  'output': True,
                  'paletted': False,
                  'hardware_accelerated':False,
                  'nb_components': 3,
                  'bits_per_pixel': 12},
    'yuyv422': {'bitstream': False,
                  'input': True,
                  'output': True,
                  'paletted': False,
                  'hardware_accelerated':False,
                  'nb_components': 3,
                  'bits_per_pixel': 16},
    'rgb24': {  'bitstream': False,
              'input': True,
              'output': True,
              'paletted': False,
              'hardware_accelerated':False,
              'nb_components': 3,
              'bits_per_pixel': 24},
    'bgr24': {'bitstream': False,
            'input': True,
            'output': True,
            'paletted': False,
            'hardware_accelerated': False,
            'nb_components': 3,
            'bits_per_pixel': 24},
    'yuv422p': {'bitstream': False,
            'input': True,
            'output': True,
            'paletted': False,
            'hardware_accelerated': False,
            'nb_components': 3,
            'bits_per_pixel': 16},
    'yuv444p': {'bitstream': False,
            'input': True,
            'output': True,
            'paletted': False,
            'hardware_accelerated': False,
            'nb_components': 3,
            'bits_per_pixel': 24},
    'yuv410p': {'bitstream': False,
            'input': True,
            'output': True,
            'paletted': False,
            'hardware_accelerated': False,
            'nb_components': 3,
            'bits_per_pixel': 9},
    'yuv411p': {'bitstream': False,
                'input': True,
                'output': True,
                'paletted': False,
                'hardware_accelerated': False,
                'nb_components': 3,
                'bits_per_pixel': 12},
    'gray': {'bitstream': False,
                'input': True,
                'output': True,
                'paletted': False,
                'hardware_accelerated': False,
                'nb_components': 1,
                'bits_per_pixel': 8},
    'monow': {'bitstream': True,
             'input': True,
             'output': True,
             'paletted': False,
             'hardware_accelerated': False,
             'nb_components': 1,
             'bits_per_pixel': 1},
    'monob': {'bitstream': True,
              'input': True,
              'output': True,
              'paletted': False,
              'hardware_accelerated': False,
              'nb_components': 1,
              'bits_per_pixel': 1},
    'pal8': {'bitstream': False,
              'input': True,
              'output': False,
              'paletted': True,
              'hardware_accelerated': False,
              'nb_components': 1,
              'bits_per_pixel': 8},
    'yuvj420p': {'bitstream': False,
             'input': True,
             'output': True,
             'paletted': False,
             'hardware_accelerated': False,
             'nb_components': 3,
             'bits_per_pixel': 12},
    'yuvj422p': {'bitstream': False,
                 'input': True,
                 'output': True,
                 'paletted': False,
                 'hardware_accelerated': False,
                 'nb_components': 3,
                 'bits_per_pixel': 16},
    'yuvj444p': {'bitstream': False,
                 'input': True,
                 'output': True,
                 'paletted': False,
                 'hardware_accelerated': False,
                 'nb_components': 3,
                 'bits_per_pixel': 24},
    'uyvy422': {'bitstream': False,
                 'input': True,
                 'output': True,
                 'paletted': False,
                 'hardware_accelerated': False,
                 'nb_components': 3,
                 'bits_per_pixel': 16},
    'uyyvyy411': {'bitstream': False,
                'input': False,
                'output': False,
                'paletted': False,
                'hardware_accelerated': False,
                'nb_components': 3,
                'bits_per_pixel': 12},
    'bgr8': {'bitstream': True,
                  'input': False,
                  'output': True,
                  'paletted': False,
                  'hardware_accelerated': False,
                  'nb_components': 3,
                  'bits_per_pixel': 8},
    'bgr4': {'bitstream': True,
             'input': False,
             'output': True,
             'paletted': False,
             'hardware_accelerated': False,
             'nb_components': 3,
             'bits_per_pixel': 4},
    'bgr4_byte': {'bitstream': False,
             'input': True,
             'output': True,
             'paletted': False,
             'hardware_accelerated': False,
             'nb_components': 3,
             'bits_per_pixel': 4},
    'rgba': {'bitstream': False,
                  'input': True,
                  'output': True,
                  'paletted': False,
                  'hardware_accelerated': False,
                  'nb_components': 4,
                  'bits_per_pixel': 32},
    'rgb8': {'bitstream': False,
             'input': True,
             'output': True,
             'paletted': False,
             'hardware_accelerated': False,
             'nb_components': 3,
             'bits_per_pixel': 8},
    'x2rgb10be': {'bitstream': False,
             'input': False,
             'output': False,
             'paletted': False,
             'hardware_accelerated': False,
             'nb_components': 3,
             'bits_per_pixel': 30},
    'argb': {'bitstream': False,
                  'input': True,
                  'output': True,
                  'paletted': False,
                  'hardware_accelerated': False,
                  'nb_components': 4,
                  'bits_per_pixel': 32},
    'rgb4': {'bitstream': True,
             'input': False,
             'output': True,
             'paletted': False,
             'hardware_accelerated': False,
             'nb_components': 3,
             'bits_per_pixel': 4},

    'x2rgb10le': {'bitstream': False,
             'input': True,
             'output': True,
             'paletted': False,
             'hardware_accelerated': False,
             'nb_components': 3,
             'bits_per_pixel': 30}
}

#TODO - Port and remove entries below
'''
Pixel formats:
I.... = Supported Input  format for conversion
.O... = Supported Output format for conversion
..H.. = Hardware accelerated format
...P. = Paletted format
....B = Bitstream format
FLAGS NAME            NB_COMPONENTS BITS_PER_PIXEL
-----
IO... rgb4_byte              3             4
IO... nv12                   3            12
IO... nv21                   3            12
IO... abgr                   4            32
IO... bgra                   4            32
IO... gray16be               1            16
IO... gray16le               1            16
IO... yuv440p                3            16
IO... yuvj440p               3            16
IO... yuva420p               4            20
IO... rgb48be                3            48
IO... rgb48le                3            48
IO... rgb565be               3            16
IO... rgb565le               3            16
IO... rgb555be               3            15
IO... rgb555le               3            15
IO... bgr565be               3            16
IO... bgr565le               3            16
IO... bgr555be               3            15
IO... bgr555le               3            15
..H.. vaapi_moco             0             0
..H.. vaapi_idct             0             0
..H.. vaapi_vld              0             0
IO... yuv420p16le            3            24
IO... yuv420p16be            3            24
IO... yuv422p16le            3            32
IO... yuv422p16be            3            32
IO... yuv444p16le            3            48
IO... yuv444p16be            3            48
..H.. dxva2_vld              0             0
IO... rgb444le               3            12
IO... rgb444be               3            12
IO... bgr444le               3            12
IO... bgr444be               3            12
IO... ya8                    2            16
IO... bgr48be                3            48
IO... bgr48le                3            48
IO... yuv420p9be             3            13
IO... yuv420p9le             3            13
IO... yuv420p10be            3            15
IO... yuv420p10le            3            15
IO... yuv422p10be            3            20
IO... yuv422p10le            3            20
IO... yuv444p9be             3            27
IO... yuv444p9le             3            27
IO... yuv444p10be            3            30
IO... yuv444p10le            3            30
IO... yuv422p9be             3            18
IO... yuv422p9le             3            18
IO... gbrp                   3            24
IO... gbrp9be                3            27
IO... gbrp9le                3            27
IO... gbrp10be               3            30
IO... gbrp10le               3            30
IO... gbrp16be               3            48
IO... gbrp16le               3            48
IO... yuva422p               4            24
IO... yuva444p               4            32
IO... yuva420p9be            4            22
IO... yuva420p9le            4            22
IO... yuva422p9be            4            27
IO... yuva422p9le            4            27
IO... yuva444p9be            4            36
IO... yuva444p9le            4            36
IO... yuva420p10be           4            25
IO... yuva420p10le           4            25
IO... yuva422p10be           4            30
IO... yuva422p10le           4            30
IO... yuva444p10be           4            40
IO... yuva444p10le           4            40
IO... yuva420p16be           4            40
IO... yuva420p16le           4            40
IO... yuva422p16be           4            48
IO... yuva422p16le           4            48
IO... yuva444p16be           4            64
IO... yuva444p16le           4            64
..H.. vdpau                  0             0
IO... xyz12le                3            36
IO... xyz12be                3            36
..... nv16                   3            16
..... nv20le                 3            20
..... nv20be                 3            20
IO... rgba64be               4            64
IO... rgba64le               4            64
IO... bgra64be               4            64
IO... bgra64le               4            64
IO... yvyu422                3            16
IO... ya16be                 2            32
IO... ya16le                 2            32
IO... gbrap                  4            32
IO... gbrap16be              4            64
IO... gbrap16le              4            64
..H.. qsv                    0             0
..H.. mmal                   0             0
..H.. d3d11va_vld            0             0
..H.. cuda                   0             0
IO... 0rgb                   3            24
IO... rgb0                   3            24
IO... 0bgr                   3            24
IO... bgr0                   3            24
IO... yuv420p12be            3            18
IO... yuv420p12le            3            18
IO... yuv420p14be            3            21
IO... yuv420p14le            3            21
IO... yuv422p12be            3            24
IO... yuv422p12le            3            24
IO... yuv422p14be            3            28
IO... yuv422p14le            3            28
IO... yuv444p12be            3            36
IO... yuv444p12le            3            36
IO... yuv444p14be            3            42
IO... yuv444p14le            3            42
IO... gbrp12be               3            36
IO... gbrp12le               3            36
IO... gbrp14be               3            42
IO... gbrp14le               3            42
IO... yuvj411p               3            12
I.... bayer_bggr8            3             8
I.... bayer_rggb8            3             8
I.... bayer_gbrg8            3             8
I.... bayer_grbg8            3             8
I.... bayer_bggr16le         3            16
I.... bayer_bggr16be         3            16
I.... bayer_rggb16le         3            16
I.... bayer_rggb16be         3            16
I.... bayer_gbrg16le         3            16
I.... bayer_gbrg16be         3            16
I.... bayer_grbg16le         3            16
I.... bayer_grbg16be         3            16
..H.. xvmc                   0             0
IO... yuv440p10le            3            20
IO... yuv440p10be            3            20
IO... yuv440p12le            3            24
IO... yuv440p12be            3            24
IO... ayuv64le               4            64
..... ayuv64be               4            64
..H.. videotoolbox_vld       0             0
IO... p010le                 3            15
IO... p010be                 3            15
IO... gbrap12be              4            48
IO... gbrap12le              4            48
IO... gbrap10be              4            40
IO... gbrap10le              4            40
..H.. mediacodec             0             0
IO... gray12be               1            12
IO... gray12le               1            12
IO... gray10be               1            10
IO... gray10le               1            10
IO... p016le                 3            24
IO... p016be                 3            24
..H.. d3d11                  0             0
IO... gray9be                1             9
IO... gray9le                1             9
IO... gbrpf32be              3            96
IO... gbrpf32le              3            96
IO... gbrapf32be             4            128
IO... gbrapf32le             4            128
..H.. drm_prime              0             0
..H.. opencl                 0             0
IO... gray14be               1            14
IO... gray14le               1            14
IO... grayf32be              1            32
IO... grayf32le              1            32
IO... yuva422p12be           4            36
IO... yuva422p12le           4            36
IO... yuva444p12be           4            48
IO... yuva444p12le           4            48
IO... nv24                   3            24
IO... nv42                   3            24
..H.. vulkan                 0             0
..... y210be                 3            20
I.... y210le                 3            20
'''

# Legal values that govern how mask frame data will be interpreted
class MaskBehavior(Enum):
    LOOP_FRAMES = 0
    FINITE_LIST = 1

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