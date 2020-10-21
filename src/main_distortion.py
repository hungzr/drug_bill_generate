import distortion_blur
import distortion_color
import distortion_compress
import distortion_noise
import distortion_quality_reduced
import random
from PIL import Image
import cv2

def random_number():
    return random.randint(0,4)


def blur(img, inx):
    BD = distortion_blur.BlurDistortion(img)
    gaussian = BD.blur_gaussian(BD.gaussian[random_number()])
    cv2.imwrite('../data/results/blur_' + inx + '_gaussian.png', gaussian)

    lens = BD.blur_lens(BD.lensblur[random_number()])
    cv2.imwrite('../data/results/blur_' + inx + '_lens.png', lens)

    motion = BD.blur_motion(BD.motionbl[random_number()])


def compress(img, inx):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    CD = distortion_compress.CompressDistortions(img)
    jpeg = CD.JPEGCompress(CD.JPEQuality[random_number()])
    cv2.imwrite('../data/results/compress_' + inx + '_jpeg.png', jpeg)

    jp2k = CD.JP2KCompress(CD.JP2Quality[random_number()])
    cv2.imwrite('../data/results/compress_' + inx + '_jp2k.png', jp2k)


def color(img, inx):
    CD = distortion_color.ColorDistortion(img)
    diff = CD.color_diffuse(CD.colorDiff[random_number()])
    cv2.imwrite('../data/results/color_' + inx + '_diff.png', diff)

    shif = CD.color_shifting(CD.colorShif[random_number()])
    cv2.imwrite('../data/results/color_' + inx + '_shif.png', shif)

    quan = CD.color_quantize(CD.colorQuan[random_number()])
    cv2.imwrite('../data/results/color_' + inx + '_quan.png', quan)

    satu = CD.color_saturate(CD.colorSatu[random_number()])
    cv2.imwrite('../data/results/color_' + inx + '_satu.png', satu)

    img_satu = CD.image_saturate(CD.imageSatu[random_number()])
    cv2.imwrite('../data/results/color_' + inx + '_img_satu.png', img_satu)


def noise(img, inx):
    ND = distortion_noise.NoiseDistortion(img)
    gaussian = ND.gaussian_noise(ND.gaussianVars[random_number()])
    cv2.imwrite('../data/results/noise_' + inx + '_gaussian.png', gaussian)

    local = ND.localvar_noise(ND.localVars[random_number()])
    cv2.imwrite('../data/results/noise_' + inx + '_local.png', local)

    poison = ND.poison_noise(ND.poisonVars[random_number()])
    cv2.imwrite('../data/results/noise_' + inx + '_poison.png', poison)

    salt = ND.salt_noise(ND.saltAmount[random_number()])
    cv2.imwrite('../data/results/noise_' + inx + '_salt.png', salt)

    pepper = ND.pepper_noise(ND.pepperAmount[random_number()])
    cv2.imwrite('../data/results/noise_' + inx + '_pepper.png', pepper)

    salt_pepper = ND.saltAndPepper_noise(ND.saltAndPepperAmount[random_number()])
    cv2.imwrite('../data/results/noise_' + inx + '_salt_pepper.png', salt_pepper)

    speckle = ND.speckle_noise(ND.speckleVars[random_number()])
    cv2.imwrite('../data/results/noise_' + inx + '_speckle.png', speckle)

    denoise = ND.de_noise_image(ND.denoiseWeight[random_number()])
    cv2.imwrite('../data/results/noise_' + inx + '_denoise.png', denoise)


# img = cv2.imread('/home/hungdo/HungDo/ocr_generate/src/text.jpg')
# noise(img, str(1))