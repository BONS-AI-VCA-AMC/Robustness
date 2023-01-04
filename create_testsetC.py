import numpy as np
import os
from utils import define_perturbation
import random
from utils import Compose

random.seed(0)

def create_testset_c(path_images, path_masks=None):
    """read all images"""



    """check imagesizes"""

    data_processed = ''

    """perturbations"""
    corruption_options = ['Resolution', 'JPG', 'SpotLight - light', 'Contrast', 'Brightness',
                            'Saturation', 'Hue', 'defocus-blur', 'Motion-blur']
    factor_1 = [1,2,3,4,5]
    factor_2 = [6,7,8,9,10,11,12,13,14,15]

    # save dir
    path_save_images = '/Testset-C/Images'

    os.makedirs(path_save_images, exist_ok=True)

    if path_masks != None:
        path_save_masks = '/Testset-C/Masks'
        os.makedirs(path_save_masks, exist_ok=True)


    # corruptions
    nb_it = 5 #number of iteration over testset
    nb_per = 5 #maximum number of corruptions per images

    for i in list(range(nb_it)):

        '''resize images to 1024x1024'''



        for k in range(len(data_processed)):

            nb_corruptions = random.randint(1,nb_per) #random number of corruptions for image
            idx_corruptions = random.sample(range(0, len(corruption_options)), nb_corruptions) #random chosen corruption

            perturbations = list()
            perturbations_names = list()
            factors = list()

            #create list with all perturbations
            for nb in range(nb_corruptions):
                #append perturbation to transform
                perturbation = corruption_options[idx_corruptions[nb]]
                perturbations_names.append(perturbation)


                if perturbation in ['Contrast', 'Brightness','Saturation', 'Hue']:
                    factor = factor_2[random.randint(0,len(factor_2)-1)]
                else:
                    factor = factor_1[random.randint(0, len(factor_1)-1)]

                perturbations.extend(define_perturbation(perturbation, factor=factor))
                factors.append(factor)

            #apply perturbations on images
            transforms = Compose(perturbations)
            image = data_processed[k]


            image_c = transforms(image)

            name = 'image_' + str(random.randint(0,10000)) + '_'
            for i in range(len(perturbations_names)):
                print(perturbations_names[i], factors[i])
                name = name + perturbations_names[i] + '_' + str(factors[i]) + '_'

            name = name + '.png'
            print(name)

            path_image = os.path.join(path_save_images, name)
            image_c.save(path_image)

            if path_masks != None:
                path_mask = os.path.join(path_save_masks, name)
                mask_gt.save(path_mask)

