#!/usr/bin/env python3

from pathlib import Path
import sys
import os
import shutil
from typing import List, Optional
import logging

from face.crop_and_resize_images import crop_and_resize_images
from utils import Point, Region, Resolution
from face.video_to_images import extract_frames
from face.crop_ui import run_image_cropper_with_image

RATE = 1
TOP_LEFT = Point(430, 80)
BOTTOM_RIGHT = Point(930, 580)
RESOLUTION = Resolution(224, 224)


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
            shutil.move(source_file_path, destination_file_path)
            logging.debug("Moved %s to %s", filename, destination_path)

    return destination_paths.values()


def data_processing(
    video_dir: Path,
    output_path: Path,
    binary: bool,
    get_frames: Optional[bool] = True,
) -> Path:
    """
    Extracts frames from all videos, then crops them and separates them to the correct directory in the output path.
    """
    logging.basicConfig(level=logging.DEBUG)

    # Get all the video files in the directory
    video_files = [file for file in os.listdir(video_dir) if file.endswith(".mp4")]

    # Extract the frames from each video and get the list of image directories
    image_dirs = []
    for video_file in video_files:
        video_file_path = video_dir / video_file
        image_dir = video_file_path.parent / video_file_path.stem
        if get_frames:
            extract_frames(video_file_path, RATE, image_dir)
        image_dirs.append(image_dir)

    # Crop the images using the UI
    for image_dir in image_dirs:
        logging.debug("Cropping images in %s", image_dir)

        files = sorted(
            [entry.path for entry in os.scandir(image_dir) if entry.is_file()]
        )

        logging.debug("Files: %s", files)

        # Check if the directory is not empty
        if len(files) > 0:
            # Find the midpoint index
            midpoint_index = len(files) // 2

            # Get the file at the midpoint index
            halfway_file = files[midpoint_index]
            logging.debug("Halfway file: %s", halfway_file)
            try:
                run_image_cropper_with_image(image_path=halfway_file)
            except ValueError as e:
                logging.error("Error cropping images: %s", e)
        else:
            logging.error("Error: Directory is empty")

    try:
        separate_images(image_dirs, output_path, binary)
    except FileNotFoundError as e:
        logging.error("Error separating images: %s", e)
    return output_path


if __name__ == "__main__":
    # Convert string arguments to boolean values
    binary = sys.argv[3].lower() == "true"
    get_frames = sys.argv[4].lower() == "true"

    # Call the function with converted boolean values
    data_processing(Path(sys.argv[1]), Path(sys.argv[2]), binary, get_frames)
