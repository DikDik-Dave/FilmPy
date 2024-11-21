import argparse
import random
import string
import xml.etree.ElementTree as ET

from FilmPy import Editor


def _process_tag_video_clip(video_clip_element):
    """
    Process VideoClip tags

    :param video_clip_element:
    :return:
    """
    # Ensure we have a path
    if 'path' not in video_clip_element.attrib:
        raise AttributeError(f"{video_clip_element} - path attribute must be set for a VideoClip.")

    # Set the clip name, if not provided generate a random
    if 'name' in video_clip_element.attrib:
        clip_name = video_clip_element.attrib['name']
    else:
        clip_name =''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    video_clip = Editor.video_clip(video_path=video_clip_element.attrib['path'])
    for element in video_clip_element:
        # Handle the mirror-x tag
        if element.tag == 'mirror-x':
            video_clip.mirror_x()
        # Handle the mirror-y tag
        if element.tag == 'mirror-y':
            video_clip.mirror_y()
        # Handle the write-video tag
        elif (element.tag == 'write-video') and ('path' not in element.attrib):
            raise AttributeError(f"{element} - path attribute must be set for a write-video")
        elif element.tag == 'write-video':
            video_clip.write_video_file(element.attrib['path'])

    return clip_name, video_clip

def main():
    parser = argparse.ArgumentParser(description='FilmPy Command Line Editor')
    parser.add_argument('script', type=str, help='Your name')
    args = parser.parse_args()
    tree = ET.parse(args.script)
    root = tree.getroot()
    clips = {}
    for element in root:
        if element.tag == 'VideoClip':
            name, clip = _process_tag_video_clip(element)
            clips[name] = clip

if __name__ == '__main__':
    main()