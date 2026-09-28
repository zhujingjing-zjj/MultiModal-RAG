import json

# 定义输入输出文件路径
glm_input_file = '.\dataset\gpt4_lpips.json'
output_file = './result/gpt4_lpips_result/gpt4_lpips类别结果输出.txt'

# 安全隐患描述字典
standard_descriptions = {
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

# 加载 JSON 文件
with open(glm_input_file, 'r', encoding='utf-8') as f:
    glm_output = json.load(f)

# 创建并打开输出文件
with open(output_file, 'w', encoding='utf-8') as f:
    # 提取所需信息
    for item in glm_output:
        image_name = item['图片名称']
        glm_description = item['隐患描述']

        # 获取标准描述
        try:
            category_number = int(image_name.split('-')[0])  # 获取类别序号（例如 1）
            standard_description = standard_descriptions.get(category_number, "描述未找到")
        except ValueError:
            standard_description = "描述未找到"

        # 格式化输出内容
        output_line = f"{image_name}\n{glm_description}\n{standard_description}\n\n"

        # 写入到文件
        f.write(output_line)

print(f"结果已成功保存到 {output_file}。")
