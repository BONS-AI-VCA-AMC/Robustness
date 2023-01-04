import numpy as np
from PIL import Image, ImageFilter
import cv2
from torchvision import transforms
from io import BytesIO
from wand.image import Image as WandImage
from wand.api import library as wandlibrary


# Custom corruption classes
class Normalize:
    def __call__(self, img):
        img_out = (img - np.min(img)) / np.ptp(img)
        return img_out


class JPGcompression:
    def __init__(self, save_path, severity):
        self.save_path = save_path
        self.severity = severity

    def normalize(self, img):
        img_out = (img - np.min(img)) / np.ptp(img)

        return img_out
    def __call__(self, img):
        c = [40, 35, 30, 25, 20, 12, 10, 8, 6, 4][self.severity - 1]

        quality = c

        img.save(self.save_path, format='JPEG', quality=quality)
        img_jpg = Image.open(self.save_path)

        img = self.normalize(np.array(img_jpg))

        return img


class JPG2000compression:
    def __init__(self, save_path, quality=100):
        self.save_path = save_path
        self.quality = quality

    def normalize(self, img):
        img_out = (img - np.min(img)) / np.ptp(img)

        return img_out

    def __call__(self, img):
        img = (img * 255).astype(np.uint8)
        img = Image.fromarray(img)
        img.save(self.save_path, format='JP2', quality=self.quality)
        img_jpg = Image.open(self.save_path)

        img = self.normalize(np.array(img_jpg))

        return img


class GaussianNoise:
    def __init__(self, severity):
        self.severity = severity

    def normalize(self, img):
        img_out = (img - np.min(img)) / np.ptp(img)
        return img_out

    def __call__(self, img):
        c = [0.05, 0.1, 0.13, 0.16, 0.2, 0.3, 0.4, 0.6, 0.8, 1][self.severity - 1]

        noise_factor = c

        img = self.normalize(np.array(img))

        img_noisy = img + np.random.randn(img.shape[0], img.shape[1], img.shape[2]) * noise_factor
        img_noisy = np.clip(img_noisy, 0., 1.)

        return img_noisy


class ReduceResolution:
    def __init__(self, severity):
        self.severity = severity

    def normalize(self, img):
        img_out = (img - np.min(img)) / np.ptp(img)

        return img_out

    def __call__(self, img):
        c = [2, 3, 4, 5, 6, 8, 10, 12, 16, 20][self.severity - 1]

        factor = c

        img = np.array(img)

        shape = img.shape

        res = cv2.resize(img, dsize=(shape[0] // factor, shape[1] // factor), interpolation=cv2.INTER_CUBIC)
        res = cv2.resize(res, dsize=(shape[1], shape[0]), interpolation=cv2.INTER_CUBIC)
        res, mask, has_mask = self.normalize(res)

        return res


class ToPIL:
    def __call__(self, img):
        img = (img * 255).astype(np.uint8)
        PIL_img = Image.fromarray(img)

        return PIL_img


# Custom Class for ColorJitter
class ColorJitter:
    def __init__(self, severity, deg):
        self.severity = severity

        if deg == 'brightness':
            c = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 1.2, 1.4, 1.6, 1.8, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0][
                self.severity - 1]
            self.jitter = transforms.ColorJitter(brightness=(c, c))
        if deg == 'contrast':
            c = \
            [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.9, 0.95, 1.1, 1.2, 1.25, 1.3, 1.4, 1.7, 2.0, 2.3, 2.7,
             3.1][self.severity - 1]
            self.jitter = transforms.ColorJitter(contrast=(c, c))
        if deg == 'saturation':
            c = \
            [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.7, 2.0, 2.6, 3.5][
                self.severity - 1]
            self.jitter = transforms.ColorJitter(saturation=(c, c))
        if deg == 'hue':
            c = \
            [-0.1, -0.08, -0.065, -0.04, -0.03, -0.025, -0.02, -0.016, -0.013, -0.01, 0.01, 0.013, 0.016, 0.018, 0.02,
             0.04, 0.05, 0.06, 0.08, 0.1][self.severity - 1]
            self.jitter = transforms.ColorJitter(hue=(c, c))

    def __call__(self, img):
        img = self.jitter(img)

        return img


class Sharpness(object):
    """
    adjust sharpness
    """

    def __init__(self, severity=1):
        self.severity = severity

    def __call__(self, img, mask, has_mask):
        c = [2.0, 4.0, 5.0, 10, 15, 20, 40, 60, 80, 100][self.severity - 1]

        sharpness = transforms.RandomAdjustSharpness(c, p=1)

        img_sharp = sharpness(img)

        return img_sharp


# classes for motion blurring
# Extend wand.image.Image class to include method signature
class MotionImage(WandImage):
    def motion_blur(self, radius=0.0, sigma=0.0, angle=0.0):
        wandlibrary.MagickMotionBlurImage(self.wand, radius, sigma, angle)

class motion_blur(object):
    """
    Apply Motion Blur to the PIL image.
    """

    def __init__(self, severity=1):
        self.severity = severity

    def __call__(self, img, mask, has_mask):
        c = [(10, 3), (24, 8), (40, 16), (70, 16), (100, 16), (100, 24), (120, 24), (120, 30), (150, 30), (200, 40)][
            self.severity - 1]

        output = BytesIO()

        img.save(output, format='PNG')

        img = MotionImage(blob=output.getvalue())

        img.motion_blur(radius=c[0], sigma=c[1], angle=np.random.uniform(-45, 45))

        img = cv2.imdecode(np.fromstring(img.make_blob(), np.uint8),
                           cv2.IMREAD_UNCHANGED)

        return Image.fromarray(np.clip(img[..., [2, 1, 0]], 0, 255).astype(np.uint8)), mask, has_mask  # BGR to RGB

