import os
from utils import define_corruption
import random
from utils import Compose, combine_paths
from PIL import Image

random.seed(0)
def create_testset_c(path_images, path_masks=None):
    """read images and check imagesize"""

    cwd = os.getcwd()
    images = os.listdir(path_images)

    print('total number of images in folder = ' + str(len(images)))
    combined_path_images = combine_paths(path_images, images)
    idx_remove = []

    for i in range(len(combined_path_images)):
        image = Image.open(combined_path_images[i])
        shape = image.size
        if shape[0] < 1024 or shape[1] < 1024:
            idx_remove.append(i)

    print('total number of images removed because of low resolution = ' + str(len(idx_remove)))
    path_images_clean = [i for j, i in enumerate(combined_path_images) if j not in idx_remove]
    print('total number of images used for TestSet-C = ' + str(len(path_images_clean)))

    """perturbations"""
    corruption_options = ['Resolution', 'JPG', 'SpotLight - light', 'Contrast', 'Brightness',
                            'Saturation', 'Hue', 'defocus-blur', 'Motion-blur']

    factor_1 = [1,2,3,4,5]
    factor_2 = [6,7,8,9,10,11,12,13,14,15]

    # save dir
    path_save_images = os.path.join(cwd,'Testset-C/Images')
    os.makedirs(path_save_images, exist_ok=True)

    if path_masks != None:
        path_save_masks = os.path.join(cwd,'Testset-C/Masks')
        os.makedirs(path_save_masks, exist_ok=True)

        masks = os.listdir((path_masks))
        combined_path_masks = combine_paths(path_masks, masks)
        path_masks_clean = [i for j, i in enumerate(combined_path_masks) if j not in idx_remove]

        if len(path_masks_clean) != len(path_images_clean):
            AttributeError('not the same amount of images and masks')




    # corruptions
    nb_it = 5 #number of iteration over testset
    nb_per = 5 #maximum number of corruptions per images

    for i in list(range(nb_it)):
        for k in range(len(path_images_clean)):
            '''resize images to 1024x1024'''

            image = Image.open(path_images_clean[k])
            image.resize((1024,1024),resample=Image.LANCZOS)

            nb_corruptions = random.randint(1,nb_per) #random number of corruptions for image
            idx_corruptions = random.sample(range(0, len(corruption_options)), nb_corruptions) #random chosen corruption

            corruptions = list()
            corruptions_names = list()
            factors = list()

            #create list with all perturbations
            for nb in range(nb_corruptions):
                #append perturbation to transform
                corruption = corruption_options[idx_corruptions[nb]]
                corruptions_names.append(corruption)


                if corruption in ['Contrast', 'Brightness','Saturation', 'Hue']:
                    factor = factor_2[random.randint(0,len(factor_2)-1)]
                else:
                    factor = factor_1[random.randint(0, len(factor_1)-1)]

                corruptions.extend(define_corruption(corruption, factor=factor))
                factors.append(factor)

            #apply perturbations on images
            transforms = Compose(corruptions)
            image_c = transforms(image)

            name = 'image_' + str(random.randint(0,10000)) + '_'
            for i in range(len(corruptions_names)):
                name = name + corruptions_names[i] + '_' + str(factors[i]) + '_'

            name = name + '.png'
            path_image = os.path.join(path_save_images, name)
            image_c.save(path_image)

            if path_masks != None:
                mask = Image.open(path_masks_clean[k])
                mask.resize((1024, 1024), resample=Image.NEAREST)
                path_mask = os.path.join(path_save_masks, name)
                mask.save(path_mask)
        print('iteration ' + str(i) + ' is done')
        print(str(nb_it-i) + ' iterations to go')
        print('-----------------------------------')

    print('Testset-C is created!')

if __name__ == "__main__":
    path_images = r'C:\Users\20172619\OneDrive - TU Eindhoven\PhD\jaar 1\first_experiments\Testset-C\val-set-images'
    path_masks = r'C:\Users\20172619\OneDrive - TU Eindhoven\PhD\jaar 1\first_experiments\Testset-C\val-set-masks'

    create_testset_c(path_images, path_masks=path_masks)

