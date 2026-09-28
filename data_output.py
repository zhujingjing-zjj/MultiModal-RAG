import base64
import random

from zhipuai import ZhipuAI
import argparse
import ipdb
import os
import os.path as op
import re
from dotenv import load_dotenv

load_dotenv()

# 获取密钥
api_key = os.getenv("ZHIPU_API_KEY")

prompt="隐患类别的共15类包括:['未按规定穿戴反光安全服', '高处作业未正确使用安全带', '配电箱未及时锁闭', '未按规定配置灭火器、消防设施等', " \
                 "'现场防护栏等安全防护设施缺失、破损或设置不规范', '设备安全防护设施、装置缺失或失效', '起重吊装设备钢丝绳磨损、断丝严重，搭接长度不足', " \
                 "'汽车吊、随车吊、泵车支腿未全部伸出、未垫枕木进行作业', '基坑支护措施不到位', '灭火器未按规定要求放置', '未按规定设置接地线或接地不良', " \
                 "'安全警示标志标识缺失或设置不规范', '灭火器压力不足，灭火器、消防设施等未按规定进行检查、维护'," \
                 "'不符合'三级配电两级漏电保护、一机一闸一漏一箱'要求', '电缆外皮破损或敷设不规范']\n\n" \
                 f"作为一个工地隐患检查人员，你的任务是根据文字描述，写出1条最明显的隐患类别，然后写出对应的隐患描述和整改意见。具体格式如下：\n" \
                 "隐患类别:<隐患类别>\n" \
                 "隐患描述:<隐患描述>\n" \
                 "整改意见:<整改意见>\n"

def read_txt(inputpath):
    data_out_dir='./textdata'
    os.makedirs(data_out_dir, exist_ok=True)
    with open(inputpath, 'r', encoding='utf-8') as infile:

            for line in infile:
                data_line = line.strip("\n") # 去除首尾换行符
                if(data_line.strip("	") == ""):
                    break
                #去除空白行
                title = str(re.findall("\d.*?(?=:)",data_line)).strip("[]'") # 提取序列
                context = data_line.strip(":"+title)
                output_filename = os.path.join(data_out_dir, f'{title}.txt')

                if op.exists(output_filename):
                    continue

                print(title)
                print(context)
                client = ZhipuAI(api_key)  # 填写您自己的APIKey

                response = client.chat.completions.create(
                    model="glm-4v-plus",  # 填写需要调用的模型名称
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": context
                                },
                                {
                                    "type": "text",
                                    "text": prompt
                                }
                            ]
                        }
                    ]
                )
                result = response.choices[0].message.content
                with open(output_filename, 'w', encoding='utf-8') as file:
                    file.write(result)


if __name__ == "__main__":
    input_path = './dataset/隐患描述文档.txt'
    read_txt(input_path)
