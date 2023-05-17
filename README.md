# Evaluating Robustness of Deep Neural Networks for Automated Cancer Detection in Endoscopy
ACCPEPTED AT MICCAI 2023! \
\
This repository contains code used to create the robustness test set in the paper 'Evaluating Robustness of Deep Neural Networks for Automated Cancer Detection in Endoscopy'. The full paper can found in this [link]("aanpassen").
# Abstract
Virtually all endoscopic AI models are developed with clean, high-quality imagery from expert centers, but the clinical data quality is much more heterogeneous. Endoscopic image quality can degrade by e.g. poor lighting, motion blur, and image compression, which have a significant impact on the performance of DNNs. In order to find the limitations of DNNs and provide more robust models for automated cancer
detection, this work evaluates model performance under clinically relevant image degradations. Commonly-used DNN architectures are eval-
uated for various types of degradation, grouped in 3 categories: userdependent corruptions, image acquisition and processing changes, and
artifacts from compression. All corruption levels of severity were calibrated by two clinical research fellows. The results indicate that model
performance already decreases, within clinically relevant regions, up to 35%, 8%, and 40% for user-dependent, image acquisition and processing,
and compression, respectively. Our findings emphasize the significance of including robustness evaluation for DNNs used in endoscopy.

# Results
The figures below show the effect of individual image degradations at different severity levels. All corruptions are included to create the R5-test set (all corruptions with severity level upt to 5).
\
\
![FIG 1.](Images/user_dependent.png)
**Fig 1.** *Effects of user-dependent image degradation on model performance. The blue
areas indicate the levels of severity expected to be present in expert datasets, while the
green area indicates a clinically relevant amount of degradation. The black dotted line
highlights the reference performance of the ResNet-50 encoder on the original test set.*

![FIG 2.](Images/processing.png)
**Fig 2.** *Effects of changes in image acquisition and processing on model performance.*

![FIG 3.](Images/compression.png)
**Fig 3.** *Effects of changes in image acquisition and processing on model performance.*

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

## Create Robustness test set
The robustness test set is meant to evalate endoscopic models on more hetrogeneus data by applying the above mentioned corruptions. In the orignal paper we only include corruptions
upto severity level 5 since they are clincally calibrated and at level 5 still realistic. In the paper model performance dropped up to 14% on the robustness test set. \
\
To generate the Robustness test set, use the following command:

```
python create_testset_c.py 'path/to/testset/images' 'path/to/testset/masks'
```
include the paths to masks if there are present.

![FIG 5.](Images/R5T.png)
**Fig 4.** *Random examples included in the robustness test set.*




