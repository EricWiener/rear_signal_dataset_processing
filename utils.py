import os
import shutil
import numpy as np
import imghdr  # for checking images are valid
from shutil import rmtree

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
