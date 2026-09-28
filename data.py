#生成结果中提取并清洗文本
import os
import json
import re

def clean_text(text):
    """
    去掉文本中的【】符号。
    """
    return re.sub(r'[【】]', '', text)

def extract_info_from_text(content):
    """
    使用正则表达式从文本内容中提取隐患类别、隐患描述和整改意见。
    """
    # 定义正则模式
    category_pattern = r'隐患类别\s*[:：]\s*(.+)'
    description_pattern = r'隐患描述\s*[:：]\s*(.+)'
    suggestion_pattern = r'整改意见\s*[:：]\s*(.+)'

    # 进行匹配
    category = re.search(category_pattern, content)
    description = re.search(description_pattern, content)
    suggestion = re.search(suggestion_pattern, content)

    # 返回提取结果并清理文本
    return {
        "隐患类别": clean_text(category.group(1).strip()) if category else "",
        "隐患描述": clean_text(description.group(1).strip()) if description else "",
        "整改意见": clean_text(suggestion.group(1).strip()) if suggestion else ""
    }

def main():
    """
    主函数，负责遍历文件夹、解析文件内容并保存结果到JSON文件。
    """
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 定义Glm文件夹的路径
    input_dir = os.path.join(current_dir, '.\deepseek_output_lpips/type_2/1')

    # 检查Glm文件夹是否存在
    if not os.path.exists(input_dir):
        print(f"错误：找不到目录 {input_dir}")
        return

    # 初始化结果列表
    results = []

    # 遍历Glm文件夹中的所有txt文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"无法读取文件 {filename}：{e}")
                continue

            # 尝试从内容中提取JSON数据
            try:
                # 使用正则查找JSON块
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())
                    category = clean_text(data.get("隐患类别", ""))
                    description = clean_text(data.get("隐患描述", ""))
                    suggestion = clean_text(data.get("整改意见", ""))
                else:
                    raise ValueError("未找到JSON格式的数据")
            except:
                # 如果不是JSON格式，则使用文本解析
                data = extract_info_from_text(content)
                category = data["隐患类别"]
                description = data["隐患描述"]
                suggestion = data["整改意见"]

            # 去掉文件名的后缀 .txt
            image_name = os.path.splitext(filename)[0]

            # 构建记录字典，将“文档名称”改为“图片名称”
            entry = {
                "图片名称": image_name,
                "隐患类别": category,
                "隐患描述": description,
                "整改意见": suggestion
            }

            # 添加到结果列表
            results.append(entry)

    # 定义输出JSON文件的路径
    output_file = os.path.join('.\dataset', 'deepseek_lpips_type2.json')

    # 将结果写入JSON文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"提取完成，结果已保存到 {output_file}")
    except Exception as e:
        print(f"无法写入JSON文件：{e}")

if __name__ == "__main__":
    main()

# import os
# import json
# import re

# def extract_info_from_text(content):
#     """
#     使用正则表达式从文本内容中提取隐患类别、隐患描述和整改意见。
#     """
#     # 定义正则模式
#     category_pattern = r'隐患类别\s*[:：]\s*(.+)'
#     description_pattern = r'隐患描述\s*[:：]\s*(.+)'
#     suggestion_pattern = r'整改意见\s*[:：]\s*(.+)'

#     # 进行匹配
#     category = re.search(category_pattern, content)
#     description = re.search(description_pattern, content)
#     suggestion = re.search(suggestion_pattern, content)

#     # 返回提取结果
#     return {
#         "隐患类别": category.group(1).strip() if category else "",
#         "隐患描述": description.group(1).strip() if description else "",
#         "整改意见": suggestion.group(1).strip() if suggestion else ""
#     }

# def main():
#     """
#     主函数，负责遍历文件夹、解析文件内容并保存结果到JSON文件。
#     """
#     # 获取当前脚本所在目录
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     # 定义Glm文件夹的路径
#     input_dir = os.path.join(current_dir, 'Glm')

#     # 检查Glm文件夹是否存在
#     if not os.path.exists(input_dir):
#         print(f"错误：找不到目录 {input_dir}")
#         return

#     # 初始化结果列表
#     results = []

#     # 遍历Glm文件夹中的所有txt文件
#     for filename in os.listdir(input_dir):
#         if filename.endswith('.txt'):
#             file_path = os.path.join(input_dir, filename)
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     content = f.read()
#             except Exception as e:
#                 print(f"无法读取文件 {filename}：{e}")
#                 continue

#             # 尝试从内容中提取JSON数据
#             try:
#                 # 使用正则查找JSON块
#                 json_match = re.search(r'\{.*\}', content, re.DOTALL)
#                 if json_match:
#                     data = json.loads(json_match.group())
#                     category = data.get("隐患类别", "")
#                     description = data.get("隐患描述", "")
#                     suggestion = data.get("整改意见", "")
#                 else:
#                     raise ValueError("未找到JSON格式的数据")
#             except:
#                 # 如果不是JSON格式，则使用文本解析
#                 data = extract_info_from_text(content)
#                 category = data["隐患类别"]
#                 description = data["隐患描述"]
#                 suggestion = data["整改意见"]

#             # 去掉文件名的后缀 .txt
#             image_name = os.path.splitext(filename)[0]

#             # 构建记录字典，将“文档名称”改为“图片名称”
#             entry = {
#                 "图片名称": image_name,
#                 "隐患类别": category,
#                 "隐患描述": description,
#                 "整改意见": suggestion
#             }

#             # 添加到结果列表
#             results.append(entry)

#     # 定义输出JSON文件的路径
#     output_file = os.path.join(current_dir, 'output.json')

#     # 将结果写入JSON文件
#     try:
#         with open(output_file, 'w', encoding='utf-8') as f:
#             json.dump(results, f, ensure_ascii=False, indent=4)
#         print(f"提取完成，结果已保存到 {output_file}")
#     except Exception as e:
#         print(f"无法写入JSON文件：{e}")

# if __name__ == "__main__":
#     main()
