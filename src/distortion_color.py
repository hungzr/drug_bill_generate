import cv2
import numpy as np
from scipy.ndimage import gaussian_filter as gf
from sklearn.cluster import MiniBatchKMeans


class ColorDistortion():
    def __init__(self, image):
        self.image = image
        self.w, self.h, self.d = self.image.shape
        self.colorDiff = [1, 3, 6, 8, 12]
        self.colorShif = [1, 3, 6, 8, 12]
        self.colorQuan = [64, 48, 32, 16, 8]
        self.colorSatu = [0.4, 0.2, 0.1, 0, -0.4]
        self.imageSatu = [.5, .7, .9, 1.1, 1.3]
        self.labin = cv2.cvtColor(self.image, cv2.COLOR_RGB2LAB)
        self.hsvin = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
        (self.h, self.w) = self.image.shape[:2]

    def color_diffuse(self, amount):
        sigma = 1.5 * amount + 2
        scale = amount
        labout = np.copy(self.labin)
        labout[:, :, 1] = gf(self.labin[:, :, 1], sigma)
        labout[:, :, 2] = gf(self.labin[:, :, 2], sigma)
        diffuse = cv2.cvtColor(labout, cv2.COLOR_LAB2RGB)
        return diffuse

    def color_quantize(self, n):
        # reshape the image into a feature vector so that k-means
        # can be applied
        imageIn = self.labin.reshape((self.h * self.w, 3))
        # apply k-means using the specified number of clusters and
        # then create the quantized image based on the predictions
        clt = MiniBatchKMeans(n_clusters=n)
        labels = clt.fit_predict(imageIn)
        quant = clt.cluster_centers_.astype("uint8")[labels]

        # reshape the feature vectors to images
        quant = quant.reshape((self.h, self.w, 3))
        imageIn =imageIn.reshape((self.h, self.w, 3))

        # convert from L*a*b* to RGB
        quant = cv2.cvtColor(quant, cv2.COLOR_LAB2RGB)
        image = cv2.cvtColor(imageIn, cv2.COLOR_LAB2BGR)
        reslt = np.hstack([image, quant])
        return quant

    def color_shifting(self, value):
        hsvIm = np.copy(self.labin)
        for i in range(1, 3):
            hsvIm[:, :, i] = hsvIm[:, :, i] + value
            hsvIm[:, :, i] = np.clip(hsvIm[:, :, i], 0, 255)
        hsvIm = hsvIm.astype(np.uint8)
        rgbOut = cv2.cvtColor(hsvIm, cv2.COLOR_LAB2RGB)
        return rgbOut

    def color_saturate(self, factor):
        hsvIm = np.copy(self.hsvin)
        hsvIm[:,:,1] = hsvIm[:,:,1] * factor
        hsvIm[:, :, 1] = np.clip(hsvIm[:,:,1], 0, 255)
        rgbOut = cv2.cvtColor(hsvIm, cv2.COLOR_HSV2RGB)
        rgbOut = rgbOut.astype(np.uint8)
        return rgbOut

    def image_saturate(self, factor):
        labIm = np.copy(self.labin)
        labIm[:,:,1:] = labIm[:,:,1:] * factor
        rgbOut = cv2.cvtColor(labIm, cv2.COLOR_LAB2RGB)
        return rgbOut

# from PIL import Image
# import cv2
# im = cv2.imread('/home/hungdo/HungDo/ocr_generate/src/text.jpg')
# CD = ColorDistortion(im)
# jpeg = CD.color_diffuse(CD.colorDiff[4])
# from matplotlib import pyplot as plt
# fig, ax = plt.subplots(nrows=1, ncols=2)
# ax[0].imshow(im)
# ax[1].imshow(jpeg)
# plt.show()