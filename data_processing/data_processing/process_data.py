#!/usr/bin/env python3

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
    logging: bool = False,
    plot_matlab: bool = False,
    plot_result: bool = False,
):
    face.process_data(video_dir, output_path, binary_face, get_frames, crop_images, logging)
    pupil.process_data(pupil_dir, plot_matlab, plot_result)

if __name__ == "__main__":
    process_data(Path(sys.argv[1]), Path(sys.argv[1]), Path(sys.argv[2]))
