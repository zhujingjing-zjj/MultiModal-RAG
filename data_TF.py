import jieba
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity

# 定义计算TF-IDF相似度的函数
def calc_similarity(s1, s2):
    # 使用jieba进行分词
    s1_words = ' '.join(jieba.cut(s1))
    s2_words = ' '.join(jieba.cut(s2))

    # 初始化TF-IDF向量化器
    vectorizer = TfidfVectorizer()

    # 计算TF-IDF矩阵
    tfidf_matrix = vectorizer.fit_transform([s1_words, s2_words])

    # 计算余弦相似度
    sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return sim

# 从文件读取内容并提取句子对
def read_document(filename):
    sentence_pairs_by_category = defaultdict(list)  # 存储按类别分组的句子对
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i in range(1, len(lines), 4):  # 每组句子对的位置是4n+2和4n+3
            category = lines[i - 1].strip().split('-')[0]  # 获取类别a（即文件名中的a-b格式，取a部分）
            s1 = lines[i].strip()  # 第4n+2行是句子1
            s2 = lines[i + 1].strip()  # 第4n+3行是句子2
            sentence_pairs_by_category[category].append((s1, s2))  # 按类别存储句子对
    return sentence_pairs_by_category

# 从gpt.txt文件读取句子对
filename = 'result/deepseek_result/deepseek_lpips_type2结果输出.txt'
sentence_pairs_by_category = read_document(filename)

# 存储每个类别的相似度结果
category_results = {}

# 计算每个类别的相似度并存储结果
total_similarity = 0
total_pairs = 0

for category, sentence_pairs in sentence_pairs_by_category.items():
    category_similarity = 0
    category_pairs = len(sentence_pairs)

    # 计算类别内所有句子对的相似度
    for s1, s2 in sentence_pairs:
        sim = calc_similarity(s1, s2)
        category_similarity += sim

    # 计算该类别的平均相似度
    category_results[category] = category_similarity / category_pairs
    total_similarity += category_similarity
    total_pairs += category_pairs

# 计算整体的平均相似度
average_similarity = total_similarity / total_pairs
print(f"Overall average similarity: {average_similarity:.4f}")

# 输出每个类别的平均相似度
for category, avg_sim in category_results.items():
    print(f"Category {category} average similarity: {avg_sim:.4f}")
