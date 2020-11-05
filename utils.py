import os
import shutil
import numpy as np
import imghdr  # for checking images are valid
from shutil import rmtree
import random
from collections import defaultdict
from natsort import natsorted

def get_immediate_directories(directory_path):
    """
    Example:
    ```
    >>> print(get_immediate_directories('./data'))
    [...]
    ```
    """
    
    # Only get directories (no files)
    dirs = next(os.walk(directory_path))[1]

    return dirs


def get_immediate_images(directory_path, extension='png'):
    """
    Example:
    ```
    >>> print(get_immediate_images('./data'))
    [...]
    ```
    """

    # Only get valid images
    imgs = [i for i in os.listdir(directory_path) if image_is_valid(os.path.join(directory_path, i), extension=extension)]

    return imgs


def get_label_sequence_from_name(name):
    """
    Gets a label for the images from the name of the directory
    Example name: "20160805_g1k17-08-05-2016_16-25-43_idx99_BLO"
    
    ```
    >>> print(get_label_from_name("20160805_g1k17-08-05-2016_16-25-43_idx99_BLO"))
    "BLO"
    ```
    """
    removed_extension = name.split(".")[0]
    label = removed_extension[-3:]
    sequence = removed_extension[:-4]  # drops the _BLO
    return label, sequence

def get_split(test=0.15, val=0.15):
    """
    Returns whether to put something in 'train', 'test', or 'val'
    using a random number generator. Specify test and validation size. 
    Train size will be everything else.
    - test: percentage of test [0-1.0]
    - val: percentage of validation [0, 1.0]
    """
    train_upper_bound = 1.0 - test - val
    test_upper_bound = train_upper_bound + test

    x = np.random.rand()

    if x < train_upper_bound:
        return 'train'
    elif x < test_upper_bound:
        return 'test'
    return 'val'

def image_is_valid(path_to_image, extension='png'):
    """
    Returns True if the image is valid. False otherwise
    """
    return imghdr.what(path_to_image) == extension

def rm_mkdir(directory_name):
    """
    Helper function to remove the contents of a directory and re-create an empty one
    """

    if os.path.exists(directory_name):
        # Remove the existing folder to get rid of old contents
        rmtree(directory_name)
    os.mkdir(directory_name)


def get_paths_for_image_sequences(difficulties):
    """
    Gets the path for the images per sequence

    - difficulties: an instance of DifficultyLevels (difficulty_level.py)
    
    Will return a dictionary per_class_image_sequences of form:
        {
            <label>: {
                <sequence>: {
                    difficulty: 'E', // 'E', 'M', 'H'
                    image_paths: [...],
                    split: "train", // "train", "test", "val"
                },
                <sequence>: {
                    difficulty: 'E', // 'E', 'M', 'H'
                    image_paths: [...],
                    split: "val",
                },
            },
            <label>: {
                // ...
            },
        }
    """
    # Ensure the results are reproducable
    random.seed(0)

    per_class_image_sequences = defaultdict(lambda: defaultdict(dict))

    # Footage directories
    footage_dirs = get_immediate_directories('./data')

    for f_dir in footage_dirs:
        # These are folders corresponding to each class
        path_1 = os.path.join('./data', f_dir)
        f_class_dirs = get_immediate_directories(path_1)

        # Loop through all sequence dirs of form Footage_name_XXX_DDD
        # ex. 20160805_g1k17-08-05-2016_15-57-59_idx99_BOO
        for f_class_dir in f_class_dirs:
            # The label of the class ex. "BLO"
            class_label, _ = get_label_sequence_from_name(f_class_dir)

            path_2 = os.path.join(path_1, f_class_dir)
            footage_sequence_dirs = get_immediate_directories(path_2)

            # Loop through the individual sequences
            # footage_sequence_dir can be of form 20160805_g1k17-08-05-2016_15-57-59_idx99_BOO_00023411
            for footage_sequence_dir in footage_sequence_dirs:
                path_3 = os.path.join(
                    path_2, footage_sequence_dir, "light_mask")

                difficulty_level = difficulties.get_difficulty_level(
                    footage_sequence_dir)

                # Save the difficulty level
                per_class_image_sequences[class_label][footage_sequence_dir]["difficulty"] = difficulty_level
                per_class_image_sequences[class_label][footage_sequence_dir]["split"] = get_split(
                )

                # Get the images
                image_names = get_immediate_images(path_3)
                image_names = [os.path.join(path_3, i) for i in image_names]

                # Save all the valid image paths
                per_class_image_sequences[class_label][footage_sequence_dir]["image_paths"] = image_names

    return per_class_image_sequences

def labels_to_ints(labels, csv_output):
    """
    Receives a list of string labels, sorts them, and returns a dictionary
    mapping the labels to an int id.
    """
    # Sort naturally
    labels = natsorted(labels)
    return {label: idx for idx, label in enumerate(labels)}