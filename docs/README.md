# FilmPy
FilmPy is a python module for film editing. 
Its goal is to enable programatic video and audio editing. FilmPy is released quarterly via pypi, with a rolling long term stable release. 
Each long term release will be supported for two years. The first official release is planned to be in the spring of 2025. 

Some of the benefits of this package over similiar python packages are
* Easily configurable logging
* Commitment to a DRY and performant approach to software architecture
* A command line interface that allows editing via xml script files
* Helper methods for standard video sizes, pixel formats, 

## Main Functionality
### Using FilmPy you are able to do the following
| Features                                             | Features                                |
| :--------                                            | :---------------------                  |
| Add borders (margin) to a clip                       | Do color division on a clip             |
| Invert the colors of a clip                          | Do color multipication on a clip        |
| Decrease the audio volume of a clip                  | Remove the audio for a track [NOT DONE] |
| Increase the audio volume of a clip                  | Composite video clips                   |
| Create a linear fade in from a given color on a clip | Mirror footage horizontally             |
| Concatenate clips                                    | Mirror footage vertically               |
| Save a single image from a video file                | Gamma Correction |
| Find installed fonts (Windows Only)                  | Convert footage to grayscale |
| Resize the footage using various resampling methods  | Reverse footage |
| Configure package level logging                      | |
| | |

### Expected in version 25.1
| Features                                             | Features                                              |
| :--------------------------------------------------- | :-----------------------------------------------------|
| SlideUp(Transition)                                  | SlideDown(Transition)                                 |
| Create a linear fade out to a given color on a clip  | Add static image overlays to a video clip             |
| ClipBase.audio_fade_out()                            | Clip.fade_in()                                        |
| ClipBase.fade_out()                                  | Adjust the audio volume of a clips and clip sequences |
| ClipBase.audio_normalize()                           |                                                       |

### Thinking About For Later
* Different Storage Engines (datatable?)
* Improved parallezation of processing (too premature)


| Adjust the audio volume of a clips and clip sequences [NOT YET] | Save a single image from a video file ||
| Save clips as video files | Rotate clips, images, and sequences of clips||


## How To Use This Library
There are two primary interfaces to use FilmPy, importing the package or calling it via command line interface. 
These two approaches are briefly described below. 

### Import the editor
The Editor class is designed to be the one and only import needed to use this library. 
The Editor is a class that represents video editing. 
This class does not need to be instantiated to be used.

`from FilmPy import Editor`

### Create some clips 
Now that you have the editor, you need to create some Clips for you to play around with.

```
clip1 = Editor.video_clip('assets/test/.mp4)
clip2 = Editor.vidoe_clip('assets/test/.mp4')
sequence = Editor.concatenate(clip1, clip2)
sequence.write_video_file('output/clip1+clip2.mp4')
```

## Further Reading
 
For more detailed usage, please refer to the documentation found at www.filmpy.org. 
