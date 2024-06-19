import streamlit as st
import jieba
import requests
from collections import Counter
import re
import string
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
# 定义数据清洗函数
def clean_text(text):
    text = text.replace('\n', '').replace(' ', '').strip()
    return text

# 定义分词函数，使用 jieba 进行中文分词
def segment(text):
    stopwords = ['的', '了', '在', '是', '我', '你', '他', '她', '它', '们', '这', '那', '之', '与', '和', '或']
    punctuation = string.punctuation
    text = text.translate(str.maketrans('', '', punctuation)).replace('\n', '')
    words = jieba.lcut(text)
    words = [word for word in words if word not in stopwords]
    return words

# 去除数字和标点符号
def remove_punctuation_and_numbers(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    return re.sub('\d+', '', text)

def main():
    st.title("文本分析与词云可视化")

    # 用户输入 URL
    url = st.text_input("请输入网页 URL:")

    if url:
        # 发送 HTTP 请求获取网页内容
        response = requests.get(url)
        response.encoding = 'utf-8'
        text = response.text

        # 清洗文本
        text = clean_text(text)
        text = remove_punctuation_and_numbers(text)

        # 分词
        words = segment(text)

        # 统计词频
        word_counts = Counter(words)

        # 获取最常见的20个词
        top_words = word_counts.most_common(20)

        # 绘制条形图
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh([word[0] for word in top_words], [word[1] for word in top_words], color='skyblue')
        ax.set_xlabel('词频')
        ax.set_title('词频统计条形图')
        ax.invert_yaxis()  # 颠倒y轴顺序，使得最常见的词在上方

        # 显示图表
        st.pyplot(fig)

        # 显示词频统计结果
        st.write("最常见的20个词及其词频：")
        for word, count in top_words:
            st.write(f"{word}: {count}")

if __name__ == "__main__":
    main()