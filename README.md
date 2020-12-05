This repository contains scripts to help process the [Vehicle Rear Signal Dataset](http://vllab1.ucmerced.edu/~hhsu22/rear_signal/rear_signal#) provided by UC Merced.

# Notebooks
### process_rear_signal_dataset.ipynb
This notebook will extract a single frame from every sequence to use for training. This is useful for creating datasets for one-shot models.

Output Dataset folder structure:
One image from every sequence is moved into a directory corresponding to that sequence's label
```
|_ BLO
|  |_ frame_000001.png
|  |_ frame_000002.png
|  |_ ...
|_ BLR
|  |_ frame_000001.png
|  |_ frame_000002.png
|  |_ ...
|_ ...
```

### process_rear_signal_dataset_sequences.ipynb
This notebook is used to organize the data in such a way that it can be used for training models that handle sequences of data (LSTM, SlowFast, ResNet3D, etc).

Output Dataset folder structure:
```
|_ frames
|  |_ [video name 0]
|  |  |_ frame_000001.jpg
|  |  |_ frame_000002.jpg
|  |  |_ ...
|  |_ [video name 1]
|     |_ frame_000001.jpg
|     |_ frame_000002.jpg
|     |_ ...
|_ train.csv
|_ test.csv
|_ val.csv
|_ label_to_id.pickle (maps from label string -> class id #)
```

# Dataset Description
----------------------------------------------------------------------------------------------------------------
This dataset contains time-sequence images of different vehicle rears under various real-world road conditions.
Each image frame of the sequence is the vehicle rear cropped mannually from the raw video.
Every sequence is categorized into 8 classes regarding to the status of the rear lights (brake and turn lights).
----------------------------------------------------------------------------------------------------------------

### Class definition

This data set includes sequences labeled with a total of 8 distinct classes for all possible rear signal states. 
Each state is denoted by 3 letters: B (brake), L (left), and R (right).
We give either the corresponding letter of the signal when it is on, or a letter O for off.
Consequently, there will be 8 different states:
OOO: Brake light and turn signals off
BOO: Brake light on, turn signals off
OLO: Brake light off, left signal on
BLO: Brake light on, left signal on
OOR: Brake light off, right signal on
BOR: Brake light on, right signal on
OLR: Brake light off, left and right signal on (hazard warning light on)
BLR: Brake light on, left and right signal on (hazard warning light on)

### Folder structure
-rear_signal_dataset
   -Footage_name
      -Footage_name_XXX
         -Footage_name_XXX_DDD (sequence of class XXX starting from frame number DDD)
            -light_mask
               -frameDDDDDDDD.png (frames with a 8 digit number indicating the frame number)
               -...
         -Footage_name_XXX_DDD
            -light_mask
               -frameDDDDDDDD.png
               -...
      -Footage_name_XXX
         -Footage_name_XXX_DDD
            -...
         -Footage_name_XXX_DDD
            -...
         -Footage_name_XXX_DDD
            -...
   -Footage_name
      -...
*XXX indicates the label of the signal


### Dataset statistics

Total sequences: 649
Total frames: 63637

Number of sequences in each class:
OOO: 188 BOO: 211 OLO: 78 BLO: 63
OOR:  58 BOR:  33 OLR:  9 BLR:  9

Number of frames in each class:
OOO: 21867 BOO: 17874 OLO: 6271 BLO: 6380
OOR:  4728 BOR:  3527 OLR: 1600 BLR: 1390

### Level of difficulty

There is three levels of difficulty for this dataset: Easy, Moderate and Hard.
There are three .txt files repectively documenting the sequence folder names(e.g. 20160805_g1k17-08-05-2016_15-57-59_idx99_BOO_00002671) in that specific level.