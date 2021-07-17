import re
import sys
import nltk

import jieba
import wordcloud

def filterChinese(line):
    regStr = ".*?([\u4E00-\u9FA5]+).*?"
    ret = re.findall(regStr, line)
    if ret:
        return ret
    else:
        return []

def main():
    filename = sys.argv[1]

    # Read messages
    with open(filename, encoding='utf-8') as f:
        lines = [line for line in f.readlines()]

    # Fileter Chinese characters
    sentences = sum([filterChinese(line) for line in lines], [])
    
    # Cut sentences
    words = sum([list(jieba.cut(sentence)) for sentence in sentences], [])
    
    # Count frequency
    frequency = nltk.FreqDist(words)
    
    # Generate word cloud
    font = r'C:\Windows\Fonts\MSYHL.TTC'
    wordcloud.WordCloud(background_color="white", font_path=font).generate_from_frequencies(frequency).to_file('%s.png' % filename)


if __name__ == '__main__':
    main()