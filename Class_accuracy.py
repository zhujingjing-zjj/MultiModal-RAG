# import json

# # 定义隐患类别的字典映射
# category_mapping = {
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

# # 假设你的json数据是保存在文件data.json中
# with open('./dataset/Glm_output.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # 统计正确和总数
# correct_count = 0
# total_count = len(data)

# # 遍历每一个隐患项
# for item in data:
#     # 提取图片名称中的第一个数字
#     image_name = item['图片名称']
#     first_number = int(image_name.split('-')[0])

#     # 获取该数字对应的隐患类别
#     correct_category = category_mapping.get(first_number)

#     # 判断当前的隐患类别是否与图片名称对应
#     if item['隐患类别'] == correct_category:
#         correct_count += 1
#     else:
#         print(f"图片名称: {image_name} 分类错误: 预期类别为 {correct_category}, 实际为 {item['隐患类别']}")

# # 计算准确率
# accuracy = correct_count / total_count * 100
# print(f"隐患类别判断的准确率为: {accuracy:.2f}%")
import json

# 定义隐患类别的字典映射
category_mapping = {
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

# 假设你的json数据是保存在文件data.json中
with open('.\dataset\deepseek_lpips_type2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 创建一个文件，将输出写入其中
with open('./result/deepseek_result/deepseek_lpips_output.txt', 'w', encoding='utf-8') as output_file:
    # 统计正确和总数
    correct_count = 0
    total_count = len(data)

    # 遍历每一个隐患项
    for item in data:
        # 提取图片名称中的第一个数字
        image_name = item['图片名称']
        first_number = int(image_name.split('-')[0])

        # 获取该数字对应的隐患类别
        correct_category = category_mapping.get(first_number)

        # 判断当前的隐患类别是否与图片名称对应
        if item['隐患类别'] == correct_category:
            correct_count += 1
        else:
            output_file.write(
                f"图片名称: {image_name} 分类错误: 预期类别为 {correct_category}, 实际为 {item['隐患类别']}\n")

    # 计算准确率
    accuracy = correct_count / total_count * 100
    output_file.write(f"\n隐患类别判断的准确率为: {accuracy:.2f}%\n")

print("结果已经写入到 output.txt 文件中。")
