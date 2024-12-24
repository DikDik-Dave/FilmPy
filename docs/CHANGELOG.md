# Changelog for FilmPY

## [25.1.0] - 2025-03-DD - Initial Release

- Initial release of the project
- This is the first Long Term Stable Release

### Added
- Added `library/ClipBase.py` - Base class for all clip objects
- Added `library/ClipBase.py` properties
  - Added `ClipBase.audio_channels` property - How many audio channels 
  - Added `ClipBase.audio_sample_rate` property - Sample Rate of the audio
  - Added `Clip.audio_start_index` getter - Frame Index corresponding to `ClipBase.start_time`
  - Added `ClipBase.audio_end_index` getter - Frame index corresponding to `ClipBase.end_time`
  - Added `ClipBase.behavior` -- Needs more work
- Added `library/ClipBase.py` methods
  - Added `ClipBase.__init__()` - Initialize the ClipBase object itself
  - Added `ClipBase.play_audio()` - Plays the audio frames for this clip, via ffplay
- Added library/Clip.py - A clip with audio and/or video
- Added library/ImageClip.py - Clip class to generate clips from a single image
- Added library/TextClip.py - Clip class to generate a clip from a piece of text
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


