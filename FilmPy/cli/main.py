import argparse
import inspect
import logging
import os.path
import random
import string
from inspect import signature
from logging import getLogger
from xml.etree import ElementTree
from ..Editor import Editor
from ..clips import ImageClip, TextClip
from ..clips.Clip import Clip

def _process_tag_clip(clip_element, clip_spec):
    """
    Process Clip tags

    :param clip_element: XML element corresponding to this clip
    :returns name: Name of the clip
    :returns clip: FilmPy clip object
    """
    logger = getLogger(__name__)
    logger.debug(f'Processing {clip_element}')

    # Set the clip name, if not provided generate a random
    if 'name' in clip_element.attrib:
        clip_name = clip_element.attrib['name']
    else:
        clip_name =''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    logger.debug(f'Clip name - {clip_name}')

    # Instantiate the clip
    clip = clip_spec['class'](**clip_element.attrib)

    for method_element in clip_element:
        # Validate that we actually have a method that maps to this tag
        if method_element.tag not in clip_spec['methods'].keys():
            logger.warning(f"{method_element.tag} is not a valid method of {type(clip).__name__}")
            continue

        func = getattr(clip, method_element.tag)
        func(**method_element.attrib)

    return clip_name, clip


def _generate_method_specification():
    """
    Generate a dictionary of method specifications
    :return:
    """
    spec = {}
    filmpy_classes = [Clip, ImageClip, TextClip]

    for fpy_class in filmpy_classes:
        # Build a list of this class and all its parents
        classes_to_check = set()
        classes_to_check.add(fpy_class)
        classes_to_check.update(fpy_class.__bases__)

        # Loop until we get all parent classes (of parent classes)
        while True:
            new_classes_to_check = set()
            for cls in classes_to_check:
                new_classes_to_check.add(cls)
                new_classes_to_check.update(cls.__bases__)

            # Have we added all classes or do we need to check again?
            if len(new_classes_to_check) == len(classes_to_check):
                break
            else:
                classes_to_check = new_classes_to_check

        # Get all methods from the necessary classes
        all_methods = {}
        for cls in classes_to_check:
            for method in inspect.getmembers(cls, predicate=inspect.isfunction):
                if not method[0].startswith('_'):
                    all_methods[method[0]] = inspect.signature(method[1])

        # Add the specification for this class
        spec[fpy_class.__name__] =  {}
        spec[fpy_class.__name__]['class'] = fpy_class
        spec[fpy_class.__name__]['methods'] = all_methods

    # Return the specification
    return spec


def main():
    """
    Main function for the command line interface for FilmPy
    :return:
    """
    logger = getLogger(__name__)

    # Create an argument parser and parse the command line
    parser = argparse.ArgumentParser(description='FilmPy Command Line Editor')
    parser.add_argument('script', type=str, help='FilmPy xml script file path')
    parser.add_argument('--log_level', type=str, help='Application logging level.', default='INFO')

    args = parser.parse_args()

    class_specs = _generate_method_specification()

    # Set the log level to the requested level
    log_level = logging.getLevelNamesMapping()[str.upper(args.log_level)]
    logger.setLevel(log_level)

    # Make sure the script exists
    if not os.path.exists(args.script):
        logger.error(f"'{args.script}' does not exist")
        return

        # Make sure the script exists is a file
    if not os.path.isfile(args.script):
        logger.error(f"'{args.script}' is not a file")
        return

    # Parse the xml document
    logger.debug(f'Parsing {args.script}')
    tree = ElementTree.parse(args.script)
    root = tree.getroot()
    clips = {}
    for element in root:
        # We have some kind of clip tag that needs to be processed
        if (element.tag in class_specs.keys()) and (element.tag.find('Clip') >= 0):
            # print(element.tag)
            name, clip = _process_tag_clip(element, class_specs[element.tag])
            clips[name] = clip

