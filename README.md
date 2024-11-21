# FilmPy
FilmPy is a python module for film editing. 
Its goal is to enable fully video and audio editing. 

## Main Functionality
By using FilmPy you will be able to 
| :----------------------------------------------------- | :----------------------------------------------------- |
| Add static image overlays to a video clip [NOT YET]    | Concatenate clips                                      |
| Create composite video clips [NOT YET]                 | Rotate clips, images, and sequences of clips           |
| Mirror horizontally clips, images, and clip sequences  | Mirror vertically clips, images, and clip sequences    |


* Mirror horizontally clips, images, and clip sequences
* Mirror vertically clips, images, and clip sequences
* Adjust the audio volume of a clips and clip sequences [NOT YET]
* Save a single image from a video file
* Save clips as video files

## How To Use This Library
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
