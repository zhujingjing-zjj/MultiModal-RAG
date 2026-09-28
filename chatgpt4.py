import argparse
import base64
import random

import requests
import os
import os.path as op
import json
import ipdb
from dotenv import load_dotenv

load_dotenv()

# 获取密钥
api_key = os.getenv("OPENAI_API_KEY")


parser = argparse.ArgumentParser(prog='Chatgpt4 for test datasets', description='Use Chatgpt4 for identification of hidden dangers')
parser.add_argument('--output_dir', type = str, default='./gpt4_output')
parser.add_argument('--image_dir', type = str, default='./dataset/隐患图片')
parser.add_argument('--prompt_type', type = str, default='type_1', choices=['type_1', 'type_2', 'type_3', 'type_4'])
parser.add_argument('--result_num', type = str, default='1', choices=['1,3,5'])
parser.add_argument('--shuffle', type = bool, default=False)
parser.add_argument('--data_check_path',type = str,default='./data_check.json')
args = parser.parse_args()

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def get_example(example_num):

    with open(args.data_check_path, "r", encoding='utf8') as file:
        data = json.load(file)
        return data[str(example_num)]


# Function to get prompt
def get_prompt(prompt_type, result_num):
    # Getting example
    example = get_example(random.randint(1, 325))
    pic_path = example["图片地址"]
    type_text = example["隐患类别"]
    con_text = example["隐患描述"]
    if not op.isabs(pic_path):
        pic_path = op.join(args.image_dir, pic_path)
    base64_example = encode_image(pic_path)
    if prompt_type == 'type_1':
        prompt = f"作为一个工地隐患检查人员，你的任务是根据施工工地图片，写出{result_num}条最明显的隐患类别，然后写出对应的隐患描述和整改意见。"
    elif prompt_type == 'type_2':
        prompt = "隐患类别的共15类包括:['未按规定穿戴反光安全服', '高处作业未正确使用安全带', '配电箱未及时锁闭', '未按规定配置灭火器、消防设施等', " \
                 "'现场防护栏等安全防护设施缺失、破损或设置不规范', '设备安全防护设施、装置缺失或失效', '起重吊装设备钢丝绳磨损、断丝严重，搭接长度不足', " \
                 "'汽车吊、随车吊、泵车支腿未全部伸出、未垫枕木进行作业', '基坑支护措施不到位', '灭火器未按规定要求放置', '未按规定设置接地线或接地不良', " \
                 "'安全警示标志标识缺失或设置不规范', '灭火器压力不足，灭火器、消防设施等未按规定进行检查、维护'," \
                 "'不符合“三级配电两级漏电保护、一机一闸一漏一箱”要求', '电缆外皮破损或敷设不规范']\n\n" \
                 f"作为一个工地隐患检查人员，你的任务是根据施工工地图片，写出{result_num}条最明显的隐患类别，然后写出对应的隐患描述和整改意见。"
    elif prompt_type == 'type_3':
        prompt = f"作为一个工地隐患检查人员，你的任务是根据施工工地图片，写出{result_num}条最明显的隐患类别，然后写出对应的隐患描述和整改意见。具体格式如下：\n" \
                 "隐患类别:<隐患类别>\n" \
                 "隐患描述:<隐患描述>\n" \
                 "整改意见:<整改意见>\n"
    elif prompt_type == 'type_4':
        prompt = "隐患类别的共15类包括:['未按规定穿戴反光安全服', '高处作业未正确使用安全带', '配电箱未及时锁闭', '未按规定配置灭火器、消防设施等', " \
                 "'现场防护栏等安全防护设施缺失、破损或设置不规范', '设备安全防护设施、装置缺失或失效', '起重吊装设备钢丝绳磨损、断丝严重，搭接长度不足', " \
                 "'汽车吊、随车吊、泵车支腿未全部伸出、未垫枕木进行作业', '基坑支护措施不到位', '灭火器未按规定要求放置', '未按规定设置接地线或接地不良', " \
                 "'安全警示标志标识缺失或设置不规范', '灭火器压力不足，灭火器、消防设施等未按规定进行检查、维护'," \
                 "'不符合'三级配电两级漏电保护、一机一闸一漏一箱'要求', '电缆外皮破损或敷设不规范']\n\n" \
                 f"作为一个工地隐患检查人员，你的任务是根据施工工地图片，写出{result_num}条最明显的隐患类别，然后写出对应的隐患描述和整改意见。具体格式如下：\n" \
                 "隐患类别:<隐患类别>\n" \
                 "隐患描述:<隐患描述>\n" \
                 "整改意见:<整改意见>\n" \
                 "以下是一个例子：\n" \
                 f"施工图片:{base64_example}\n" \
                 f"隐患类别:{type_text}\n" \
                 f"隐患描述:{con_text}\n" \
                 "请根据上述例子，识别下面图片，给出隐患类别和隐患描述的同时给出整改意见"
    elif prompt_type == 'type_5':
        prompt = "隐患类别的共15类包括:['未按规定穿戴反光安全服', '高处作业未正确使用安全带', '配电箱未及时锁闭', '未按规定配置灭火器、消防设施等', " \
                 "'现场防护栏等安全防护设施缺失、破损或设置不规范', '设备安全防护设施、装置缺失或失效', '起重吊装设备钢丝绳磨损、断丝严重，搭接长度不足', " \
                 "'汽车吊、随车吊、泵车支腿未全部伸出、未垫枕木进行作业', '基坑支护措施不到位', '灭火器未按规定要求放置', '未按规定设置接地线或接地不良', " \
                 "'安全警示标志标识缺失或设置不规范', '灭火器压力不足，灭火器、消防设施等未按规定进行检查、维护'," \
                 "'不符合'三级配电两级漏电保护、一机一闸一漏一箱'要求', '电缆外皮破损或敷设不规范']\n\n" \
                 f"作为一个工地隐患检查人员，你的任务是根据施工工地图片，写出{result_num}条最明显的隐患类别，然后写出对应的隐患描述和整改意见。具体格式如下：\n" \
                 "隐患类别:<隐患类别>\n" \
                 "隐患描述:<隐患描述>\n" \
                 "整改意见:<整改意见>\n"
    elif prompt_type == 'type_6':
        prompt = "隐患类别的共15类包括:['未按规定穿戴反光安全服', '高处作业未正确使用安全带', '配电箱未及时锁闭', '未按规定配置灭火器、消防设施等', " \
                 "'现场防护栏等安全防护设施缺失、破损或设置不规范', '设备安全防护设施、装置缺失或失效', '起重吊装设备钢丝绳磨损、断丝严重，搭接长度不足', " \
                 "'汽车吊、随车吊、泵车支腿未全部伸出、未垫枕木进行作业', '基坑支护措施不到位', '灭火器未按规定要求放置', '未按规定设置接地线或接地不良', " \
                 "'安全警示标志标识缺失或设置不规范', '灭火器压力不足，灭火器、消防设施等未按规定进行检查、维护'," \
                 "'不符合'三级配电两级漏电保护、一机一闸一漏一箱'要求', '电缆外皮破损或敷设不规范']\n\n" \
                 f"作为一个工地隐患检查人员，你的任务是根据施工工地图片，先找到图片中人员、设施设备或者灭火器等关键目标物，再根据目标物在以上15类隐患类别中确定图片所属的隐患类别，写出{result_num}条最明显的隐患类别，然后写出对应的隐患描述和整改意见。具体格式如下：\n" \
                 "隐患类别:<隐患类别>\n" \
                 "隐患描述:<隐患描述>\n" \
                 "整改意见:<整改意见>\n"
    elif prompt_type == 'type_7':
        prompt = "隐患类别的共15类包括:['未按规定穿戴反光安全服', '高处作业未正确使用安全带', '配电箱未及时锁闭', '未按规定配置灭火器、消防设施等', " \
                 "'现场防护栏等安全防护设施缺失、破损或设置不规范', '设备安全防护设施、装置缺失或失效', '起重吊装设备钢丝绳磨损、断丝严重，搭接长度不足', " \
                 "'汽车吊、随车吊、泵车支腿未全部伸出、未垫枕木进行作业', '基坑支护措施不到位', '灭火器未按规定要求放置', '未按规定设置接地线或接地不良', " \
                 "'安全警示标志标识缺失或设置不规范', '灭火器压力不足，灭火器、消防设施等未按规定进行检查、维护'," \
                 "'不符合'三级配电两级漏电保护、一机一闸一漏一箱'要求', '电缆外皮破损或敷设不规范']\n\n" \
                 f"作为一个工地隐患检查人员，你的任务是根据施工工地图片，先找到图片中人员、设施设备或者灭火器等关键主体物，判断是否存在相关隐患，再根据图片的场景背景，判断是否存在相关隐患，最后在以上15类隐患类别中确定图片所属的隐患类别，写出{result_num}条最明显的隐患类别，然后写出对应的隐患描述和整改意见。具体格式如下：\n" \
                 "隐患类别:<隐患类别>\n" \
                 "隐患描述:<隐患描述>\n" \
                 "整改意见:<整改意见>\n"
    elif prompt_type == 'type_8':
        prompt = "隐患类别的共15类包括:['未按规定穿戴反光安全服', '高处作业未正确使用安全带', '配电箱未及时锁闭', '未按规定配置灭火器、消防设施等', " \
                 "'现场防护栏等安全防护设施缺失、破损或设置不规范', '设备安全防护设施、装置缺失或失效', '起重吊装设备钢丝绳磨损、断丝严重，搭接长度不足', " \
                 "'汽车吊、随车吊、泵车支腿未全部伸出、未垫枕木进行作业', '基坑支护措施不到位', '灭火器未按规定要求放置', '未按规定设置接地线或接地不良', " \
                 "'安全警示标志标识缺失或设置不规范', '灭火器压力不足，灭火器、消防设施等未按规定进行检查、维护'," \
                 "'不符合'三级配电两级漏电保护、一机一闸一漏一箱'要求', '电缆外皮破损或敷设不规范']\n\n" \
                 f"作为一个工地隐患检查人员，你的任务是根据施工工地图片，先判断图片中所有可能的隐患类别，再找到图片中人员、设备或者标识等关键目标物，结合背景信息和关键目标物写出可能隐患类别中{result_num}条最明显的隐患类别，然后写出对应的隐患描述和整改意见。具体格式如下：\n" \
                 "隐患类别:<隐患类别>\n" \
                 "隐患描述:<隐患描述>\n" \
                 "整改意见:<整改意见>\n"
    return prompt

image_list = os.listdir(args.image_dir)
if args.shuffle:
    random.shuffle(image_list)
    output_dir = os.path.join(args.output_dir, args.prompt_type, args.result_num + '_' + 'shuffle')
else:
    output_dir = os.path.join(args.output_dir, args.prompt_type, args.result_num)
os.makedirs(output_dir, exist_ok=True)

i = 1
for image in image_list:
    # image_dir = os.path.join(args.image_dir, image)
    # image_name = os.listdir(image_dir)[0]
    # image_path = os.path.join(args.image_dir, image, image_name)

    image_path = os.path.join(args.image_dir, image)
    result_name = image.split('.')[0]
    output_filename = os.path.join(output_dir, f'{result_name}.txt')
    if result_name == '11-23':
        continue
    if result_name == '15-12':
        continue

    if op.exists(output_filename):
        continue

    # Getting the base64 string
    base64_image = encode_image(image_path)

    # Getting the prompt
    prompt = get_prompt(args.prompt_type, args.result_num)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{prompt}",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.chatfire.cn/plus/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    result = response.json()['choices'][0]['message']['content']
    # result_name = image.split('.')[0]
    # output_filename = os.path.join(output_dir, f'{result_name}.txt')
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(result)

    i+=1

    if i == 325:
        ipdb.set_trace()
