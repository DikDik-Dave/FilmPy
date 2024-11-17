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