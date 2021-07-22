import re
import sys
import nltk

import jieba
import wordcloud
import numpy as np
from PIL import Image

ignored_words = {'你', '我', '的', '了', '是', '啊', '吧', '不', '这', '吗', '有', '还', '也', '没', '就', '都'}
# ignored_words = {}
added_words = {'内鬼'}

def filterChinese(line):
    regStr = ".*?([\u4E00-\u9FA5]+).*?"
    ret = re.findall(regStr, line)
    if ret:
        return ret
    else:
        return []

def main():
    filename = sys.argv[1]

    # Import background image
    img = Image.open("materials/初号狐.png")
    img = img.resize((int(img.width * 2), int(img.height * 2)))
    background_Image = np.array(img)

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
    
    # Count frequency
    frequency = nltk.FreqDist(words)

    # Generate word cloud
    font = r'C:\Windows\Fonts\MSYHL.TTC'
    wc = wordcloud.WordCloud(background_color="white", font_path=font, mask=background_Image)
    # wc = wordcloud.WordCloud(background_color="white", font_path=font, width=800, height=400)
    wc.generate_from_frequencies(frequency)
    
    # Set color from image
    img_colors = wordcloud.ImageColorGenerator(background_Image)
    wc.recolor(color_func=img_colors)
    
    # Save to file
    wc.to_file('%s.png' % filename)


if __name__ == '__main__':
    main()