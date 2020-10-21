from PIL import Image
from io import BytesIO
import numpy as np


class CompressDistortions():
    def __init__(self, image):
        self.image = image
        self.JPEQuality = [43, 36, 24, 7, 4]
        self.JP2Quality = [16, 32, 45, 120, 400]

    def JPEGCompress(self, ratio):
        self.outputJPEG = BytesIO()
        im = self.image
        im.save(self.outputJPEG, "JPEG", quality_layers=ratio)
        self.outputJPEG.seek(0)
        JPEGimage = Image.open(self.outputJPEG)
        JPEGimage = np.asarray(JPEGimage).astype(np.uint8)
        return JPEGimage

    def JP2KCompress(self, ratio):
        self.outputJP2K = BytesIO()
        im2k = self.image
        im2k.save(self.outputJP2K, "JPEG2000", quality_layers=[ratio])
        self.outputJP2K.seek(0)
        JP2Kimage = Image.open(self.outputJP2K)
        JP2Kimage = np.asarray(JP2Kimage).astype(np.uint8)
        return JP2Kimage


# im = Image.open('/home/hungdo/HungDo/ocr_generate/src/text.jpg')
# CD = CompressDistortions(im)
# jpeg = CD.JP2KCompress(CD.JP2Quality[4])
# from matplotlib import pyplot as plt
# fig, ax = plt.subplots(nrows=1, ncols=2)
# ax[0].imshow(im)
# ax[1].imshow(jpeg)
# plt.show()