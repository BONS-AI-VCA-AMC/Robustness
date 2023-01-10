import os
from utils import define_corruption
import random
from utils import Compose, combine_paths
from PIL import Image
import pandas as pd
import sys

random.seed(0)


def create_testset_c(path_images, path_masks=None, levels=5):
    """read images and check imagesize"""
    cwd = os.getcwd()
    images = os.listdir(path_images)

    """
    we create an excel file to link all corrupted images to the orginal ones to link them later with the correct label
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

    df["original file"] = images_clean

    """perturbations"""
    corruption_options = ['Resolution', 'JPG', 'SpotLight - light', 'Contrast', 'Brightness'
                           ,'Saturation', 'Hue', 'defocus-blur', 'Motion-blur']

    factor_1 = list(range(1,levels+1))
    factor_2 = list(range(11-levels, 11))+list(range(11,11+levels))

    # save dir
    path_save_images = os.path.join(cwd, 'Testset-C/Images')
    os.makedirs(path_save_images, exist_ok=True)

    if path_masks is not None:
        path_save_masks = os.path.join(cwd, 'Testset-C/Masks')
        os.makedirs(path_save_masks, exist_ok=True)

        masks = os.listdir(path_masks)
        combined_path_masks = combine_paths(path_masks, masks)
        path_masks_clean = [i for j, i in enumerate(combined_path_masks) if j not in idx_remove]

        if len(path_masks_clean) != len(path_images_clean):
            AttributeError('not the same amount of images and masks')

    # apply corruptions
    nb_it = 5  # number of iteration over testset
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

                if corruption in ['Contrast', 'Brightness','Saturation', 'Hue']:
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

            if path_masks is not None:
                mask = Image.open(path_masks_clean[k])
                mask = mask.resize((1024, 1024), resample=Image.NEAREST)
                path_mask = os.path.join(path_save_masks, name)
                mask.save(path_mask)

        df["iteration " + str(i)] = names

        print('iteration ' + str(i+1) + ' is done')
        print(str(nb_it-(i+1)) + ' iterations to go')
        print('-----------------------------------')

    df.to_excel(os.path.join(cwd, 'conversion_file.xlsx'))
    print('Testset-C is created!')
    print('In case of classification the conversion file can be used to link the correct label to the corrupted images')
    print('In case of segmentation the ground truth masks got the same name as the corrupted images')


if __name__ == "__main__":

    path_images = sys.argv[1]
    # Check if there are at least two inputs
    if len(sys.argv) >= 3:
        # If there are, set input2 to the second input
        path_masks = sys.argv[2]
    else:
        path_masks = None

    create_testset_c(path_images, path_masks=path_masks, levels=5)

