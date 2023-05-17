# Evaluating the Robustness of Deep Neural Networks for Automated Cancer Detection in Endoscopy
ACCPEPTED AT MICCAI 2023! This repository contains code used to create the robustness test sets in the paper 'evaluating the robustness of deep neural networks for automated cancer detection in endoscopy'. The full paper can found in this [link]("aanpassen").
# Abstract
Virtually all endoscopic AI models are developed with clean, high-quality imagery from expert centers, but the clinical data quality is much more heterogeneous. Endoscopic image quality can degrade by e.g. poor lighting, motion blur, and image compression, which have a significant impact on the performance of DNNs. In order to find the limitations of DNNs and provide more robust models for automated cancer
detection, this work evaluates model performance under clinically relevant image degradations. Commonly-used DNN architectures are eval-
uated for various types of degradation, grouped in 3 categories: userdependent corruptions, image acquisition and processing changes, and
artifacts from compression. All corruption levels of severity were calibrated by two clinical research fellows. The results indicate that model
performance already decreases, within clinically relevant regions, up to 35%, 8%, and 40% for user-dependent, image acquisition and processing,
and compression, respectively. Our findings emphasize the significance of including robustness evaluation for DNNs used in endoscopy.

# Results
![Effects of user-dependent image degradation on model performance. The blue
areas indicate the levels of severity expected to be present in expert datasets, while the
green area indicates a clinically relevant amount of degradation. The black dotted line
highlights the reference performance of the ResNet-50 encoder on the original test set.](Images/compression_no_legend.SVG)

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
