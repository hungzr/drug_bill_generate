import numpy as np
import cv2
from PIL import Image
from scipy.signal import convolve2d
from skimage.draw import circle

def fspecial_gauss(size, sigma=0.5):
    """Function to mimic the 'fspecial' gaussian MATLAB function
    """
    x, y = np.mgrid[-size//2 + 1:size//2 + 1, -size//2 + 1:size//2 + 1]
    g = np.exp(-((x**2 + y**2)/(2.0*sigma**2)))
    return g/g.sum()

class BlurDefocus():
    def __init__(self, image, radius):
        self.image = image
        self.radius = radius

    def DefocusBlur(self):
        imgarray = np.array(self.image)
        kernel = self.DiskKernel()
        imgOut = imgarray.copy()
        for i in range(3):
            convolved = convolve2d(imgarray[:,:,i], kernel, mode='same').astype("uint8")
            imgOut[:,:,i] = convolved
        return imgOut

    def DiskKernel(self):
        kernelwidth = self.radius
        kernel = np.zeros((kernelwidth, kernelwidth), dtype=np.float32)
        circleCenterCoord = round(self.radius / 2) - 1
        circleRadius = round(circleCenterCoord + 1) - 1

        rr, cc = circle(circleCenterCoord, circleCenterCoord, circleRadius)
        kernel[rr, cc] = 1
        if (self.radius == 3 or self.radius == 5):
            kernel = self.Adjust(kernel, self.radius)

        normalizationFactor = np.count_nonzero(kernel)
        kernel = kernel / normalizationFactor
        return kernel

    def Adjust(self, kernel, kernelwidth):
        kernel[0, 0] = 0
        kernel[0, kernelwidth - 1] = 0
        kernel[kernelwidth - 1, 0] = 0
        kernel[kernelwidth - 1, kernelwidth - 1] = 0
        return kernel

class BlurDistortion():
    def __init__(self, image):
        self.image = image
        self.w, self.h, self.d = self.image.shape
        self.gaussian = [0.1, 0.5, 1, 2, 5]
        self.lensblur = [1, 3, 5, 7, 9]
        self.motionbl = [1, 2, 4, 6, 10]

    def blur_gaussian(self, sigma):
        self.blurGimage = cv2.GaussianBlur(self.image,(15,15),sigma)
        return self.blurGimage

    def blur_lens(self, radius):
        self.BDF = BlurDefocus(self.image, radius)
        self.blurLimage = self.BDF.DefocusBlur()
        return self.blurLimage

    def blur_motion(self, size):
        # generating the kernel
        kernel_motion_blur = np.zeros((size, size))
        kernel_motion_blur[int((size - 1) / 2), :] = np.ones(size)
        kernel_motion_blur = kernel_motion_blur / size
        # applying the kernel to the input image
        self.blurMimage = cv2.filter2D(self.image, -1, kernel_motion_blur)
        return self.blurMimage