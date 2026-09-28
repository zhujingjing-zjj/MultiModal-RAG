import json
from collections import defaultdict
import re  # 用于忽略标点差异

# 读取JSON文件
with open('.\dataset\gpt4_lpips.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# 定义隐患类别字典
category_dict = {
    1: "未按规定穿戴反光安全服",
    2: "高处作业未正确使用安全带",
    3: "配电箱未及时锁闭",
    4: "未按规定配置灭火器、消防设施等",
    5: "现场防护栏等安全防护设施缺失、破损或设置不规范",
    6: "设备安全防护设施、装置缺失或失效",
    7: "起重吊装设备钢丝绳磨损、断丝严重，搭接长度不足",
    8: "汽车吊、随车吊、泵车支腿未全部伸出、未垫枕木进行作业",
    9: "基坑支护措施不到位",
    10: "灭火器未按规定要求放置",
    11: "未按规定设置接地线或接地不良",
    12: "安全警示标志标识缺失或设置不规范",
    13: "灭火器压力不足，灭火器、消防设施等未按规定进行检查、维护",
    14: "不符合“三级配电两级漏电保护、一机一闸一漏一箱”要求",
    15: "电缆外皮破损或敷设不规范"
}

# 为类别14添加标点不同的变体
category_dict[14] = [
    "不符合“三级配电两级漏电保护、一机一闸一漏一箱”要求",
    "不符合'三级配电两级漏电保护、一机一闸一漏一箱'要求"
]

# 初始化变量
correct_predictions = defaultdict(int)
total_predictions = defaultdict(int)
incorrect_predictions = defaultdict(list)  # 用来存储未匹配的结果
total_correct = 0  # 总的正确预测数量
total_images = 0  # 总的图片数量

# 处理JSON数据
for entry in json_data:
    # 获取图片名称中的数字（类别）
    img_name = entry["图片名称"]
    predicted_category = entry["隐患类别"]

    # 提取图片名称前面的数字
    actual_category_num = int(img_name.split('-')[0])

    # 根据数字获取实际类别（注意类别14是一个列表）
    actual_category = category_dict[actual_category_num]

    # 增加该类别的总预测数量
    total_predictions[actual_category_num] += 1

    # 判断预测是否正确，忽略标点符号差异
    if isinstance(actual_category, list):  # 如果类别14有多个变体
        # 清理两侧空格并去除所有标点进行比较
        actual_category_clean = [re.sub(r'[^\w\s]', '', cat).strip() for cat in actual_category]
        predicted_clean = re.sub(r'[^\w\s]', '', predicted_category).strip()
        if predicted_clean in actual_category_clean:
            correct_predictions[actual_category_num] += 1
            total_correct += 1
    else:
        # 清理两侧空格并去除所有标点进行比较
        actual_category_clean = re.sub(r'[^\w\s]', '', actual_category).strip()
        predicted_clean = re.sub(r'[^\w\s]', '', predicted_category).strip()
        if actual_category_clean == predicted_clean:
            correct_predictions[actual_category_num] += 1
            total_correct += 1

    total_images += 1

# 计算总的预测准确度
overall_accuracy = total_correct / total_images if total_images > 0 else 0

# 计算准确度并将结果写入文件
with open('./result/gpt4_lpips_result/gpt4_lpips_accuracy.txt', 'w', encoding='utf-8') as output_file:
    # 输出总的准确度
    output_file.write(f"所有图片的总预测准确度: {overall_accuracy:.2%}\n\n")

    # 输出每个类别的准确度
    for category_num in total_predictions:
        accuracy = correct_predictions[category_num] / total_predictions[category_num]
        output_file.write(f"类别 {category_num} ({category_dict[category_num]}) 的预测准确度: {accuracy:.2%}\n")

        # 如果该类别有未匹配结果，写入未匹配的信息
        if category_num in incorrect_predictions:
            for incorrect in incorrect_predictions[category_num]:
                output_file.write(
                    f"未匹配的图片: {incorrect['图片名称']} - 预测类别: {incorrect['预测类别']} - 实际类别: {incorrect['实际类别']}\n")

# import json
# from collections import defaultdict
# import re  # 用于忽略标点差异
#
# # 读取JSON文件
# with open('glmn2_output.json', 'r', encoding='utf-8') as file:
#     json_data = json.load(file)
#
# # 定义隐患类别字典
# category_dict = {
#     1: "未按规定穿戴反光安全服",
#     2: "高处作业未正确使用安全带",
#     3: "配电箱未及时锁闭",
#     4: "未按规定配置灭火器、消防设施等",
#     5: "现场防护栏等安全防护设施缺失、破损或设置不规范",
#     6: "设备安全防护设施、装置缺失或失效",
#     7: "起重吊装设备钢丝绳磨损、断丝严重，搭接长度不足",
#     8: "汽车吊、随车吊、泵车支腿未全部伸出、未垫枕木进行作业",
#     9: "基坑支护措施不到位",
#     10: "灭火器未按规定要求放置",
#     11: "未按规定设置接地线或接地不良",
#     12: "安全警示标志标识缺失或设置不规范",
#     13: "灭火器压力不足，灭火器、消防设施等未按规定进行检查、维护",
#     14: "不符合“三级配电两级漏电保护、一机一闸一漏一箱”要求",
#     15: "电缆外皮破损或敷设不规范"
# }
#
# # 为类别14添加标点不同的变体
# category_dict[14] = [
#     "不符合“三级配电两级漏电保护、一机一闸一漏一箱”要求",
#     "不符合'三级配电两级漏电保护、一机一闸一漏一箱'要求"
# ]
#
# # 初始化变量
# correct_predictions = defaultdict(int)
# total_predictions = defaultdict(int)
# incorrect_predictions = defaultdict(list)  # 用来存储未匹配的结果
#
# # 处理JSON数据
# for entry in json_data:
#     # 获取图片名称中的数字（类别）
#     img_name = entry["图片名称"]
#     predicted_category = entry["隐患类别"]
#
#     # 提取图片名称前面的数字
#     actual_category_num = int(img_name.split('-')[0])
#
#     # 根据数字获取实际类别（注意类别14是一个列表）
#     actual_category = category_dict[actual_category_num]
#
#     # 增加该类别的总预测数量
#     total_predictions[actual_category_num] += 1
#
#     # 判断预测是否正确，忽略标点符号差异
#     if isinstance(actual_category, list):  # 如果类别14有多个变体
#         # 清理两侧空格并去除所有标点进行比较
#         actual_category_clean = [re.sub(r'[^\w\s]', '', cat).strip() for cat in actual_category]
#         predicted_category_clean = re.sub(r'[^\w\s]', '', predicted_category).strip()
#
#         if predicted_category_clean in actual_category_clean:
#             correct_predictions[actual_category_num] += 1
#         else:
#             # 如果预测不正确，将错误信息存储到incorrect_predictions中
#             incorrect_predictions[actual_category_num].append({
#                 "图片名称": img_name,
#                 "实际类别": actual_category,
#                 "预测类别": predicted_category
#             })
#     else:  # 对于其他类别
#         if actual_category == predicted_category:
#             correct_predictions[actual_category_num] += 1
#         else:
#             incorrect_predictions[actual_category_num].append({
#                 "图片名称": img_name,
#                 "实际类别": actual_category,
#                 "预测类别": predicted_category
#             })
#
# # 计算准确度并将结果写入文件
# with open('../result/glmn2/accuracy_1.txt', 'w', encoding='utf-8') as output_file:
#     for category_num in total_predictions:
#         accuracy = correct_predictions[category_num] / total_predictions[category_num]
#         output_file.write(f"类别 {category_num} ({category_dict[category_num]}) 的预测准确度: {accuracy:.2%}\n")
#
#         # 如果该类别有未匹配结果，写入未匹配的信息
#         if category_num in incorrect_predictions:
#             for incorrect in incorrect_predictions[category_num]:
#                 output_file.write(
#                     f"图片名称: {incorrect['图片名称']}, 实际类别: {incorrect['实际类别']}, 预测类别: {incorrect['预测类别']}\n")
#
# # import json
# # from collections import defaultdict
# #
# # # 读取JSON文件
# # with open('llava_output.json', 'r', encoding='utf-8') as file:
# #     json_data = json.load(file)
# #
# # # 定义隐患类别字典
# # category_dict = {
# #     1: "未按规定穿戴反光安全服",
# #     2: "高处作业未正确使用安全带",
# #     3: "配电箱未及时锁闭",
# #     4: "未按规定配置灭火器、消防设施等",
# #     5: "现场防护栏等安全防护设施缺失、破损或设置不规范",
# #     6: "设备安全防护设施、装置缺失或失效",
# #     7: "起重吊装设备钢丝绳磨损、断丝严重，搭接长度不足",
# #     8: "汽车吊、随车吊、泵车支腿未全部伸出、未垫枕木进行作业",
# #     9: "基坑支护措施不到位",
# #     10: "灭火器未按规定要求放置",
# #     11: "未按规定设置接地线或接地不良",
# #     12: "安全警示标志标识缺失或设置不规范",
# #     13: "灭火器压力不足，灭火器、消防设施等未按规定进行检查、维护",
# #     14: "不符合“三级配电两级漏电保护、一机一闸一漏一箱”要求",
# #     15: "电缆外皮破损或敷设不规范"
# # }
# #
# # # 初始化变量
# # correct_predictions = defaultdict(int)
# # total_predictions = defaultdict(int)
# # incorrect_predictions = defaultdict(list)  # 用来存储未匹配的结果
# #
# # # 处理JSON数据
# # for entry in json_data:
# #     # 获取图片名称中的数字（类别）
# #     img_name = entry["图片名称"]
# #     predicted_category = entry["隐患类别"]
# #
# #     # 提取图片名称前面的数字
# #     actual_category_num = int(img_name.split('-')[0])
# #
# #     # 根据数字获取实际类别
# #     actual_category = category_dict[actual_category_num]
# #
# #     # 增加该类别的总预测数量
# #     total_predictions[actual_category_num] += 1
# #
# #     # 判断预测是否正确
# #     if actual_category == predicted_category:
# #         correct_predictions[actual_category_num] += 1
# #     else:
# #         # 如果预测不正确，将错误信息存储到incorrect_predictions中
# #         incorrect_predictions[actual_category_num].append({
# #             "图片名称": img_name,
# #             "实际类别": actual_category,
# #             "预测类别": predicted_category
# #         })
# #
# # # 计算准确度并将结果写入文件
# # with open('llava_accuracy_1.txt', 'w', encoding='utf-8') as output_file:
# #     for category_num in total_predictions:
# #         accuracy = correct_predictions[category_num] / total_predictions[category_num]
# #         output_file.write(f"类别 {category_num} ({category_dict[category_num]}) 的预测准确度: {accuracy:.2%}\n")
# #
# #         # 如果该类别有未匹配结果，写入未匹配的信息
# #         if category_num in incorrect_predictions and incorrect_predictions[category_num]:
# #             output_file.write(f"类别 {category_num} 的未匹配结果如下：\n")
# #             for item in incorrect_predictions[category_num]:
# #                 output_file.write(f"    图片名称: {item['图片名称']}, 实际类别: {item['实际类别']}, 预测类别: {item['预测类别']}\n")
# #             output_file.write("\n")
# #
# # print("准确度结果以及未匹配的详细信息已写入文件 gpt_accuracy_output_1.txt")
