import distortion_blur
import distortion_color
import distortion_compress
import distortion_noise
import distortion_quality_reduced
import random
from PIL import Image
import cv2
import os

root_save_path = '../data/results'

def random_number():
    return random.randint(0,4)


def blur(img, inx, form):
    BD = distortion_blur.BlurDistortion(img)
    
    gaussian = BD.blur_gaussian(BD.gaussian[random_number()])
    img_name = form + '_' + inx + '_blur_gaussian.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), gaussian)

    lens = BD.blur_lens(BD.lensblur[random_number()])
    img_name = form + '_' + inx + '_blur_lens.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), lens)

    motion = BD.blur_motion(BD.motionbl[random_number()])
    img_name = form + '_' + inx + '_blur_motion.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), motion)


def compress(img, inx, form):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    CD = distortion_compress.CompressDistortions(img)
    
    jpeg = CD.JPEGCompress(CD.JPEQuality[random_number()])
    img_name = form + '_' + inx + '_compress_jpeg.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), jpeg)

    jp2k = CD.JP2KCompress(CD.JP2Quality[random_number()])
    img_name = form + '_' + inx + '_compress_jp2k.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), jp2k)


def color(img, inx, form):
    CD = distortion_color.ColorDistortion(img)
    
    diff = CD.color_diffuse(CD.colorDiff[random_number()])
    img_name = form + '_' + inx + '_color_diff.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), diff)

    shif = CD.color_shifting(CD.colorShif[random_number()])
    img_name = form + '_' + inx + '_color_shif.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), shif)

    quan = CD.color_quantize(CD.colorQuan[random_number()])
    img_name = form + '_' + inx + '_color_quan.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), quan)

    satu = CD.color_saturate(CD.colorSatu[random_number()])
    img_name = form + '_' + inx + '_color_satu.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), satu)

    img_satu = CD.image_saturate(CD.imageSatu[random_number()])
    img_name = form + '_' + inx + '_color_img_satu.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), img_satu)


def noise(img, inx, form):
    ND = distortion_noise.NoiseDistortion(img)
    
    gaussian = ND.gaussian_noise(ND.gaussianVars[random_number()])
    img_name = form + '_' + inx + '_noise_gaussian.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), gaussian)

    local = ND.localvar_noise(ND.localVars[random_number()])
    img_name = form + '_' + inx + '_noise_local.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), local)

    poison = ND.poison_noise(ND.poisonVars[random_number()])
    img_name = form + '_' + inx + '_noise_poison.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), poison)

    salt = ND.salt_noise(ND.saltAmount[random_number()])
    img_name = form + '_' + inx + '_noise_salt.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), salt)

    pepper = ND.pepper_noise(ND.pepperAmount[random_number()])
    img_name = form + '_' + inx + '_noise_pepper.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), pepper)

    salt_pepper = ND.saltAndPepper_noise(ND.saltAndPepperAmount[random_number()])
    img_name = form + '_' + inx + '_noise_salt_pepper.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), salt_pepper)

    speckle = ND.speckle_noise(ND.speckleVars[random_number()])
    img_name = form + '_' + inx + '_noise_speckle.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), speckle)

    denoise = ND.de_noise_image(ND.denoiseWeight[random_number()])
    img_name = form + '_' + inx + '_noise_denoise.png'
    cv2.imwrite(os.path.join(root_save_path, img_name), denoise)


# img = cv2.imread('/home/hungdo/HungDo/ocr_generate/src/text.jpg')
# noise(img, str(1))