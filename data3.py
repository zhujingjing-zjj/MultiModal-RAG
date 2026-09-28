#分别从标准答案和生成结果里提取隐患描述

import json
#标准输出

# 定义输入输出文件路径
glm_input_file = '.\dataset\deepseek_lpips_type2.json'
standard_input_file = '.\dataset\Standard_output.json'
output_file = './result/deepseek_result/deepseek_lpips_type2结果输出.txt'

# 加载 JSON 文件
with open(glm_input_file, 'r', encoding='utf-8') as f:
    glm_output = json.load(f)

with open(standard_input_file, 'r', encoding='utf-8') as f:
    standard_output = json.load(f)

# 创建并打开输出文件
with open(output_file, 'w', encoding='utf-8') as f:
    # 提取所需信息
    for item in glm_output:
        image_name = item['图片名称']
        glm_description = item['隐患描述']
        standard_description = standard_output.get(image_name, "描述未找到")
        
        # 格式化输出内容
        output_line = f"{image_name}\n{glm_description}\n{standard_description}\n\n"
        
        # 写入到文件
        f.write(output_line)

print(f"结果已成功保存到 {output_file}。")

