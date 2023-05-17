import os
from utils import define_corruption
import random
from utils import Compose, combine_paths
from PIL import Image
import pandas as pd
import sys

random.seed(0)


def create_testset_c(path_images, path_masks=None, max_levels=5, min_level=1, nb_iterations=5, include_compression=False):
    """read images and check imagesize"""
    cwd = os.getcwd()
    images = os.listdir(path_images)

    """
    we create an excel file to link all corrupted images to the original ones to link them later with the correct label
    """
    df = pd.DataFrame()

    print('total number of images in folder = ' + str(len(images)))
    path_images = combine_paths(path_images, images)

    """perturbations"""
    corruption_options = ['Motion-blur', 'Overexposure', 'defocus-blur', 'Hue','Saturation', 'Contrast', 'Sharpness', 'Brightness']

    if include_compression == True:
        corruptions_compression = ['Resolution', 'JPG', 'JPEG2000']
        corruption_options.extend(corruptions_compression)

    factor_1 = list(range(1+min_level, max_levels+1))
    factor_2 = list(range(11-max_levels, 11-min_level))+list(range(11+min_level,11+max_levels))

    # save dir
    path_save_images = os.path.join(cwd, 'Testset-C/Images')
    os.makedirs(path_save_images, exist_ok=True)

    #store image names and corrupted image names
    images_clean_total = []
    images_corruption_total = []

    if os.path.exists(path_masks) is True:
        path_save_masks = os.path.join(cwd, 'Testset-C/Masks')
        os.makedirs(path_save_masks, exist_ok=True)

        masks = os.listdir(path_masks)
        path_masks = combine_paths(path_masks, masks)

        if len(path_masks) != len(path_images):
            AttributeError('not the same amount of images and masks')

    # apply corruptions
    nb_it = nb_iterations  # number of iteration over testset
    nb_corruptions = 5  # maximum number of corruptions per images

    for i in list(range(nb_it)):
        names = []
        images_clean = []
        for k in range(len(path_images)):
            '''resize images to 1024x1024'''

            image = Image.open(path_images[k]).convert('RGB')
            image = image.resize((1024, 1024), resample=Image.LANCZOS)

            p = random.random()

            if p < 3/11:
                nb_corruptions = nb_corruptions - 1


            nb_corruptions = random.randint(1, nb_corruptions)  #random number of corruptions for image
            idx_corruptions = random.sample(range(0, len(corruption_options - 3)), nb_corruptions)  #random chosen corruption

            if include_compression is True and p < 3/11:
                idx_corruptions.extend(random.randint(range(len(corruption_options - 3)), len(corruption_options - 3)))

            corruptions = list()
            corruptions_names = list()
            factors = list()

            # create list with all perturbations
            for nb in range(nb_corruptions):
                # append perturbation to transform
                corruption = corruption_options[idx_corruptions[nb]]
                corruptions_names.append(corruption)

                if corruption in ['Contrast', 'Saturation', 'Hue', 'Brightness']: #Brightness
                    factor = factor_2[random.randint(0, len(factor_2)-1)]
                else:
                    factor = factor_1[random.randint(0, len(factor_1)-1)]

                corruptions.extend(define_corruption(corruption, factor=factor))
                factors.append(factor)

            # apply perturbations on images
            transforms = Compose(corruptions)
            image_c = transforms(image)

            name = 'image_' + str(random.randint(0,10000)) + '_'
            for j in range(len(corruptions_names)):
                name = name + corruptions_names[j] + '_' + str(factors[j]) + '_'

            name = name + '.png'
            names.append(name)
            path_image = os.path.join(path_save_images, name)
            image_c.save(path_image)

            if os.path.exists(path_masks) is True:
                mask = Image.open(path_masks[k])
                mask = mask.resize((1024, 1024), resample=Image.NEAREST)
                path_mask = os.path.join(path_save_masks, name)
                mask.save(path_mask)

        images_clean_total.extend(images_clean)
        images_corruption_total.extend(names)

        print('iteration ' + str(i+1) + ' is done')
        print(str(nb_it-(i+1)) + ' iterations to go')
        print('-----------------------------------')

    df["original file"] = images_clean_total
    df["corrupted file"] = images_corruption_total
    df.to_excel(os.path.join(cwd, 'conversion_file.xlsx'))
    print('Testset-C is created!')
    print('In case of classification the conversion file can be used to link the correct label to the corrupted images')
    print('In case of segmentation the ground truth masks got the same name as the corrupted images')


if __name__ == "__main__":

    path_images = sys.argv[1]

    # Parse keyword arguments
    kwargs = {}
    for arg in sys.argv[2:]:
        key, value = arg.split('=')
        kwargs[key] = value

    path_masks = kwargs.get('path_masks')
    max_levels = int(kwargs.get('max_levels'))
    min_level = int(kwargs.get('min_level'))
    inc_compression = bool(kwargs.get('include_compression'))
    iterations = int(kwargs.get('nb_iterations'))

    print(path_masks)
    print(max_levels, min_level)
    print(inc_compression)
    print(iterations)

    create_testset_c(path_images, path_masks=path_masks, max_levels=int(max_levels), min_level=int(min_level), nb_iterations=int(iterations), include_compression=bool(inc_compression))

