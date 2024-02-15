#!/usr/bin/env python3

from pathlib import Path
import sys
import os
import shutil
from typing import List
import logging

from face.crop_and_resize_images import crop_and_resize_images
from utils import Point, Region, Resolution
from face.video_to_images import extract_frames

# If we are making a UI, return these values for TOP_LEFT and BOTTOM_RIGHT
RATE = 1
TOP_LEFT = Point(430, 80)
BOTTOM_RIGHT = Point(930, 580)
RESOLUTION = Resolution(224, 224)
# Add FILE_LIST as global variable


def data_processing(video_path: Path, output_path: Path) -> List[Path]:
    """Extracts frames from a video and crops and resizes them to a specified resolution."""
    image_paths = extract_frames(video_path, RATE, output_path)
    return crop_and_resize_images(
        image_paths, Region(TOP_LEFT, BOTTOM_RIGHT), RESOLUTION
    )


if __name__ == "__main__":
    data_processing(Path(sys.argv[1]), Path(sys.argv[2]))


def separate_images(source_dirs, output_dir, binary=False):
    """
    Takes in a list of source folders and separates the images into folders based on emotions.
    Each source folder should contain a 'cropped' directory with the images to be copied.
    """
    emotions_binary = {
        "positive": ["happy", "fun", "calm", "joy"],
        "negative": ["anger", "sad", "fear"],
    }

    emotions_multiple = ["happy", "fun", "calm", "joy", "anger", "sad", "fear"]

    for source_dir in source_dirs:
        if not os.path.exists(source_dir):
            raise FileNotFoundError(
                "Source folder {} does not exist".format(source_dir)
            )

    if binary:
        emotions = emotions_binary
    else:
        emotions = {emotion: [emotion] for emotion in emotions_multiple}

    destination_paths = {}

    for emotion_category, _ in emotions.items():
        destination_path = Path(output_dir) / emotion_category
        destination_paths[emotion_category] = destination_path

        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

    for source_dir in source_dirs:
        logging.debug("Source folder: %s", source_dir)

        if "cropped" not in os.listdir(source_dir):
            raise FileNotFoundError(
                "Source folder does not contain a 'cropped' directory, skipping."
            )

        crop_dir = os.path.join(source_dir, "cropped")

        matched_emotion = None
        for emotion in emotions:
            if any(keyword in str(source_dir) for keyword in emotions[emotion]):
                matched_emotion = emotion
                break

        if matched_emotion:
            destination_path = destination_paths[matched_emotion]
            logging.debug("Keyword matched: %s", matched_emotion)
        else:
            logging.debug(
                "Folder %s does not match any emotion, skipping.",
                source_dir,
            )
            continue

        files = os.listdir(crop_dir)
        for filename in files:
            source_file_path = os.path.join(crop_dir, filename)
            destination_file_path = os.path.join(destination_path, filename)
            shutil.copy(source_file_path, destination_file_path)
            logging.debug("Moved %s to %s", filename, destination_path)

    return destination_paths.values()


# def separate_images_binary(source_dirs, output_dir):
#     """
#     Takes in a list of source folders and separates the images into positive and negative folders
#     based on the emotion keyword in the source folder name.
#     Each source folder should contain a 'cropped' directory with the images to be copied.
#     """
#     for source_dir in source_dirs:
#         if not os.path.exists(source_dir):
#             raise FileNotFoundError(
#                 "Source folder {} does not exist".format(source_dir)
#             )

#     positive_dir = Path(output_dir) / "positive"
#     negative_dir = Path(output_dir) / "negative"

#     if not os.path.exists(positive_dir):
#         os.makedirs(positive_dir)
#     if not os.path.exists(negative_dir):
#         os.makedirs(negative_dir)

#     positive_keywords = ["happy", "fun", "calm", "joy"]
#     negative_keywords = ["anger", "sad", "fear"]

#     for source_dir in source_dirs:
#         logging.debug("Source folder: %s", source_dir)

#         # make sure the source folder contains 'cropped' in its subdirectories
#         if "cropped" not in os.listdir(source_dir):
#             raise FileNotFoundError(
#                 "Source folder does not contain a 'cropped' directory, skipping."
#             )

#         crop_dir = os.path.join(source_dir, "cropped")

#         # check if the source folder name contains an emotion keyword
#         if any(keyword in str(source_dir) for keyword in positive_keywords):
#             destination_path = positive_dir
#             logging.debug("Keyword matched: Positive")
#         elif any(keyword in str(source_dir) for keyword in negative_keywords):
#             destination_path = negative_dir
#             logging.debug("Keyword matched: Negative")
#         else:
#             logging.debug(
#                 "Folder %s does not match positive or negative criteria, skipping.",
#                 source_dir,
#             )

#         # Move all files from the cropped folder to the appropriate destination folder
#         files = os.listdir(crop_dir)
#         for filename in files:
#             source_file_path = os.path.join(crop_dir, filename)
#             destination_file_path = os.path.join(destination_path, filename)
#             shutil.copy(source_file_path, destination_file_path)
#             logging.debug("Moved %s to %s", filename, destination_path)

#     return positive_dir, negative_dir


# def separate_images_multiple(source_dirs, output_dir):
#     """
#     Takes in a list of source folders and separates the images into folders for each emotion.
#     Each source folder should contain a 'cropped' directory with the images to be copied.
#     """
#     for source_dir in source_dirs:
#         if not os.path.exists(source_dir):
#             raise FileNotFoundError(
#                 "Source folder {} does not exist".format(source_dir)
#             )

#     emotions = ["happy", "fun", "calm", "joy", "anger", "sad", "fear"]

#     destination_paths = []
#     for source_dir in source_dirs:
#         logging.debug("Source folder: %s", source_dir)

#         # make sure the source folder contains 'cropped' in its subdirectories
#         if "cropped" not in os.listdir(source_dir):
#             raise FileNotFoundError(
#                 "Source folder does not contain a 'cropped' directory, skipping."
#             )

#         crop_dir = os.path.join(source_dir, "cropped")

#         # Initialize variable to store matched emotion
#         matched_emotion = None

#         # Check if the source folder name contains an emotion keyword
#         for emotion in emotions:
#             if emotion in str(source_dir):
#                 matched_emotion = emotion
#                 break

#         if matched_emotion:
#             destination_path = Path(output_dir) / matched_emotion
#             destination_paths.append(destination_path)
#             logging.debug("Keyword matched: %s", matched_emotion)
#         else:
#             logging.debug(
#                 "Folder %s does not match any emotion, skipping.",
#                 source_dir,
#             )

#         # Move all files from the cropped folder to the appropriate destination folder
#         files = os.listdir(crop_dir)
#         for filename in files:
#             source_file_path = os.path.join(crop_dir, filename)
#             if not os.path.exists(destination_path):
#                 os.makedirs(destination_path, exist_ok=True)
#             destination_file_path = os.path.join(destination_path, filename)
#             shutil.copy(source_file_path, destination_file_path)
#             logging.debug("Moved %s to %s", filename, destination_path)

#     return destination_paths
