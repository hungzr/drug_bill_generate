import numpy as np
import cv2

class NoiseDistortion():
    def __init__(self, image):
        self.image = image
        (self.w, self.h, self.d) = self.image.shape
        if self.image.min() < 0:
            self.low_clip = -1.
        else:
            self.low_clip = 0.
        self.image = self.image.astype(np.float)
        self.gaussianVars = [0.001, 0.002, 0.003, 0.005, 0.01]
        self.localVars = [0.001, 0.005, 0.01, 0.02, 0.03]
        self.poisonVars = [0.001, 0.002, 0.003, 0.005, 0.01]
        self.saltAmount = [0.001, 0.005, 0.01, 0.02, 0.03]
        self.pepperAmount = [0.001, 0.005, 0.01, 0.02, 0.03]
        self.saltAndPepperAmount = [0.001, 0.005, 0.01, 0.02, 0.03]
        self.speckleVars = [0.001, 0.005, 0.01, 0.02, 0.05]
        self.denoiseWeight = [1, 3, 5, 7, 9]

    def gaussian_noise(self, var):
        noise = np.random.normal(0, var ** 0.5,
                                 self.image.shape)
        out = self.image + noise
        out = out.astype(np.uint8)
        return out

    def localvar_noise(self, var):
        out = self.image + np.random.normal(0, var ** 0.5)
        out = out.astype(np.uint8)
        return out

    def poison_noise(self, var):
        # Determine unique values in image & calculate the next power of two
        vals = len(np.unique(self.image))
        vals = 2 ** np.ceil(np.log2(vals))
        vals = vals * var
        # Generating noise for each unique value in image.
        out = np.random.poisson(self.image * vals) / float(vals)
        out = out.astype(np.uint8)
        return out

    def salt_noise(self, amount):
        out = self.saltAndPepper_noise(amount=amount, s_p=1)
        return out

    def pepper_noise(self, amount):
        out = self.saltAndPepper_noise(amount=amount, s_p=0.)
        return out

    def salt_pepper_half(self, amount):
        out = self.saltAndPepper_noise(amount=amount, s_p=0.5)
        return out

    def saltAndPepper_noise(self,amount, s_p=.5):
        out = self.image.copy()
        p = amount
        q = s_p
        flipped = np.random.choice([True, False], size=self.image.shape,
                                   p=[p, 1 - p])
        salted = np.random.choice([True, False], size=self.image.shape,
                                  p=[q, 1 - q])
        peppered = ~salted
        out[flipped & salted] = 1
        out[flipped & peppered] = self.low_clip
        out = out.astype(np.uint8)
        return out

    def speckle_noise(self, var):
        inImage = self.image.copy()
        noise = np.random.normal(0, var ** 0.5,
                                 inImage.shape)
        out = inImage + inImage * noise
        out = out.astype(np.uint8)
        return out

    def de_noise_image(self, weight):
        inImage = self.image.copy()
        inImage = inImage.astype(np.uint8)
        out = cv2.fastNlMeansDenoisingColored(inImage, None, weight, 10, 7, 15)
        return out