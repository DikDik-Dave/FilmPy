# FilmPy
FilmPy is a python module for film editing. 
Its goal is to enable fully video and audio editing. 

## Main Functionality
By using FilmPy you will be able to 
* Add static image overlays to a video clip [NOT YET]
* Compile various clips into a video and save it 
* Create composite video clips [NOT YET]
* Rotate a video
* Flip a video (left to right or top to bottom) [NOT YET]

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
