import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from random import randint


# 用于书写单个字的函数，输入参数为x坐标，y坐标，要写的字
def write_word(x_coordinate, y_coordinate, word_, draw_):
    x = x_coordinate + randint(0, page_parameter_dict['word_x_distance_offset'])
    y = y_coordinate + randint(0, page_parameter_dict['word_y_distance_offset'])
    draw_.text((x, y), word_, font_color, font=font)


# 设置字体相关参数，包括所用字体，字体大小，字体颜色
font = ImageFont.truetype('life.ttf', 40, encoding='utf-8')
font_color = (0, 0, 0)    # 字体颜色设置为黑色

# 读入背景图片
image = cv2.imread('back_picture.jpg')

# 背景图片格式转换
cv2_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
pil_img = Image.fromarray(cv2_img)

# 重要的页面参数记录
page_parameter_dict = {
    "page_width": 1684,             # 页面宽度 1684 个像素
    "page_height": 2386,            # 页面长度 2386 个像素
    "x_margin_length": 32,          # 页面两边空白宽度 32
    "y_first_line": 175,            # 页面第一行 y 坐标 175
    "x_title": 640,                 # 首行标题第一个字 x 坐标 640
    "line_num": 42,                 # 一页有 40 行
    "line_distance": 50.5,          # 行间距 50.5
    "word_distance": 40,            # 字间距 40
    "word_num": 40,                 # 一行能写 40 个字
    "word_x_distance_offset": 8,    # 单个字左右浮动，范围为 0～8
    "word_y_distance_offset": 4     # 单个字上下浮动，范围为 0～4
}

# 添加内容
draw = ImageDraw.Draw(pil_img)

# 从 txt 文件内读取文本信息
txt_file = open('text.txt', 'r')
text = txt_file.read()    # 读取全文，每段之间以 '\n' 分隔
txt_file.close()
text_list_0 = text.split('\n')
# 去除掉段内的空格
text_list = list()
for paragraph in text_list_0:
    paragraph = paragraph.replace(' ', '')
    paragraph = paragraph.replace('（', '(')
    paragraph = paragraph.replace('）', ')')
    paragraph = paragraph.replace('《', '')
    paragraph = paragraph.replace('》', '')
    text_list.append(paragraph)


# 文本信息可能包含字母，书名号等
alphabet = '（）()《》qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
# 第一个出现的字母不用缩进，但是后续都需要

# 设置行计数器，因为可能涉及到换页问题
page_num = 0
line_num = 0

# 书写标题，默认第一行足够写完，不设置换行
title = text_list[0]
word_x = page_parameter_dict["x_title"]
word_y = page_parameter_dict["y_first_line"]
for word in title:
    write_word(word_x, word_y, word, draw)
    if word in alphabet:
        word_x += page_parameter_dict["word_distance"] - 20
    else:
        word_x += page_parameter_dict["word_distance"]
line_num += 1

# 书写剩余的每一段，段首空两个字的距离，写之前首先把上一行写完后的指针位置移动到本行的起始位置
for num in range(len(text_list)-1):
    paragraph = text_list[num+1]    # 本段文本信息
    # word_x = page_parameter_dict["x_margin_length"] + 70    # 段首空两个字
    word_x = page_parameter_dict["x_margin_length"]
    word_y += page_parameter_dict["line_distance"]    # y 坐标对应到新的一行
    first_line = True
    word_num = 0    # 记录本行已写字数
    for word in paragraph:    # 书写每一个字，注意写完后 word_x 自增，一行写满后换行
        write_word(word_x, word_y, word, draw)
        if word in alphabet:
            word_x += page_parameter_dict["word_distance"] - 20
        else:
            word_x += page_parameter_dict["word_distance"]
        word_num += 1
        if first_line:
            # if word_num == 38:    # 第一行已写满
            if word_num == 40:
                word_num = 0  # 刷新单词计数器

                line_num += 1
                first_line = False  # 之后的都不是第一行
                word_y += page_parameter_dict["line_distance"]    # y 坐标对应到新的一行
                word_x = page_parameter_dict["x_margin_length"]    # x 坐标回归行首位置
                # 每一次行写满都要检查一下，如果写满则换页
                if line_num == page_parameter_dict['line_num']:
                    print("一页写完，保存图片{}.jpg".format(page_num))
                    cv2img2 = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                    cv2.imwrite(str(page_num) + '.jpg', cv2img2)
                    line_num = 0
                    pil_img = Image.fromarray(cv2_img)
                    draw = ImageDraw.Draw(pil_img)
                    word_y = page_parameter_dict["y_first_line"]
                    page_num += 1
        else:
            if word_num == 40:    # 本行已写满（非第一行）
                word_num = 0  # 刷新单词计数器

                line_num += 1
                word_y += page_parameter_dict["line_distance"]    # y 坐标对应到新的一行
                word_x = page_parameter_dict["x_margin_length"]  # x 坐标回归行首位置
                # 每一次行写满都要检查一下，如果写满则换页
                if line_num == page_parameter_dict['line_num']:
                    print("一页写完，保存图片{}.jpg".format(page_num))
                    cv2img2 = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                    cv2.imwrite(str(page_num) + '.jpg', cv2img2)
                    line_num = 0
                    pil_img = Image.fromarray(cv2_img)
                    draw = ImageDraw.Draw(pil_img)
                    word_y = page_parameter_dict["y_first_line"]
                    page_num += 1

    # 可能本段写完也不满一行，这个时候也要增加行数
    line_num += 1

# 保存图片
cv2img2 = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
cv2.imwrite(str(page_num)+'.jpg', cv2img2)
print("一页写完，保存图片{}.jpg".format(page_num))
