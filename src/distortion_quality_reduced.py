import numpy as np
import cv2
from scipy import ndimage as ndi
from skimage import exposure


class QualityReduced():
    def __init__(self, image):
        self.image = image
        (self.w, self.h, self.d) = self.image.shape
        self.darkenRatio = [0.05, 0.1, 0.2, 0.4, 0.8]
        self.brightRatio = [1.5, 3.5, 5.5, 7.5, 9.5]
        self.shiftingRat = [0.15, 0.08, 0, -0.08, -0.15]

    def enhance_adjust_gamma(self, gamma):
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
        image = self.image.copy()
        image = image.astype(np.uint8)
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")
        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)

    def enhance_shifting(self, amount):
        floatImage = self.image.astype(np.float)
        # normalImage = floatImage / np.max(floatImage)
        out = np.zeros((self.w, self.h, self.d), np.float)
        for i in range(3):
            comp = amount + floatImage[:,:,i] / np.max(floatImage[:,:,i])
            trunc = np.copy(comp)
            trunc[np.where(comp >= 1)] = 1
            trunc[np.where(comp <= 0)] = 0
            out[:,:,i] = trunc
        return (out * 255).astype(np.uint8)

    def sharpening_high_pass(self, alpha):
        image = self.image.astype(np.uint8)
        # High pass filtering for image sharpening
        kernel = alpha * np.array([[-1, -1, -1],
                           [-1, 8, -1],
                           [-1, -1, -1]])
        highpass_3x3 = np.zeros_like(image)
        for i in range(3):
            highpass_3x3[:,:,i] = ndi.convolve(image[:,:,i], kernel)
        return image - highpass_3x3

    def jitter_image(self, val):
        image = self.image.astype(np.uint8)
        noise = np.random.randint(0, val, (self.w, self.h))  # design jitter/noise here
        zitter = np.zeros_like(image)
        zitter[:, :, 1] = noise

        noise_added = cv2.add(image, zitter)
        combined = np.vstack((image[:int(self.h / 2), :, :], noise_added[int(self.h / 2):, :, :]))
        return combined

    def equalization(self, lim):
        image = self.image.copy()
        img_adapteq = exposure.equalize_adapthist(image, clip_limit=lim)
        return (255 * img_adapteq).astype(np.uint8)

    def resize_restore(self, strength):
        image = self.image.astype(np.uint8)
        ratio = 0.9 - strength ** .6
        newH = int(self.h * ratio)
        newW = int(self.w * ratio)
        resized = cv2.resize(image, (newH, newW))
        restored = cv2.resize(resized, (self.h, self.w))
        return restored