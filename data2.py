
#从隐患描述文档提取标准答案
import os
import json

# 设置文件路径
txt_file_path = os.path.join(os.getcwd(), '.\dataset', '隐患描述文档.txt')
json_file_path = os.path.join(os.getcwd(), '.\dataset','Standard_output.json')

# 初始化一个空字典用于存储图片名称和隐患描述
data = {}

# 读取txt文件
with open(txt_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # 去除前后的空白符和换行符
        line = line.strip()
        if line:
            # 使用冒号分隔图片名称和隐患描述
            parts = line.split(':', 1)
            if len(parts) == 2:
                image_name = parts[0].strip()  # 图片名称
                hazard_description = parts[1].strip()  # 隐患描述
                # 将结果添加到字典中
                data[image_name] = hazard_description

# 将字典保存为json文件
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f"已成功生成 {json_file_path}")

