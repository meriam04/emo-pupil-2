#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys

import data_processing.face as face
import data_processing.pupil as pupil


def process_data(
    video_dir: Path,
    output_path: Path,
    pupil_dir: Path,
    binary_face: bool = False,
    get_frames: bool = True,
    crop_images: bool = True,
    log: bool = False,
    plot_matlab: bool = False,
    plot_result: bool = False,
):
    face.process_data(video_dir, output_path, binary_face, get_frames, crop_images, log)
    pupil.process_data(pupil_dir, plot_matlab, plot_result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process video and pupil data.")
    parser.add_argument(
        "video_dir", type=Path, help="Input directory containing videos."
    )
    parser.add_argument(
        "output_path",
        type=Path,
        help="Output path where train/val/test directories will be created.",
    )
    parser.add_argument(
        "pupil_dir", type=Path, help="Input directory containing pupil data."
    )
    parser.add_argument(
        "-b",
        "--binary-face",
        action="store_true",
        help="Whether to use binary face mode.",
    )
    parser.add_argument(
        "-f", "--get-frames", action="store_true", help="Whether to get frames."
    )
    parser.add_argument(
        "-c", "--crop-images", action="store_true", help="Whether to crop images."
    )
    parser.add_argument(
        "-l", "--log", action="store_true", help="Whether to enable logging."
    )
    parser.add_argument(
        "-m",
        "--plot-matlab",
        action="store_true",
        help="Whether to plot the data with Matlab.",
    )
    parser.add_argument(
        "-r", "--plot-result", action="store_true", help="Whether to plot results."
    )
    args = parser.parse_args()

    # Call the function with parsed arguments
    process_data(
        args.video_dir,
        args.output_path,
        args.pupil_dir,
        args.binary_face,
        args.get_frames,
        args.crop_images,
        args.log,
        args.plot_matlab,
        args.plot_result,
    )
