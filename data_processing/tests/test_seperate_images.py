import os
import pytest
from pathlib import Path
import logging
from ..data_processing import separate_images_binary, separate_images_multiple
from ..crop_and_resize_images import crop_and_resize_image, crop_and_resize_images
from ..utils import Point, Region, Resolution

test_files_dir = Path(__file__).parent / "test_files" / "separate_images"


@pytest.fixture(autouse=True)
def set_logging_level(caplog):
    # Set logging level to capture debug messages
    caplog.set_level(logging.DEBUG)


def setup_test_folders(setup_folders):
    """
    Create test directories and populate them with dummy image values.
    """
    for folder in setup_folders:
        os.makedirs(folder / "cropped", exist_ok=True)
        emotion_name = folder.stem.split("_")[
            1
        ]  # Extract emotion name from folder name
        # Create dummy image files with emotion name
        for i in range(5):
            with open(folder / f"cropped/image_{i}_{emotion_name}.jpg", "w") as f:
                f.write("Dummy image data")


@pytest.mark.parametrize(
    "setup_folders, output_folders",
    [
        (
            [
                test_files_dir / "test_happy",
                test_files_dir / "test_sad",
                test_files_dir / "test_fear",
                test_files_dir / "test_anger",
                test_files_dir / "test_fun",
                test_files_dir / "test_calm",
                test_files_dir / "test_joy",
            ],
            test_files_dir,
        ),
    ],
)
def test_separate_images_binary(setup_folders, output_folders, caplog):

    # Call the setup_test_folders function to prepare test directories
    setup_test_folders(setup_folders)

    # Set logging level to capture debug messages
    caplog.set_level(logging.DEBUG)

    positive_dir, negative_dir = separate_images_binary(setup_folders, output_folders)

    # Assert that files are moved correctly to positive and negative folders
    assert positive_dir.exists() and positive_dir.is_dir()
    assert negative_dir.exists() and negative_dir.is_dir()

    # Ensure the files were correctly moved
    assert len(os.listdir(positive_dir)) > 0
    assert len(os.listdir(negative_dir)) > 0

    # Ensure the files weren't deleted from source folders
    for folder in setup_folders:
        assert len(os.listdir(folder / "cropped")) > 0

    # Ensure that all files were moved to the correct folders
    positive_keywords = ["happy", "fun", "calm", "joy"]
    negative_keywords = ["anger", "sad", "fear"]

    for folder in setup_folders:
        for file in os.listdir(folder / "cropped"):
            if any(keyword in file for keyword in positive_keywords):
                assert (positive_dir / file).exists()
            elif any(keyword in file for keyword in negative_keywords):
                assert (negative_dir / file).exists()
            else:
                assert False, f"File {file} was not moved to the correct folder."

    # Ensure that positive folder contains no negative keyword images
    for file in os.listdir(positive_dir):
        assert not any(keyword in file for keyword in negative_keywords)

    for file in os.listdir(negative_dir):
        assert not any(keyword in file for keyword in positive_keywords)


# def test_separate_images_multiple(setup_folders):
#     source_folder, _, _, output_folders, keywords = setup_folders
#     separate_images_multiple(source_folder, output_folders, keywords)

#     # Assert that files are moved correctly to output folders
#     for folder in output_folders:
#         assert len(os.listdir(folder)) > 0


# #Make sure to replace your_module with the actual name of the module where your separate_images_binary and separate_images_multiple functions are defined.

# #These tests use the pytest library and fixtures to set up a temporary folder structure for testing. The test_separate_images_binary and test_separate_images_multiple functions then call your separation functions and assert that the files are moved correctly.

# #You can run the tests by executing the pytest command in your terminal, assuming you have pytest installed (pip install pytest).

# import os
# import shutil
# import pytest
# import logging
# from pathlib import Path
# from ..data_processing import separate_images_binary, separate_images_multiple

# # Define test data directories
# TEST_FILES_DIR = Path(__file__).parent / "test_files"
# SOURCE_FOLDER = TEST_FILES_DIR / "source"
# POSITIVE_FOLDER = TEST_FILES_DIR / "positive"
# NEGATIVE_FOLDER = TEST_FILES_DIR / "negative"
# OUTPUT_FOLDERS = [
#     TEST_FILES_DIR / "output" / "anger",
#     TEST_FILES_DIR / "output" / "sad",
#     TEST_FILES_DIR / "output" / "fear",
#     TEST_FILES_DIR / "output" / "happy",
#     TEST_FILES_DIR / "output" / "fun",
#     TEST_FILES_DIR / "output" / "calm",
#     TEST_FILES_DIR / "output" / "joy",
# ]
# KEYWORDS = ["anger", "sad", "fear", "happy", "fun", "calm", "joy"]


# @pytest.fixture
# def setup_test_data():
#     # Create test directories and files
#     os.makedirs(SOURCE_FOLDER, exist_ok=True)
#     os.makedirs(POSITIVE_FOLDER, exist_ok=True)
#     os.makedirs(NEGATIVE_FOLDER, exist_ok=True)
#     for folder in OUTPUT_FOLDERS:
#         os.makedirs(folder, exist_ok=True)

#     yield  # This is where the test runs

#     # Cleanup after the test
#     shutil.rmtree(SOURCE_FOLDER)
#     shutil.rmtree(POSITIVE_FOLDER)
#     shutil.rmtree(NEGATIVE_FOLDER)
#     for folder in OUTPUT_FOLDERS:
#         shutil.rmtree(folder)


# def test_separate_images_binary(setup_test_data):

#     separate_images_binary(SOURCE_FOLDER, POSITIVE_FOLDER, NEGATIVE_FOLDER, "happy")
#     # Debugging: Print out the contents of POSITIVE_FOLDER
#     print("Contents of POSITIVE_FOLDER:", os.listdir(POSITIVE_FOLDER))

#     # Assert that files are moved correctly to positive and negative folders
#     assert len(os.listdir(POSITIVE_FOLDER)) > 0
#     assert len(os.listdir(NEGATIVE_FOLDER)) > 0

#     # Check if SOURCE_FOLDER contains a folder named "cropped"
#     assert "cropped" in os.listdir(SOURCE_FOLDER)


# def test_separate_images_multiple(setup_test_data):
#     separate_images_multiple(SOURCE_FOLDER, OUTPUT_FOLDERS, KEYWORDS)
#     # Assert that files are moved correctly to output folders
#     for folder in OUTPUT_FOLDERS:
#         assert len(os.listdir(folder)) > 0

#     # Check if SOURCE_FOLDER contains a folder named "cropped"
#     assert "cropped" in os.listdir(SOURCE_FOLDER)
