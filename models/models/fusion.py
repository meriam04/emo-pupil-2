import csv
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
import pickle
from PIL import Image
import re
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import sys
from tensorflow import convert_to_tensor, get_logger, random
from tensorflow.data import AUTOTUNE, Dataset
from tensorflow.keras.utils import img_to_array
from typing import Tuple

from data_processing.face.process_data import BINARY_EMOTIONS, TIMES_FILE_FORMAT
import models.face as face
import models.pupil as pupil

def get_data(pkl_dir: Path, face_dir: Path, image_shape: Tuple[int, int], window_size: int = 100):
    """
    Get the functions from the .pkl files and timestamps from the face directories, then create the dataset.

    Args:
        pkl_dir: The path to the directory of .pkl files containing the pupillometry splines.
        face_dir: The path to the directory of face images (for getting the times files)
        window_size: The number of data samples to be considered at a time.
        batch_size: The batch size to be used in the training.

    Returns:
        The dataset and the label classes.
    """
    # Read the splines from the pkl files
    splines = {}
    for file in os.listdir(pkl_dir):
        # Check if the file is a pkl with the correct format
        if match := re.search(r"pupil_(?P<inits>\w+)_(?P<emotion>\w+).pkl$", str(file)):
            emotion = match["emotion"]
            inits = match["inits"]

            if match["inits"] not in splines:
                splines[match["inits"]] = {}

            with open(pkl_dir / file, 'rb') as f:
                splines[inits][emotion] = pickle.load(f)

    # Generate the dilations_windows, labels, and classes
    names = []
    images = []
    dilation_windows = []
    labels = []
    classes = []
    for i, label in enumerate(os.listdir(face_dir)):
        classes.append(label)
        for inits, init_splines in splines.items():
            for emotion, spline in init_splines.items():
                # Get the times file for this inits + emotion combination
                times_path = face_dir / label / TIMES_FILE_FORMAT.format(inits, emotion)
                if not os.path.isfile(times_path):
                    continue

                with open(times_path, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Check if a window can be generated for this time
                        end_time = float(row["times"])
                        if end_time < pupil.PERIOD * window_size:
                            continue

                        # Construct the image name
                        name = f"{inits}_{emotion}_{end_time}_c.png"
                        names.append(name)

                        # Get the image for the time
                        image = Image.open(face_dir / label / name)
                        image = image.resize(image_shape)
                        images.append(img_to_array(image))

                        # Generate a window for this time
                        times = np.linspace(end_time - pupil.PERIOD * window_size, end_time, window_size)
                        dilation_windows.append(spline(times))
                        labels.append(i)

    # Convert the dilations and labels to a tensor dataset
    names_t = convert_to_tensor(names)
    images_t = convert_to_tensor(images)
    dilations_t = convert_to_tensor(dilation_windows)
    labels_t = convert_to_tensor(labels)
    dataset = Dataset.from_tensor_slices((names_t, images_t, dilations_t, labels_t))

    # Prefetch datasets
    dataset = dataset.batch(1).cache().shuffle(1000).prefetch(AUTOTUNE)

    return dataset, classes

def create_confusion_matrix(labels, predictions, classes):
    cm = confusion_matrix(labels, predictions)
    disp = ConfusionMatrixDisplay(cm, display_labels=classes)
    disp.plot()
    plt.title("Confusion Matrix")
    plt.savefig(Path(__file__).parent / 'confusion_matrix.png')

if __name__ == "__main__":
    # Disable annoying tensorflow warnings
    get_logger().setLevel('ERROR')

    # Fix random seed for reproducibility
    random.set_seed(496)

    window_size = 100
    image_shape = (224, 224, 1)

    # Get the dataset and classes
    test_set, classes = get_data(Path(sys.argv[1]), Path(sys.argv[2]), image_shape[0:2], window_size)

    input_shape = (window_size, 1)
    num_classes = len(classes)

    # Create the models
    face_model = face.create_model(num_classes, image_shape)
    pupil_model = pupil.create_model(2, input_shape)

    # Load the weights
    face_model.load_weights(face.BINARY_CHECKPOINT_PATH if len(classes) == 2 else face.MULTICLASS_CHECKPOINT_PATH).expect_partial()
    pupil_model.load_weights(pupil.CHECKPOINT_PATH).expect_partial()

    # Get the accuracy on the test set
    correct = 0
    labels = []
    predictions = []
    prediction_classes = set()
    for image_name, face_image, pupil_window, label in test_set:
        face_prediction = face_model.predict(face_image, verbose=None)
        pupil_prediction = pupil_model.predict(pupil_window, verbose=None)

        if len(classes) != 2:
            multiclass_pupil_prediction = []
            for v in BINARY_EMOTIONS.values():
                if v == "negative":
                    multiclass_pupil_prediction.append(pupil_prediction[0][0])
                else:
                    multiclass_pupil_prediction.append(pupil_prediction[0][1])
            pupil_prediction = multiclass_pupil_prediction

        # Check that the label matches the emotion with the highest probability
        prediction = np.argmax(face_prediction + pupil_prediction)
        labels.append(label)
        predictions.append(prediction)
        prediction_classes.add(classes[label[0]])
        prediction_classes.add(classes[prediction])
        if prediction == label:
            correct += 1
        
        print(f"Predicted {classes[prediction]} for {image_name.numpy()[0].decode('ascii')}")

    print(f"Test accuracy: {correct/len(test_set)}")
    create_confusion_matrix(labels, predictions, sorted(prediction_classes))
