# Evaluating Robustness of Deep Neural Networks for Automated Cancer Detection in Endoscopy
\
This repository contains code used to create the robustness test set used in the following publication:

- [Tim J.M. Jaspers *et al.*](https://link.springer.com/chapter/10.1007/978-3-031-47076-9_4) - Investigating the Impact of Image Quality on Endoscopic AI Model Performance (*Second Workshop on Applications of Medical AI (AMAI) - Satellite Event MICCAI 2023*)

- Tim J.M. Jaspers *et al.* - Robustness evaluation of deep neural networks for endoscopic image analysis: insights
and strategies *(Currently under Review)* 

# Abstract
Computer-aided detection and diagnosis systems (CADe/CADx) in endoscopy are commonly trained using high-quality imagery, which is not representative for the heterogeneous input typically encountered in clinical practice. In endoscopy,
the image quality heavily relies on both the skills and experience of the endoscopist and the specifications of the system used for screening. Factors such as poor illumination, motion blur, and specific post-processing settings can
significantly alter the quality and general appearance of these images. This so-called domain gap between the data used for de-
veloping the system and the data it encounters after deployment, and the impact it has on the performance of deep neural networks (DNNs) 
supportive endoscopic CAD systems remains largely unexplored. As many of such systems, for e.g. polyp detection,
are already being rolled out in clinical practice, this poses severe patient risks in particularly community hospitals,
where both the imaging equipment and experience are
subject to considerable variation. Therefore, this study aims to evaluate the impact of
this domain gap on the clinical performance of CADe/CADx for various endoscopic
applications. For this, we leverage two publicly available data sets (KVASIR-SEG and
GIANA) and two in-house data sets. We investigate the performance of commonly-used
DNN architectures under synthetic, clinically calibrated image degradations and on a
prospectively collected dataset including 342 endoscopic images of lower subjective
quality. Additionally, we assess the influence of DNN architecture and complexity, data
augmentation, and pretraining techniques for improved robustness. The results reveal
a considerable decline in performance of 11.6% (±1.5) as compared to the reference,
within the clinically calibrated boundaries of image degradations. Nevertheless, employing more advanced DNN architectures and self-supervised in-domain pre-training
effectively mitigate this drop to 7.7% (±2.03). Additionally, these enhancements yield
the highest performance on the manually collected test set including images with lower
subjective quality. By comprehensively assessing the robustness of popular DNN architectures and training strategies across multiple datasets, this study provides valuable in-
sights into their performance and limitations for endoscopic applications. The findings
highlight the importance of including robustness evaluation when developing DNNs for
endoscopy applications and propose strategies to mitigate performance loss.

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
The purpose of the robustness test set is created to evaluate endoscopic models using more heterogeneous data by 
incorporating the aforementioned corruptions. In the original paper, we included corruptions
up to severity level 5, as they are clinically calibrated and still realistic at that level. The paper revealed a performance drop of up to **14%** on the robustness test set.\
\
An other option could be to only evaluated upto severity level 2, which represent the amount of image degradation
expected in 'expert level' datasets. Alternatively, for those seeking to assess robustness in extreme scenarios, the evaluation could extend to severity levels 8, 9, and 10.\
\
To generate the Robustness test set, use the following command:

```
python create_robustness_set.py 'path/to/testset/images' path_masks='path/to/testset/Masks'  max_level=5, min_level=1 nb_iterations=5 include_compression=True
```
include the paths to masks if there are present. *nb_iterations* denotes the number of iterations the original test set is looped over.
In the original paper, the test set was corrupted a total of 5 times. The robustness after waiting for a while corrupted images can be found in the 'robustness test set' folder.

![FIG 5.](Images/R5T.png)
**Fig 4.** *Random examples included in the robustness test set.*


## Citation
If you find our work useful in your research please consider citing our paper:
```
@InProceedings{IQimpact2024,
author="Jaspers, Tim J. M. and Boers, Tim G. W. and Kusters, Carolus H. J. and Jong, Martijn R. and Jukema, Jelmer B. and de Groof, Albert J. and Bergman, Jacques J. and de With, Peter H. N. and van der Sommen, Fons"
title="Investigating the Impact of Image Quality on Endoscopic AI Model Performance",
booktitle="Applications of Medical Artificial Intelligence",
year="2024",
publisher="Springer Nature Switzerland",
pages="32--41",
isbn="978-3-031-47076-9"
}
```

## Acknowledgments 






