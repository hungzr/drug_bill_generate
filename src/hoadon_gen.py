from faker import Faker
import cv2
import random
from PIL import ImageFont, ImageDraw, Image
from main_distortion import *
import numpy as np
import time


def load_txt(txt_path):
    f = open(txt_path, 'r')
    contents = [line.replace('\n', '') for line in f.readlines()]
    # print(contents)
    return contents


def gen_age():
    return random.randint(1, 100)


def gen_gender():
    gender = ['Nam', 'Nữ']
    return random.choice(gender)


def gen_phone():
    return '09' + ''.join(str(random.randint(0, 9)) for _ in range(8))


def gen_patient_id():
    return 'BN: ' + ''.join(str(random.randint(0, 9)) for _ in range(9))


def gen_hospital_location():
    hospital_name = load_txt('../data/hospital_name.txt')
    hospital_location = load_txt('../data/hospital_location.txt')
    inx = random.randint(0, len(hospital_name)-1)

    return hospital_name[inx] + '\n' + hospital_location[inx]


def gen_patient_name():
    fake = Faker()
    my_list = ['Nguyễn', 'Đỗ', 'Lê', 'Hoàng', 'Trần',
                'Văn', 'Thị', 'Đức', 'Đình', 'Minh',
                'Hưng', 'Huy', 'Hoàng']

    return fake.sentence(ext_word_list=my_list, nb_words=4)


def gen_patient_location():
    street = ['Hoàng Quốc Việt', 'Hai Bà Trưng', 'Trần Phú',
               'Phạm Văn Đồng', 'Nguyễn Trãi']
    district = ['Cầu Giấy', 'Đống Đa', 'Ba Đình']
    city = ['Hà Nội', 'Hải Phòng', 'Nam Định']
    location = random.choice(street) + ', ' + random.choice(district) + ', '\
                + random.choice(city)
    return location


def gen_patient_health():
    health = load_txt('../data/patient_health.txt')
    return random.choice(health)


def gen_list_drug():
    drug = load_txt('../data/drugs.txt')

    time_to_use = ['Sáng', 'Tối']
    result = random.choice(drug) + '\nUống ' + random.choice(time_to_use)
    return result


def gen_datatime():
    fake = Faker()
    date_time = str(fake.date_this_year())
    temp = date_time.split('-')
    new_date_time = 'Ngày ' + temp[2] + ' tháng ' + temp[1] + ' năm ' + temp[0]
    return new_date_time


def draw_form_1(hospital_location, patient_id, patient_name, patient_age,
                patient_gender, patient_location, patient_phone,
                patient_health, patient_drug, patient_date, doctor_name):
    font_size = 36
    width = 1080
    height = 1920
    back_ground_color = (255, 255, 255)
    font_size = 38
    font_color = (0, 0, 0)
    amount = ['viên', 'gói']

    img = Image.new("RGB", (width, height), back_ground_color)
    draw = ImageDraw.Draw(img)
    unicode_font = ImageFont.truetype("../font/arial-unicode-ms/ArialUnicodeMS.ttf", font_size)
    unicode_font_big = ImageFont.truetype("../font/arial-unicode-ms/ARIALUNI.TTF", font_size + 4)

    draw.text((100, 90), hospital_location, font=unicode_font_big, fill=font_color)
    draw.text((750, 90), patient_id, font=unicode_font, fill=font_color)
    draw.text((430, 270), u'ĐƠN THUỐC', font=unicode_font_big, fill=font_color)
    draw.text((60, 340), u'Họ tên: ' + patient_name, font=unicode_font, fill=font_color)
    draw.text((60, 390), u'Tuổi: ' + str(patient_age), font=unicode_font, fill=font_color)
    draw.text((320, 390), u'Giới tính: ' + patient_gender, font=unicode_font, fill=font_color)
    draw.text((60, 440), u'Địa chỉ: ' + patient_location, font=unicode_font, fill=font_color)
    draw.text((60, 490), u'SĐT: ' + patient_phone, font=unicode_font, fill=font_color)
    draw.text((60, 540), u'Chẩn đoán: ' + patient_health, font=unicode_font, fill=font_color)
    draw.text((120, 620), u'Tên thuốc - Hoạt chất                              SL', 
                font=unicode_font_big, fill=font_color)
    draw.text((130, 680), patient_drug, font=unicode_font, fill=font_color)
    draw.text((130, 780), gen_list_drug(), font=unicode_font, fill=font_color)
    draw.text((130, 880), gen_list_drug(), font=unicode_font, fill=font_color)
    draw.text((130, 980), gen_list_drug(), font=unicode_font, fill=font_color)
    draw.text((850, 680), str(random.randint(1, 10)) + random.choice(amount), 
                font=unicode_font, fill=font_color)
    draw.text((850, 780), str(random.randint(1, 10)) + random.choice(amount), 
                font=unicode_font, fill=font_color)
    draw.text((850, 880), str(random.randint(1, 10)) + random.choice(amount), 
                font=unicode_font, fill=font_color)
    draw.text((850, 980), str(random.randint(1, 10)) + random.choice(amount), 
                font=unicode_font, fill=font_color)
    draw.text((60, 1200), 'Lời dặn bác sĩ : ', font=unicode_font, fill=font_color)
    draw.text((520, 1400), patient_date, font=unicode_font, fill=font_color)
    draw.text((710, 1440), 'Bác sĩ', font=unicode_font, fill=font_color)
    draw.text((600, 1700), doctor_name, font=unicode_font, fill=font_color)

    # img.save("text.jpg")
    return img


def draw_form_2(hospital_location, patient_name, patient_age,
                patient_gender, patient_location,
                patient_health, patient_drug, patient_date, doctor_name):
    font_size = 36
    width = 1280
    height = 1920
    back_ground_color = (255, 255, 255)
    font_size = 38
    font_color = (0, 0, 0)
    amount = ['viên', 'gói']

    img = Image.new("RGB", (width, height), back_ground_color)
    draw = ImageDraw.Draw(img)
    unicode_font_small = ImageFont.truetype("../font/arial-unicode-ms/ArialUnicodeMS.ttf", font_size-4)
    unicode_font_med = ImageFont.truetype("../font/arial-unicode-ms/ArialUnicodeMS.ttf", font_size)
    unicode_font_big = ImageFont.truetype("../font/arial-unicode-ms/ARIALUNI.TTF", font_size + 22)

    draw.text((80, 40), u'Bộ Y Tế', font=unicode_font_med, fill=font_color)
    draw.text((80, 90), hospital_location, font=unicode_font_med, fill=font_color)
    draw.text((530, 270), u'ĐƠN THUỐC', font=unicode_font_big, fill=font_color)
    draw.text((60, 370), u'I. THÔNG TIN BỆNH NHÂN :', font=unicode_font_med, fill=font_color)
    draw.text((60, 430), u'Họ tên: ' + patient_name, font=unicode_font_med, fill=font_color)
    draw.text((60, 470), u'Tuổi: ' + str(patient_age), font=unicode_font_med, fill=font_color)
    draw.text((420, 470), u'Giới tính: ' + patient_gender, font=unicode_font_med, fill=font_color)
    draw.text((60, 520), u'Địa chỉ: ' + patient_location, font=unicode_font_med, fill=font_color)
    draw.text((60, 570), u'Chẩn đoán: ' + patient_health, font=unicode_font_med, fill=font_color)
    draw.text((60, 640), u'II. THÔNG TIN ĐƠN THUỐC : ', font=unicode_font_med, fill=font_color)

    draw.text((130, 710), '1. ' + patient_drug, font=unicode_font_med, fill=font_color)
    draw.text((130, 810), '2. ' + gen_list_drug(), font=unicode_font_med, fill=font_color)
    draw.text((130, 910), '3. ' + gen_list_drug(), font=unicode_font_med, fill=font_color)
    draw.text((900, 710), str(random.randint(1, 10)) + '     ' + random.choice(amount), 
                font=unicode_font_med, fill=font_color)
    draw.text((900, 810), str(random.randint(1, 10)) + '     ' + random.choice(amount), 
                font=unicode_font_med, fill=font_color)
    draw.text((900, 910), str(random.randint(1, 10)) + '     ' + random.choice(amount), 
                font=unicode_font_med, fill=font_color)
    draw.text((60, 1200), 'Ghi chú : ', font=unicode_font_small, fill=font_color)
    draw.text((620, 1400), patient_date, font=unicode_font_med, fill=font_color)
    draw.text((810, 1440), 'Bác sĩ', font=unicode_font_med, fill=font_color)
    draw.text((710, 1700), doctor_name, font=unicode_font_med, fill=font_color)

    # img.save("text.jpg")
    return img


def draw_form_3(hospital_location, patient_id, patient_name, patient_age,
                patient_gender, patient_location, patient_phone,
                patient_health, patient_drug, patient_date, doctor_name):
    font_size = 36
    width = 1480
    height = 1920
    back_ground_color = (255, 255, 255)
    font_size = 42
    font_color = (0, 0, 0)
    amount = ['viên', 'gói', 'chai']

    img = Image.new("RGB", (width, height), back_ground_color)
    draw = ImageDraw.Draw(img)
    unicode_font_small = ImageFont.truetype("../font/arial-unicode-ms/ArialUnicodeMS.ttf", font_size - 4)
    unicode_font_med = ImageFont.truetype("../font/arial-unicode-ms/ArialUnicodeMS.ttf", font_size)
    unicode_font_big = ImageFont.truetype("../font/arial-unicode-ms/ARIALUNI.TTF", font_size + 22)

    draw.text((80, 40), u'Bộ Y Tế', font=unicode_font_med, fill=font_color)
    draw.text((80, 90), hospital_location, font=unicode_font_med, fill=font_color)
    draw.text((950, 90), patient_id, font=unicode_font_med, fill=font_color)
    draw.text((550, 270), u'ĐƠN THUỐC', font=unicode_font_big, fill=font_color)
    draw.text((60, 370), u'Họ tên:  ' + patient_name, font=unicode_font_med, fill=font_color)
    draw.text((820, 370), u'Tuổi:  ' + str(patient_age), font=unicode_font_med, fill=font_color)
    draw.text((60, 430), u'SĐT: ' + patient_phone, font=unicode_font_med, fill=font_color)
    draw.text((820, 430), u'Giới tính: ' + patient_gender, font=unicode_font_med, fill=font_color)
    draw.text((60, 490), u'Địa chỉ: ' + patient_location, font=unicode_font_med, fill=font_color)
    draw.text((60, 550), u'Chẩn đoán: ' + patient_health, font=unicode_font_med, fill=font_color)
    draw.text((60, 610), u'Dị ứng thuốc: Không', font=unicode_font_med, fill=font_color)

    draw.text((150, 760), '1. ' + patient_drug, font=unicode_font_med, fill=font_color)
    draw.text((150, 860), '2. ' + gen_list_drug(), font=unicode_font_med, fill=font_color)
    draw.text((150, 960), '3. ' + gen_list_drug(), font=unicode_font_med, fill=font_color)
    draw.text((1000, 760), str(random.randint(1, 10)) + '   ' + random.choice(amount), 
                font=unicode_font_med, fill=font_color)
    draw.text((1000, 860), str(random.randint(1, 10)) + '   ' + random.choice(amount), 
                font=unicode_font_med, fill=font_color)
    draw.text((1000, 960), str(random.randint(1, 10)) + '   ' + random.choice(amount), 
                font=unicode_font_med, fill=font_color)
    draw.text((60, 1200), 'Lời dặn : ', font=unicode_font_small, fill=font_color)
    draw.text((820, 1400), patient_date, font=unicode_font_med, fill=font_color)
    draw.text((1010, 1440), 'Bác sĩ', font=unicode_font_med, fill=font_color)
    draw.text((910, 1700), doctor_name, font=unicode_font_med, fill=font_color)

    # img.save("text.jpg")
    return img


def distort(img, inx):
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # Distorts - 11 types
    inx = str(inx)
    blur(img, inx)
    compress(img, inx)
    color(img, inx)
    noise(img, inx)


def main():

    # Prepair data
    hospital_location = gen_hospital_location()

    patient_id = gen_patient_id()
    patient_name = gen_patient_name()
    patient_location = gen_patient_location()
    patient_age = gen_age()
    patient_phone = gen_phone()
    patient_gender = gen_gender()
    patient_health = gen_patient_health()
    patient_drug = gen_list_drug()
    # print(patient_drug)
    patient_date = gen_datatime()
    # print(patient_date)
    doctor_name = gen_patient_name()

    # Draw
    number_of_content = 2
    for inx in range(number_of_content):
        tic = time.time()
        img_1 = draw_form_1(hospital_location, patient_id, patient_name, patient_age,
                        patient_gender, patient_location, patient_phone,
                        patient_health, patient_drug, patient_date, doctor_name)
        distort(img_1, inx)
        
        img_2 = draw_form_2(hospital_location, patient_name, patient_age,
                        patient_gender, patient_location,
                        patient_health, patient_drug, patient_date, doctor_name)
        distort(img_2, inx)

        img_3 = draw_form_3(hospital_location, patient_id, patient_name, patient_age,
                        patient_gender, patient_location, patient_phone,
                        patient_health, patient_drug, patient_date, doctor_name)
        distort(img_3, inx)
        print('Generated with %d content(s) in %.2f s' % (inx + 1, time.time() - tic))


if __name__ == "__main__":
    main()
