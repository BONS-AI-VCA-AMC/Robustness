from torchvision import transforms
import os
import local_corruptions as loc_cor
import global_corruptions as glob_cor

class Compose:
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, img):
        for t in self.transforms:
            img = t(img)
        return img

# Custom Resize class
class Resize:
    def __init__(self, target_size):
        self.target_size = target_size

    def __call__(self, img):
        img = transforms.functional.resize(img, size=self.target_size,
                                           interpolation=transforms.InterpolationMode.LANCZOS)
        mask = transforms.functional.resize(mask, size=self.target_size,
                                            interpolation=transforms.InterpolationMode.NEAREST)

        return img

def combine_paths(dir, files):
    paths = []
    for i in range(len(files)):
        paths.append(os.path.join(dir, files[i]))

    return paths


# define curruptions
def define_corruption(corruption, factor):
    corruptions = []

    if corruption == 'Resolution':
        corruptions.append(glob_cor.ReduceResolution(factor))
        corruptions.append(glob_cor.ToPIL())
    if corruption == 'Gaussian-Noise':
        corruptions.append(glob_cor.GaussianNoise(factor))
        corruptions.append(glob_cor.ToPIL())
    if corruption == 'JPG':
        cwd = os.getcwd()
        corruptions.append(glob_cor.JPGcompression(os.path.join(cwd, 'JPG_image/temporary_image.jpg'), factor))
        corruptions.append(glob_cor.ToPIL())
    if corruption == 'SpotLight - light':
        position = [(200, 200)]
        corruptions.append(loc_cor.LocalCorruptions(factor, mode='light', gauss_position = position))
        corruptions.append(glob_cor.ToPIL())
    if corruption == 'defocus-blur':
        corruptions.append(loc_cor.LocalCorruptions(factor, mode='blur'))
        corruptions.append(glob_cor.ToPIL())
    if corruption == 'Contrast':
        corruptions.append(glob_cor.ColorJitter(factor, deg='contrast'))
    if corruption == 'Brightness':
        corruptions.append(glob_cor.ColorJitter(factor, deg='brightness'))
    if corruption == 'Saturation':
        corruptions.append(glob_cor.ColorJitter(factor, deg='saturation'))
    if corruption == 'Hue':
        corruptions.append(glob_cor.ColorJitter(factor, deg='hue'))
    if corruption == 'Motion-blur':
        corruptions.append(glob_cor.motion_blur(factor))
    if corruption == 'Sharpness':
        corruptions.append(glob_cor.Sharpness(factor))

    return corruptions