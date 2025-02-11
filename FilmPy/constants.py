from enum import Enum
from PIL.Image import Transpose as _PilTranspose, Resampling as _PILResampling

AUDIO_CODECS = {
    'ogg': ["libvorbis"],
    'mp3': ["libmp3lame"],
    'wav': ["pcm_s16le", "pcm_s24le", "pcm_s32le"],
    'm4a': ["libfdk_aac"]}
ENVIRONMENT_FILE = ".filmpy.env"
FONT_EXTENSIONS = ['fon','ttf']                             # Standard extensions for a font file

BINARY_FFMPEG = "ffmpeg.exe"
BINARY_FFPROBE = 'ffprobe.exe'
BINARY_FFPLAY = 'ffplay.exe'

DEFAULT_FRAME_RATE  = 30
DEFAULT_SAMPLE_RATE = 44100

LOG_FILENAME = f"{__name__.split('.')[0]}.log"              # Default log file name to use
STANDARD_FRAME_RATES = (24,25,30,50,60)                     # Standard frame rates
VIDEO_CODECS = {'mp4': ["libx264", "libmpeg4", "aac"],
                'mkv': ["libx264", "libmpeg4", "aac"],
                'ogv': ['libvorbis'],
                'webm': ["libvorbis"]}


# Audio formats
# [nix:ffmpeg -formats | grep PCM] [windows: ffmpeg -formats | FINDSTR PCM]
AUDIO_FORMATS = {
    'alaw' :'PCM A-law',
    'f32be':'PCM 32-bit floating-point big-endian',
    'f32le':'PCM 32-bit floating-point little-endian',
    'f64be':'PCM 64-bit floating-point big-endian',
    'f64le':'PCM 64-bit floating-point little-endian',
    'mulaw':'PCM mu-law',
    's16be':'PCM signed 16-bit big-endian',
    's16le':'PCM signed 16-bit little-endian',
    's24be':'PCM signed 24-bit big-endian',
    's24le':'PCM signed 24-bit little-endian',
    's32be':'PCM signed 32-bit big-endian',
    's32le':'PCM signed 32-bit little-endian',
    's8'   :'PCM signed 8-bit',
    'u16be':'PCM unsigned 16-bit big-endian',
    'u16le':'PCM unsigned 16-bit little-endian',
    'u24be':'PCM unsigned 24-bit big-endian',
    'u24le':'PCM unsigned 24-bit little-endian',
    'u32be':'PCM unsigned 32-bit big-endian',
    'u32le':'PCM unsigned 32-bit little-endian',
    'u8'   : 'PCM unsigned 8-bit',
    'vidc' : 'PCM Archimedes VIDC'}

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
    'rgb4_byte': {'bitstream': False,
             'input': True,
             'output': True,
             'paletted': False,
             'hardware_accelerated': False,
             'nb_components': 3,
             'bits_per_pixel': 4},
    'nv12': {'bitstream': False,
                  'input': True,
                  'output': True,
                  'paletted': False,
                  'hardware_accelerated': False,
                  'nb_components': 3,
                  'bits_per_pixel': 12},
    'nv21': {'bitstream': False,
             'input': True,
             'output': True,
             'paletted': False,
             'hardware_accelerated': False,
             'nb_components': 3,
             'bits_per_pixel': 12},
    'x2rgb10le': {'bitstream': False,
             'input': True,
             'output': True,
             'paletted': False,
             'hardware_accelerated': False,
             'nb_components': 3,
             'bits_per_pixel': 30},
    'abgr': {'bitstream': False,
                  'input': True,
                  'output': True,
                  'paletted': False,
                  'hardware_accelerated': False,
                  'nb_components': 4,
                  'bits_per_pixel': 32},
    'bgra': {'bitstream': False,
             'input': True,
             'output': True,
             'paletted': False,
             'hardware_accelerated': False,
             'nb_components': 4,
             'bits_per_pixel': 32},
    'gray16be': {'bitstream': False,
             'input': True,
             'output': True,
             'paletted': False,
             'hardware_accelerated': False,
             'nb_components': 1,
             'bits_per_pixel': 16},
    'gray16le': {'bitstream': False,
                 'input': True,
                 'output': True,
                 'paletted': False,
                 'hardware_accelerated': False,
                 'nb_components': 1,
                 'bits_per_pixel': 16},
    'yuv440p': {'bitstream': False,
                 'input': True,
                 'output': True,
                 'paletted': False,
                 'hardware_accelerated': False,
                 'nb_components': 3,
                 'bits_per_pixel': 16},
    'yuvj440p': {'bitstream': False,
                'input': True,
                'output': True,
                'paletted': False,
                'hardware_accelerated': False,
                'nb_components': 3,
                'bits_per_pixel': 16},
    'yuva420p': {'bitstream': False,
                 'input': True,
                 'output': True,
                 'paletted': False,
                 'hardware_accelerated': False,
                 'nb_components': 4,
                 'bits_per_pixel': 20},
    'rgb48be': {'bitstream': False,
              'input': True,
              'output': True,
              'paletted': False,
              'hardware_accelerated': False,
              'nb_components': 3,
              'bits_per_pixel': 48},
    'rgb48le': {'bitstream': False,
                'input': True,
                'output': True,
                'paletted': False,
                'hardware_accelerated': False,
                'nb_components': 3,
                'bits_per_pixel': 48},
    'rgb565be': {'bitstream': False,
                'input': True,
                'output': True,
                'paletted': False,
                'hardware_accelerated': False,
                'nb_components': 3,
                'bits_per_pixel': 16},
    'rgb565le': {'bitstream': False,
                 'input': True,
                 'output': True,
                 'paletted': False,
                 'hardware_accelerated': False,
                 'nb_components': 3,
                 'bits_per_pixel': 16},
    'rgb555be': {'bitstream': False,
                 'input': True,
                 'output': True,
                 'paletted': False,
                 'hardware_accelerated': False,
                 'nb_components': 3,
                 'bits_per_pixel': 15},
    'rgb555le': {'bitstream': False,
                 'input': True,
                 'output': True,
                 'paletted': False,
                 'hardware_accelerated': False,
                 'nb_components': 3,
                 'bits_per_pixel': 15},
    'bgr565be': {'bitstream': False,
                 'input': True,
                 'output': True,
                 'paletted': False,
                 'hardware_accelerated': False,
                 'nb_components': 3,
                 'bits_per_pixel': 16},
    'bgr565le': {'bitstream': False,
                 'input': True,
                 'output': True,
                 'paletted': False,
                 'hardware_accelerated': False,
                 'nb_components': 3,
                 'bits_per_pixel': 16},
    'bgr555be': {'bitstream': False,
                 'input': True,
                 'output': True,
                 'paletted': False,
                 'hardware_accelerated': False,
                 'nb_components': 3,
                 'bits_per_pixel': 15},
    'bgr555le': {'bitstream': False,
                 'input': True,
                 'output': True,
                 'paletted': False,
                 'hardware_accelerated': False,
                 'nb_components': 3,
                 'bits_per_pixel': 15},
    'vaapi_moco': {'bitstream': False,
                 'input': False,
                 'output': False,
                 'paletted': False,
                 'hardware_accelerated': True,
                 'nb_components': 0,
                 'bits_per_pixel': 0},
    'vaapi_idct': {'bitstream': False,
                   'input': False,
                   'output': False,
                   'paletted': False,
                   'hardware_accelerated': True,
                   'nb_components': 0,
                   'bits_per_pixel': 0},
    'vaapi_vld': {'bitstream': False,
                   'input': False,
                   'output': False,
                   'paletted': False,
                   'hardware_accelerated': True,
                   'nb_components': 0,
                   'bits_per_pixel': 0},
    'yuv420p16le': {'bitstream': False,
                 'input': True,
                 'output': True,
                 'paletted': False,
                 'hardware_accelerated': False,
                 'nb_components': 3,
                 'bits_per_pixel': 24},
    'yuv420p16be': {'bitstream': False,
                 'input': True,
                 'output': True,
                 'paletted': False,
                 'hardware_accelerated': False,
                 'nb_components': 3,
                 'bits_per_pixel': 24},
    'yuv422p16le': {'bitstream': False,
                    'input': True,
                    'output': True,
                    'paletted': False,
                    'hardware_accelerated': False,
                    'nb_components': 3,
                    'bits_per_pixel': 32},
    'yuv422p16be': {'bitstream': False,
                    'input': True,
                    'output': True,
                    'paletted': False,
                    'hardware_accelerated': False,
                    'nb_components': 3,
                    'bits_per_pixel': 32},
    'yuv444p16le': {'bitstream': False,
                    'input': True,
                    'output': True,
                    'paletted': False,
                    'hardware_accelerated': False,
                    'nb_components': 3,
                    'bits_per_pixel': 48},
    'yuv444p16be': {'bitstream': False,
                    'input': True,
                    'output': True,
                    'paletted': False,
                    'hardware_accelerated': False,
                    'nb_components': 3,
                    'bits_per_pixel': 48},
    'dxva2_vld': {'bitstream': False,
                    'input': False,
                    'output': False,
                    'paletted': False,
                    'hardware_accelerated': True,
                    'nb_components': 0,
                    'bits_per_pixel': 0},
    'rgb444le': {'bitstream': False,
                  'input': True,
                  'output': True,
                  'paletted': False,
                  'hardware_accelerated': False,
                  'nb_components': 3,
                  'bits_per_pixel': 12},
    'rgb444be': {'bitstream': False,
                  'input': True,
                  'output': True,
                  'paletted': False,
                  'hardware_accelerated': False,
                  'nb_components': 3,
                  'bits_per_pixel': 12},
    'bgr444le': {'bitstream': False,
                  'input': True,
                  'output': True,
                  'paletted': False,
                  'hardware_accelerated': False,
                  'nb_components': 3,
                  'bits_per_pixel': 12},
    'bgr444be': {'bitstream': False,
                  'input': True,
                  'output': True,
                  'paletted': False,
                  'hardware_accelerated': False,
                  'nb_components': 3,
                  'bits_per_pixel': 12},
    'ya8': {'bitstream': False,
                 'input': True,
                 'output': True,
                 'paletted': False,
                 'hardware_accelerated': False,
                 'nb_components': 2,
                 'bits_per_pixel': 16},
    'bgr48be': {'bitstream': False,
            'input': True,
            'output': True,
            'paletted': False,
            'hardware_accelerated': False,
            'nb_components': 3,
            'bits_per_pixel': 48},
    'bgr48le': {'bitstream': False,
                'input': True,
                'output': True,
                'paletted': False,
                'hardware_accelerated': False,
                'nb_components': 3,
                'bits_per_pixel': 48},
    'yuv420p9be': {'bitstream': False,
                'input': True,
                'output': True,
                'paletted': False,
                'hardware_accelerated': False,
                'nb_components': 3,
                'bits_per_pixel': 13},
    'yuv420p9le': {'bitstream': False,
                'input': True,
                'output': True,
                'paletted': False,
                'hardware_accelerated': False,
                'nb_components': 3,
                'bits_per_pixel': 13},
    'yuv420p10be': {'bitstream': False,
                   'input': True,
                   'output': True,
                   'paletted': False,
                   'hardware_accelerated': False,
                   'nb_components': 3,
                   'bits_per_pixel': 15},
    'yuv420p10le': {'bitstream': False,
                   'input': True,
                   'output': True,
                   'paletted': False,
                   'hardware_accelerated': False,
                   'nb_components': 3,
                   'bits_per_pixel': 15},
    'yuv422p10be': {'bitstream': False,
                    'input': True,
                    'output': True,
                    'paletted': False,
                    'hardware_accelerated': False,
                    'nb_components': 3,
                    'bits_per_pixel': 20},
    'yuv422p10le': {'bitstream': False,
                    'input': True,
                    'output': True,
                    'paletted': False,
                    'hardware_accelerated': False,
                    'nb_components': 3,
                    'bits_per_pixel': 20},
    'yuv444p9be': {'bitstream': False,
                    'input': True,
                    'output': True,
                    'paletted': False,
                    'hardware_accelerated': False,
                    'nb_components': 3,
                    'bits_per_pixel': 27},
    'yuv444p9le': {'bitstream': False,
                    'input': True,
                    'output': True,
                    'paletted': False,
                    'hardware_accelerated': False,
                    'nb_components': 3,
                    'bits_per_pixel': 27},
}


# TODO - Port and remove entries below
'''
Pixel formats:
I.... = Supported Input  format for conversion
.O... = Supported Output format for conversion
..H.. = Hardware accelerated format
...P. = Paletted format
....B = Bitstream format
FLAGS NAME            NB_COMPONENTS BITS_PER_PIXEL
-----
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

# Internal formats that FilmPy supports
FILMPY_SUPPORTED_PIXEL_FORMATS = ('rgba','rgb24')

class Sizes(Enum):
    """
    Standard video sizes
    """
    CONSOLE_NES = (256, 224)
    YOUTUBE_SHORT = (1080, 1920)
    YOUTUBE_4320P = (7680, 4320)
    YOUTUBE_2160P = (3840, 2160)
    YOUTUBE_1440P = (2560, 1440)
    YOUTUBE_1080P = (1920, 1080)
    YOUTUBE_720P = (1280, 720)
    YOUTUBE_480P = (854,480)
    YOUTUBE_360P = (640,360)
    YOUTUBE_240P = (426,240)

# Legal values that govern how mask and clip data will be interpreted
class Behavior(Enum):
    """
    Governs how the library should behave when the clip's end time exceeds the material we have
    """
    ENFORCE_LIMIT = 0         # Causes the library to throw an error when out of bounds
    LOOP_FRAMES   = 1         # Loop over the existing material as needed
    PAD           = 2         # Add blank frames as needed

class Chess(Enum):
    BLACK = 'black'
    WHITE = 'white'

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

class Mask(Enum):
    BLINK = 'blink'
    BOTTOM_HALF = 'bottom_half'
    TOP_HALF = 'top_half'
    LEFT_HALF = 'left_half'
    RIGHT_HALF = 'right_half'
    LEFT_TRIANGLE = 'left_triangle'
    RIGHT_TRIANGLE = 'right_triangle'