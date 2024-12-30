# Changelog for FilmPY

## [25.1.0] - 2025-03-DD - Initial Release

- Initial release of the project
- This is the first Long Term Stable Release

### Added
- Added `library/ClipBase.py` - Base class for all clip objects
- Added `library/ClipBase.py` audio properties
  - Added `ClipBase.audio_channels` property - How many audio channels 
  - Added `ClipBase.audio_profile` - getter
  - Added `ClipBase.audio_sample_rate` property - Sample Rate of the audio
  - Added `Clip.audio_start_index` getter - Frame Index corresponding to `ClipBase.start_time`
  - Added `ClipBase.audio_end_index` getter - Frame index corresponding to `ClipBase.end_time`
- Added `library/ClipBase.py` clip properties
  - Added `ClipBase.behavior` -- Needs more work
  - Added `ClipBase.ffmpeg_binary` - Path to the ffmpeg binary to use
  - Added `ClipBase.ffplay_binary` - Path to the ffplay binary to use
  - Added `ClipBase.ffprobe_binary` - Path to the ffprobe binary to use
  - Added `ClipBase.default_frame_rate` - Default frame rate to use when creating an uninitialized clip
- Added `library/ClipBase.py` methods
  - Added `ClipBase.__init__()` - Initialize the ClipBase object itself 
  - Added `ClipBase._read_audio()` - Reads audio from a file.
  - Added `ClipBase.audio_initialize(duration,audio_channels)` - Initialize audio for the clip (replaces existing audio)
  - Added `ClipBase.add_colors(red_added,green_added,blue_added,luminance)` - Perform color addition on the clip
  - Added `ClipBase.add_sound(sound_time, sound_frames=None, file_path=None)` - Adds the given audio frames at the specific time requested
  - Added `ClipBase.blink()` - Blacks out frames of the video to create a blinking effect
  - Added `ClipBase.invert_colors()` - Invert the colors in the image
  - Added `ClipBase.even_dimensions()` - Trims the height and width as needed so the clip's height and width are even
  - Added `ClipBase.freeze(time, duration)` - Freeze the clip at `time` for `duration` seconds
  - Added `ClipBase.freeze_region(time, duration, inside, outside)` -Freeze every inside or outside a region
  - Added `ClipBase.painting(saturation,black)` - Convert the video into a type of painting 
  - Added `ClipBase.play_audio()` - Plays the audio frames for this clip, via ffplay
  - Added `ClipBase.set_pixel_format()` - Changes the internal pixel format used for the video frames
  - Added `ClipBase.write_audio(file_path)` - Creates an audio file from this clip's audio
  - Added `ClipBase.write_video(file_path)` - Creates a video file from this clip
- Added `library/Clip.py` - A clip with audio and/or video
- Added `library/Clip.py` - methods
  - Added `Clip._set_file_information()` - Sets the file information as retrieved from ffmpeg,etc
- Added `library/ImageClip.py` - Clip class to generate clips from a single image
- Added `library/TextClip.py` - Clip class to generate a clip from a piece of text
- Added library/ColorClip.py - Clip class to generate a clip from a color
- Added library/constants.py - Central place to define constants for use
- Added library/CompositeClip.py - Clip class that allows the composition of clips 
- Added library/Sequence.py - class to represent a sequence of clips
- Added Editor.py - Utility class made to simplify module usage by providing a single import

## [25.2.0] - 2025-06-DD
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [25.3.0] - 2025-06-DD - pytest
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security


