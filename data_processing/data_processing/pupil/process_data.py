#!/usr/bin/env python3

import csv
from dataclasses import dataclass
import numpy as np
import matlab.engine
import matplotlib.pyplot as plt
import os
from pathlib import Path
import pickle
import re
from scipy.interpolate import CubicSpline
import sys
from typing import Dict, List

EXCLUSION_WORDS = ("transition",)

MAT_FILE_FORMAT = "pupil_{}.mat"
DATA_FILE_FORMAT = "data_{}.csv"
SEGMENTS_FILE_FORMAT = "segments_{}.csv"
OUTPUT_FILE_FORMAT = "pupil_{}_{}.pkl"

SEG_NAME_TO_EMOTION = {
    "1.mp4": "joy",
    "2.mp4": "anger",
    "3.mp4": "fear",
    "4.mp4": "fun",
    "5.mp4": "sad",
    "6.mp4": "happy",
    "7.mp4": "calm",
}


@dataclass
class Segment:
    name: str
    start: float
    end: float


def process_participant(
    eng,
    data_dir: Path,
    pupil_file: str,
    inits: str,
    plot_matlab: bool = False,
    plot_result: bool = False,
):
    mat_file = MAT_FILE_FORMAT.format(inits)
    data_file = DATA_FILE_FORMAT.format(inits)
    segments_file = SEGMENTS_FILE_FORMAT.format(inits)
    eng.process_data(
        str(os.path.join(data_dir, "")),
        pupil_file,
        mat_file,
        data_file,
        segments_file,
        plot_matlab,
        nargout=0,
    )

    # Read the segments csv file
    segments: List[Segment] = []
    with open(data_dir / segments_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            segments.append(
                Segment(
                    row["segmentName"],
                    float(row["segmentStart"]) * 1000,
                    float(row["segmentEnd"]) * 1000,
                )
            )

    # Read the data csv file
    curr_seg_idx = 0
    data: Dict[Dict[List[float], List[float]]] = {
        segments[0].name: {"times": [], "diameters": []}
    }
    with open(data_dir / data_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Get the current segment for each time
            time = float(row["times"])
            if time > segments[curr_seg_idx].end:
                curr_seg_idx += 1
                data[segments[curr_seg_idx].name] = {"times": [], "diameters": []}

            # Add the data point to the current segment
            data[segments[curr_seg_idx].name]["times"].append(
                time - segments[curr_seg_idx].start
            )
            data[segments[curr_seg_idx].name]["diameters"].append(
                float(row["diameters"])
            )

    # Write the output csv files
    for seg_name, seg_data in data.items():
        exclude = False
        for word in EXCLUSION_WORDS:
            if word in seg_name:
                exclude = True
                break

        if not exclude:
            output_file = data_dir / OUTPUT_FILE_FORMAT.format(
                inits, SEG_NAME_TO_EMOTION[seg_name.strip()]
            )

            # Cubic smoothing
            cspline = CubicSpline(seg_data["times"], seg_data["diameters"])

            if plot_result:
                plt.clf()
                xnew = np.linspace(0, seg_data["times"][-1], num=1001)
                plt.plot(xnew, cspline(xnew), "o", label="spline")
                plt.plot(
                    seg_data["times"], seg_data["diameters"], "k", label="discrete"
                )
                plt.savefig(f"./{output_file}.png")

            with open(output_file, "wb") as f:
                pickle.dump(cspline, f)


def process_data(
    data_dir: Path,
    plot_matlab: bool = False,
    plot_result: bool = False,
):
    eng = matlab.engine.start_matlab()
    eng.addpath(str(Path(__file__).parent))

    # Iterate over all csv files in the data_dir
    csv_files = {}
    for file in os.listdir(data_dir):
        # If a matching data csv file is found add a new tuple for that participant
        if match := re.search("(?P<inits>\w+)_all_gaze\.csv", Path(file).name):
            csv_files[match["inits"]] = file

    # Iterate over all found csv files
    for inits, csv_file in csv_files.items():
        # Process each participants pupillometry data
        process_participant(eng, data_dir, csv_file, inits, plot_matlab, plot_result)

    # Close the matlab engine
    eng.quit()


if __name__ == "__main__":
    process_data(Path(sys.argv[1]))
