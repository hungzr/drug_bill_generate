import cv2
import matplotlib.pyplot as plt
import numpy as np
from distortions import distortion_blur, \
    distortion_color,\
    distortion_compress, \
    distortion_noise, \
    distortion_quality_reduced
from matplotlib import image as mli
import os
from PIL import Image
from quality_feature_extraction import quality_feature_vector
from IQA_AutoLabel import CPCQI
from brisque import BRISQUE

class DistortGenerate():
    def __init__(self):
        self.imagePath = r'D:\DAT-Image Quality Assessment\kadis700k\kadis700k\ref_imgs'
        self.sampleNumber = [100, 1000]
        self.allParams = [[2, 4, 6, 8, 10], [9, 13, 17, 21, 25], [10, 15, 20, 25, 30], [1, 3, 6, 8, 12],
                          [1, 3, 6, 8, 12], [64, 48, 32, 16, 8], [0.4, 0.2, 0.1, 0, -0.2],
                          [.5, .7, .9, 1.1, 1.3], [43, 36, 24, 7, 4], [16, 32, 45, 120, 400],
                          [.5, .7, .9, 1.5, 3], [0.5, .7, .9, 1.5, 3], [0.001, 0.002, 0.003, 0.005, 0.009],
                          [0.001, 0.003, 0.005, 0.007, 0.01], [0.001, 0.003, 0.005, 0.007, 0.01], [0.001, 0.003, 0.005, 0.007, 0.01],
                          [0.001, 0.003, 0.005, 0.007, 0.01], [1, 3, 5, 7, 9], [0.3, 0.4, 0.5, 0.65, 0.8],
                          [1.5, 2., 2.5, 3.5, 5.5], [0.15, 0.08, 0, -0.08, -0.15], [0.05, 0.1, 0.2, 0.3, 0.4],
                          [10, 20, 40, 70, 100], [0.01, 0.02, 0.03, 0.04, 0.05], [0.1, 0.2, 0.3, 0.45, 0.6]]
        self.subTitle = ['Original', 'Distortion lv 1',
                         'Distortion lv 2', 'Distortion lv 3',
                         'Distortion lv 4', 'Distortion lv 5']
        self.supTitle = ['Gaussian-Blur', 'Lens-Blur', 'Motion-Blur', 'Color-Diffuse', 'Color-Shifting',
                         'Color-Quantize', 'Color-Saturation', 'Image-Saturation', 'JPEG-Compress',
                         'JP2K-Compress', 'Gaussian-Noise', 'Local-Variations', 'Poison-Noise',
                         'Salt-Noise', 'Pepper-Noise', 'Salt-Pepper-Noise', 'Speckle-Noise',
                         'De-noise', 'Darken', 'Brighten', 'Shifting', 'Sharpen-hi-pass', 'Jitter-Added',
                         'Equalization-Hist', 'Resize-Restore-Linear']

        self.inputParams = {}
        for x in range(25):
            self.inputParams[self.supTitle[x]] = self.allParams[x]

    def image_generate(self):
        import time
        resultDict = {}
        self.images = os.listdir(self.imagePath)
        npyData = []
        npyBRQ = []
        progress = 0
        for imIdx in range(self.sampleNumber[0], self.sampleNumber[1]):
            tic = time.clock()
            resultDict['Case %d' % imIdx] = {}
            resultDict['Case %d' % imIdx]['Origin'] = {}
            resultDict['Case %d' % imIdx]['Origin']['image'] = self.images[imIdx]
            resultDict['Case %d' % imIdx]['Origin']['CPCQI'] = 0

            self.image = 255 * mli.imread(os.path.join(self.imagePath, self.images[imIdx]))
            self.image = self.image.astype(np.uint8)
            f = quality_feature_vector(self.image)
            resultDict['Case %d' % imIdx]['Origin']['feature'] = f
            npyData.append([self.images[imIdx], 0, f])
            npyBRQ.append([self.images[imIdx], 0, f])

            self.imagePIL = Image.open(os.path.join(self.imagePath, self.images[imIdx]))

            self.DBL = distortion_blur.BlurDistortion(self.image)
            self.DCL = distortion_color.ColorDistortion(self.image)

            self.DCP = distortion_compress.CompressDistortions(self.imagePIL)
            self.DNS = distortion_noise.NoiseDistortion(self.image)
            self.DQR = distortion_quality_reduced.QualityReduced(self.image)
            self.allFuntions = [self.DBL.blur_gaussian, self.DBL.blur_lens, self.DBL.blur_motion]
                                # self.DCL.color_diffuse, self.DCL.color_shifting, self.DCL.color_quantize,
                                # self.DCL.color_saturate, self.DCL.image_saturate, self.DCP.JPEGCompress,
                                # self.DCP.JP2KCompress, self.DNS.gaussian_noise, self.DNS.localvar_noise,
                                # self.DNS.poison_noise, self.DNS.salt_noise, self.DNS.pepper_noise,
                                # self.DNS.saltAndPepper_noise, self.DNS.speckle_noise, self.DNS.de_noise_image,
                                # self.DQR.enhance_adjust_gamma, self.DQR.enhance_adjust_gamma, self.DQR.enhance_shifting,
                                # self.DQR.sharpening_high_pass, self.DQR.jitter_image,
                                # self.DQR.equalization, self.DQR.resize_restore]

            for idx in range(len(self.allFuntions)):
                distortionType = self.supTitle[idx]
                resultDict['Case %d' % imIdx][distortionType] = {}
                for i in range(5):
                    dl = self.allFuntions[idx](self.inputParams[distortionType][i])
                    resultDict['Case %d' % imIdx][distortionType]['lv%d' % (i + 1)] = {}
                    cpcqi = CPCQI(self.image, dl)
                    ft = quality_feature_vector(dl)
                    testFeature = brq.get_feature(self.image)
                    testFeature = brq._scale_feature(testFeature)
                    brqf = np.array(testFeature).reshape(1, -1)
                    resultDict['Case %d' % imIdx][distortionType]['lv%d' % (i + 1)]['CPCQI'] = cpcqi
                    resultDict['Case %d' % imIdx][distortionType]['lv%d' % (i + 1)]['feature'] = ft
                    npyData.append([distortionType + 'lv%d' % (i + 1), cpcqi, ft])
                    npyBRQ.append([distortionType + 'lv%d' % (i + 1), cpcqi, brqf])
            # figSaveIndex = 0
            # for idx in range(25):
            #     result = []
            #     result.append(self.image)
            #     for i in range(5):
            #         dl = self.allFuntions[idx](self.inputParams[self.supTitle[idx]][i])
            #         result.append(dl)
            #     if figSaveIndex < 25:
            #         fig, ax = plt.subplots(nrows=2, ncols=3, dpi=200)
            #         plt.suptitle(self.supTitle[idx], fontsize="x-large")
            #         for j in range(6):
            #             if j <= 2:
            #                 ax[0][j].imshow(result[j])
            #                 ax[0][j].axis('off')
            #                 ax[0][j].set_title(self.subTitle[j])
            #             else:
            #                 ax[1][j - 3].imshow(result[j])
            #                 ax[1][j - 3].axis('off')
            #                 ax[1][j - 3].set_title(self.subTitle[j])
            #
            #         mng = plt.get_current_fig_manager()
            #         mng.full_screen_toggle()
            #         if os.path.exists('examples/%s' % self.images[imIdx]) == False:
            #             os.makedirs('examples/%s' % self.images[imIdx])
            #         plt.savefig(os.path.join('examples/%s' % self.images[imIdx], self.supTitle[idx] + '.png'))
            #         figSaveIndex += 1
            #         plt.close()
            toc = time.clock()
            progress += 1
            print('Progress % d / %d with time: % .4f' % (progress, self.sampleNumber[1] - self.sampleNumber[0], toc - tic))
        import dicttoxml
        xl = dicttoxml.dicttoxml(resultDict, attr_type=False)
        f = open("xml/kadis_distortions_fixed_%d_%d.xml" % (self.sampleNumber[0], self.sampleNumber[1]), "wb")
        f.write(xl)
        np.save("npy/kadis_distortions_fixed_%d_%d.npy" % (self.sampleNumber[0], self.sampleNumber[1]), npyData)
        np.save("brisque/kadis_distortions_brisque_%d_%d.npy" % (self.sampleNumber[0], self.sampleNumber[1]), npyBRQ)

brq = BRISQUE()
DG = DistortGenerate()
DG.image_generate()