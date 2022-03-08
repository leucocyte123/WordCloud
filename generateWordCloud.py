import re
import sys
import nltk

import jieba
from numpy.core.fromnumeric import size
import wordcloud
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

ignored_words = {
    # '你', '我', '的', '了', '是', '啊', '吧', '不', '这', '吗', '有', '还', '也', '没', '就', '都', '好', '把', '被', '耶',
    '晚安', 
    '这个', '不会', '不是', '没有', '已经', '不要', '这样', '就是', '因为', '所以'
    '不能', '好像', '下周', '这里', '不用', '要个', '还有', '这是', '两个', '一边', '其实', '这么',
    # '好耶', '晚上',
    '晚上好',
    '哈哈', '哈哈哈', '哈哈哈哈',
}
# ignored_words = {}
added_words = {
    # '内鬼', 
    '雪狐', 
    '晚上好',
    '中秋快乐',
    '不能接受',
    '国庆快乐',
    '从天台上下来',
    '歪',
    '不要跳啊',
    '？'
    # '好人', '坏人', '好女人', '坏女人'
}
# added_words = {}

def filterChinese(line):
    regStr = ".*?([？\u4E00-\u9FA5]+).*?"
    ret = re.findall(regStr, line)
    if ret:
        return ret
    else:
        return []

def main():
    filename = sys.argv[1]

    # Import background image
    # shape_image = Image.open("materials/初号狐.png")
    # shape_image = shape_image.resize((int(shape_image.width * 2), int(shape_image.height * 2)))
    # shape_image = np.array(shape_image)

    # Read messages
    with open(filename, encoding='utf-8') as f:
        lines = [line for line in f.readlines()]

    # Fileter Chinese characters
    sentences = sum([filterChinese(line) for line in lines], [])

    # Add words to jieba
    for w in added_words:
        jieba.add_word(w)
    
    # Cut sentences
    words = sum([list(jieba.cut(sentence, cut_all=False)) for sentence in sentences], [])

    # Filter some words
    words = [w for w in words if w not in ignored_words]
    words = [w for w in words if w == '？' or len(w) > 1]
    
    # Count frequency
    frequency = nltk.FreqDist(words)

    # Generate word cloud
    font = r'C:\Windows\Fonts\MSYHL.TTC'
    
    wc = wordcloud.WordCloud(background_color="white", font_path=font, width=800, height=400)
    # wc = wordcloud.WordCloud(background_color='#7FFFD4', font_path=font, mask=shape_image)
    # wc = wordcloud.WordCloud(mode='RGBA', background_color='rgba(255, 255, 255, 0)', font_path=font, mask=shape_image)
    wc.generate_from_frequencies(frequency)
    
    # Set color from image
    # img_colors = wordcloud.ImageColorGenerator(shape_image)
    # wc.recolor(color_func=img_colors)

    # Add background
    # image = Image.fromarray(wc.to_array())
    # background = Image.open('materials/钢板.png').convert("RGBA")
    # print (image.size, background.size)
    # image = Image.alpha_composite(background, image)
    
    # Save to file
    wc.to_file('%s.png' % filename)
    # plt.figure()
    # plt.axis('off')
    # fig = plt.imshow(image, interpolation='nearest')
    # fig.axes.get_xaxis().set_visible(False)
    # fig.axes.get_yaxis().set_visible(False)
    # plt.savefig('log/test.png',
    #             bbox_inches='tight',
    #             pad_inches=0,
    #             format='png',
    #             dpi=300)

if __name__ == '__main__':
    main()