# Evaluating the Robustness of Deep Neural Networks for Automated Cancer Detection in Endoscopy
This repository contains code for evaluating the robustness of deep neural networks for automated cancer detection in endoscopy.

## Installation
To clone the repository, use the following command:

```
git clone https://github.com/TimJaspers0801/Robustness.git
```
To install the required packages, navigate to the root directory of the repository and run the following command:

```
pip install -r requirements.txt
```
This will install all of the necessary packages listed in the requirements.txt file. Please also make sure you install the ImageMagicWand library:
https://imagemagick.org/script/download.php

## Usage
To generate the TestSet-C dataset, use the following command:
```
python create_testset_c.py 'path/to/testset/images' 'path/to/testset/masks'
```
include the paths to masks if there are present.
