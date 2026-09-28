# # from transformers import AutoTokenizer, AutoModel
# # import torch
# # import numpy as np
# # import ipdb
# # # 加载BERT模型和分词器
# # tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
# # model = AutoModel.from_pretrained("bert-base-chinese")
# #
# # # 定义计算相似度的函数
# # def calc_similarity(s1, s2):
# #     # 对句子进行分词，并添加特殊标记
# #     inputs = tokenizer(s1, s2, return_tensors='pt', padding=True, truncation=True)
# #
# #     # 将输入传递给BERT模型，并获取输出
# #     with torch.no_grad():
# #         outputs = model(**inputs)
# #         embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
# #
# #     # 计算余弦相似度，并返回结果
# #     ipdb.set_trace()
# #     sim = np.dot(embeddings[0], embeddings[1]) / (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1]))
# #     return sim
# #
# #
# # prediction = "工人在施工现场进行作业时，并未全部穿着反光安全服，增加了被机械或车辆碰撞的风险。"
# # standard_answer = "未按规定穿戴反光安全服"
# #
# # similarity = calc_similarity(prediction, standard_answer)
# # print(f"相似度：{similarity:.4f}")
# # from transformers import AutoTokenizer, AutoModel
# # import torch
# # import numpy as np
# #
# # # 加载BERT模型和分词器
# # tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
# # model = AutoModel.from_pretrained("bert-base-chinese")
# #
# # # 定义计算相似度的函数
# # def calc_similarity(s1, s2):
# #     # 对句子进行分词，并添加特殊标记
# #     inputs = tokenizer([s1, s2], return_tensors='pt', padding=True, truncation=True)
# #
# #     # 将输入传递给BERT模型，并获取输出
# #     with torch.no_grad():
# #         outputs = model(**inputs)
# #         embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
# #
# #     # 计算余弦相似度，并返回结果
# #     sim = np.dot(embeddings[0], embeddings[1]) / (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1]))
# #     return sim
# #
# # # 测试函数
# # s1 = "工人在施工现场进行作业时，并未全部穿着反光安全服，增加了被机械或车辆碰撞的风险。"
# # s2 = "未按规定穿戴反光安全服"
# # similarity = calc_similarity(s1, s2)
# # print(f"相似度：{similarity:.4f}")
#
# # from transformers import AutoTokenizer, AutoModel
# # import torch
# # import numpy as np
# #
# # # 加载BERT模型和分词器
# # tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
# # model = AutoModel.from_pretrained("bert-base-chinese")
# #
# # # 定义计算相似度的函数
# # def calc_similarity(s1, s2):
# #     # 对句子进行分词，并添加特殊标记
# #     inputs = tokenizer([s1, s2], return_tensors='pt', padding=True, truncation=True)
# #
# #     # 将输入传递给BERT模型，并获取输出
# #     with torch.no_grad():
# #         outputs = model(**inputs)
# #         embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
# #
# #     # 计算余弦相似度，并返回结果
# #     sim = np.dot(embeddings[0], embeddings[1]) / (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1]))
# #     return sim
# #
# # # 从文件读取内容并提取句子对
# # def read_document(filename):
# #     sentence_pairs = []
# #     with open(filename, 'r', encoding='utf-8') as file:
# #         lines = file.readlines()
# #         for i in range(1, len(lines), 4):  # 每三行代表一个对比
# #             s1 = lines[i + 1].strip()  # 第一行是编号，第二行是句子1
# #             s2 = lines[i + 2].strip()  # 第三行是句子2
# #             sentence_pairs.append((s1, s2))
# #     return sentence_pairs
# #
# # # 从gpt.txt文件读取句子对
# # sentence_pairs = read_document('../result/glmn2/glmn2结果输出22.txt')
# #
# # # 遍历句子对并计算相似度
# # for idx, (s1, s2) in enumerate(sentence_pairs, 1):
# #     similarity = calc_similarity(s1, s2)
# #     print(f"文档 {idx} 的相似度：{similarity:.4f}")
# from transformers import AutoTokenizer, AutoModel
# import torch
# import numpy as np
#
# # 加载BERT模型和分词器
# tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
# model = AutoModel.from_pretrained("bert-base-chinese")
#
# # 定义计算相似度的函数
# def calc_similarity(s1, s2):
#     # 对句子进行分词，并添加特殊标记
#     inputs = tokenizer([s1, s2], return_tensors='pt', padding=True, truncation=True)
#
#     # 将输入传递给BERT模型，并获取输出
#     with torch.no_grad():
#         outputs = model(**inputs)
#         embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
#
#     # 计算余弦相似度，并返回结果
#     sim = np.dot(embeddings[0], embeddings[1]) / (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1]))
#     return sim
#
# # 从文件读取内容并提取句子对
# def read_document(filename):
#     sentence_pairs = []
#     with open(filename, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
#         for i in range(1, len(lines), 4):  # 每组句子对的位置是4n+2和4n+3
#             s1 = lines[i].strip()  # 第4n+2行是句子1
#             s2 = lines[i + 1].strip()  # 第4n+3行是句子2
#             sentence_pairs.append((s1, s2))
#     return sentence_pairs
#
# # 从gpt.txt文件读取句子对
# filename = '../result/glmn2/glmn2结果输出22.txt'
# sentence_pairs = read_document(filename)
#
# # 计算总的相似度（所有句子对的平均相似度）
# total_similarity = 0
# for idx, (s1, s2) in enumerate(sentence_pairs, 1):
#     similarity = calc_similarity(s1, s2)
#     total_similarity += similarity
#     print(f"文档 {idx} 的相似度：{similarity:.4f}")
#
# # 计算并输出所有句子对的平均相似度
# average_similarity = total_similarity / len(sentence_pairs)
# print(f"总的平均相似度：{average_similarity:.4f}")
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from collections import defaultdict

# 加载BERT模型和分词器
path="./bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(path)
model = AutoModel.from_pretrained(path)


# 定义计算相似度的函数
def calc_similarity(s1, s2):
    # 对句子进行分词，并添加特殊标记
    inputs = tokenizer([s1, s2], return_tensors='pt', padding=True, truncation=True)

    # 将输入传递给BERT模型，并获取输出
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()

    # 计算余弦相似度，并返回结果
    sim = np.dot(embeddings[0], embeddings[1]) / (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1]))
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
    for s1, s2 in sentence_pairs:
        similarity = calc_similarity(s1, s2)
        category_similarity += similarity

    # 计算类别的平均相似度
    average_category_similarity = category_similarity / category_pairs
    category_results[category] = {
        'total_similarity': category_similarity,
        'average_similarity': average_category_similarity
    }

    # 更新总相似度和总句子对数量
    total_similarity += category_similarity
    total_pairs += category_pairs

# 计算总体平均相似度
average_similarity = total_similarity / total_pairs

# 输出到文件
with open("result/deepseek_result/deepseek_lpips_bert.txt", "w", encoding="utf-8") as f:
    # 输出每个类别的结果
    for category, results in category_results.items():
        f.write(f"类别 {category}:\n")
        f.write(f"总相似度：{results['total_similarity']:.4f}\n")
        f.write(f"平均相似度：{results['average_similarity']:.4f}\n\n")

    # 输出所有类别的总体相似度
    f.write(f"所有类别的总相似度：{total_similarity:.4f}\n")
    f.write(f"所有类别的平均相似度：{average_similarity:.4f}\n")

print("相似度计算完成，结果已输出到 similarity_results.txt 文件。")
