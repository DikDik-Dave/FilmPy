# FilmPy
FilmPy is a python module for film editing. 
Its goal is to enable programatic video and audio editing. FilmPy is released quarterly via pypi, with a rolling long term stable release. 
Each long term release will be supported for two years. The first official release is planned to be in the spring of 2025. 

Some of the benefits of this package over similiar python packages are
* Easily configurable logging
* Commitment to a DRY and performant approach to software architecture
* A command line interface that allows editing via xml script files
* Helper methods for standard video sizes, pixel formats, 

## How To Use This Library
There are two primary interfaces to use FilmPy, importing the package or calling it via command line interface. 
These two approaches are briefly described below. 

### Import the editor
The Editor class is designed to be the one and only import needed to use this library. 
The Editor is a class that represents video editing. 
This class does not need to be instantiated to be used.

`from FilmPy import Editor`

### Create some clips 
Now that you have the editor, lets create a clip, transform it, and then write it to video. 

```
clip = Editor.clip('assets/test/chameleon_small.mp4').mirror_x().mirror_y().write_video('output/chameleon_flipped_and_rotated.mp4')
```

In the example above, we used method chaining to shorten what we needed to type out. The example below is identical to the one above. 

```
clip = Editor.clip('assets/test/chameleon_small.mp4)
clip.mirror_x()
clip.mirror_y()
clip.write_video('output/chameleon_flipped_and_rotated.mp4')
```

## Main Functionality
### Using FilmPy you are able to do the following
| Features                                                                                           | Features                                |
| :--------                                                                                          | :---------------------                  |
| [Add borders / margin to a clip](http://filmpy.org/tutorials/adding-borders-to-a-clip.html)        | Do color division on a clip             |
| Invert the colors of a clip                                                                        | Do color multipication on a clip        |
| Decrease the audio volume of a clip                  | Remove the audio for a track [NOT DONE] |
| Increase the audio volume of a clip                  | Composite video clips                   |
| Create a linear fade in from a given color on a clip | Mirror footage horizontally             |
| Concatenate clips                                    | Mirror footage vertically               |
| Save a single image from a video file                | Gamma Correction                        |
| Find installed fonts (Windows Only)                  | Convert footage to grayscale            |
| Resize the footage using various resampling methods  | Reverse footage                         |
| Configure package level logging                      | Adjust the audio volume of a clips and clip sequences [NOT YET] |
| Save a single image from a video file                | Save clips as video files                                       |
| Rotate clips, images, and sequences of clips         | Save a single image from a video file                           |
| Cut footage out of a clip                            | Trim the beginning or end of a clip                             |
| Play the video associated with the clip              | Produce a stippled image                                        |

### Expected in version 25.1.0
| Features                                             | Features                                                 |
| :--------------------------------------------------- | :--------------------------------------------------------|
| ClipBase.blink()                                     | Adjust the audio volume of a clips and clip sequences    |
| ClipBase.fade_in()                                   | ClipBase.fade_out()                                      |
| SlideUp(Transition)                                  | SlideDown(Transition)                                    |
| Create a linear fade out to a given color on a clip  | Add static image overlays to a video clip                |
| ClipBase.audio_fade_out()                            | ClipBase.bilevel()                                       |
| ClipBase.audio_normalize()                           |  ClipBase.pixel_format()                                 |
| ClipBase.slide_up() [dynamic resize?]                | ClipBase.slide_down() [dynamic resize?]                  |
| ClipBase.blink(color=XXXX, frame=XXXXX)              | ClipBase.audio_fade_in(,algorithm=Fade.LINEAR) parameter |
| ClipBase.dynamic_resize()                            | ClipBase.trim_audio()                                    |
| Editor.insert(clip, insert_clip)                     | ClipBase.trim_video() & ClipBase.trim()                  |
| ClipBase.cut_audio()                                 | ClipBase.play()                                          |
| ClipBase.play_video()                                |                                         |

### Expected sometime 
| Features                                             | Description                                              |
| :--------------------------------------------------- | :--------------------------------------------------------|
| ClipBase.accelerate()                                |                                                          |
| ClipBase.decelerate()                                |                                                          |
| CrossFade(Transition)                                | Cross fade between two clips                             |
| ClipBase.add_subtitles()                             | Add subtitle text to a clip                              |
| ClipBase.add_subtitle_track()                        | Add a subtitle track to the the clip                     |
| Nagware                                              | ClipBase.motion_blur() |
| ClipBase.dynamic_resize()                            | ClipBase.slide() |
| ClipBase.head_blur() |ClipBase.scroll() |
| Clip Hierarchy HTML page | ClipBase.duplicate() |
| ClipBase.subclip() | ClipBase.typewriter_text() |
| RecipeClip | BookReviewClip() |
| ClipBase.freeze(extend_audio=True) | |
| ChessClip - Board Orientation || 


### Thinking About For Later
* Different Storage Engines (datatable?)
* Improved parallezation of processing (too premature)
* Library level caching of footage (CACHE_DIR, CACHE_SIZE, CACHE_ROTATION)
* pytest (or other) testing framework integration
* librosa?
* FilmRegistry singleton
* Faster approach to pixel format conversion
* Get all rgb colors in an image.
  
## Further Reading
 
For more detailed usage, please refer to the documentation on [www.filmpy.org](http://www.filmpy.org). 
