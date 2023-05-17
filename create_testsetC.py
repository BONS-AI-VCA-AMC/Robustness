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
    combined_path_images = combine_paths(path_images, images)
    idx_remove = []

    for i in range(len(combined_path_images)):
        image = Image.open(combined_path_images[i])
        shape = image.size
    #    if shape[0] < 1024 or shape[1] < 1024:
    #        idx_remove.append(i)

    print('total number of images removed because of low resolution = ' + str(len(idx_remove)))
    path_images_clean = [i for j, i in enumerate(combined_path_images) if j not in idx_remove]
    images_clean = [i for j, i in enumerate(images) if j not in idx_remove]
    print('total number of images used for TestSet-C = ' + str(len(path_images_clean)))

    images_clean_total = []
    images_corruption_total = []

    """perturbations"""
    corruption_options = ['Motion-blur', 'Overexposure', 'defocus-blur', 'Hue','Saturation', 'Contrast', 'Sharpness', 'Brightness','Resolution', 'JPG', 'JPEG2000']

    #if include_compression == True:
    #    print('test compression')
    #    corruptions_compression = ['Resolution', 'JPG', 'JPEG2000']
    #    corruption_options.extend(corruptions_compression)

    factor_1 = list(range(1+min_level, max_levels+1))
    factor_2 = list(range(11-max_levels, 11-min_level))+list(range(11+min_level,11+max_levels))

    # save dir
    path_save_images = os.path.join(cwd, 'Testset-C/Images')
    os.makedirs(path_save_images, exist_ok=True)



    if os.path.exists(path_masks) is True:
        path_save_masks = os.path.join(cwd, 'Testset-C/Masks')
        os.makedirs(path_save_masks, exist_ok=True)

        masks = os.listdir(path_masks)
        combined_path_masks = combine_paths(path_masks, masks)
        path_masks_clean = [i for j, i in enumerate(combined_path_masks) if j not in idx_remove]

        if len(path_masks_clean) != len(path_images_clean):
            AttributeError('not the same amount of images and masks')

    # apply corruptions
    nb_it = nb_iterations  # number of iteration over testset
    nb_per = 5  # maximum number of corruptions per images

    for i in list(range(nb_it)):
        names = []
        for k in range(len(path_images_clean)):
            '''resize images to 1024x1024'''

            image = Image.open(path_images_clean[k]).convert('RGB')
            image = image.resize((1024, 1024), resample=Image.LANCZOS)

            nb_corruptions = random.randint(1,nb_per)  # random number of corruptions for image
            idx_corruptions = random.sample(range(0, len(corruption_options)), nb_corruptions)  # random chosen corruption

            corruptions = list()
            corruptions_names = list()
            factors = list()

            # create list with all perturbations
            for nb in range(nb_corruptions):
                # append perturbation to transform
                corruption = corruption_options[idx_corruptions[nb]]
                corruptions_names.append(corruption)

                if corruption in ['Contrast', 'Saturation', 'Hue', 'Brightness']: #Brightness
                    factor = factor_2[random.randint(0,len(factor_2)-1)]
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
                mask = Image.open(path_masks_clean[k])
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
    '''
    # Check if there are at least two inputs
    if len(sys.argv) >= 3:
        # If there are, set input2 to the second input
        path_masks = sys.argv[2]
    else:
        path_masks = None

    if len(sys.argv) >= 3:
        # If there are, set input2 to the second input
        max_levels = sys.argv[3]
    if len(sys.argv) >= 4:
        min_level = sys.argv[4]
    if len(sys.argv) >=5:
        iterations = sys.argv[5]
    if len(sys.argv) >=6:
        inc_compression = sys.argv[6]
    '''
    print(path_masks)
    print(max_levels, min_level)
    print(inc_compression)
    print(iterations)

    create_testset_c(path_images, path_masks=path_masks, max_levels=int(max_levels), min_level=int(min_level), nb_iterations=int(iterations), include_compression=bool(inc_compression))

