import argparse
import base64
import random

import requests
import os
import os.path as op
import json
import ipdb
import argparse
import os
import os.path as op
import torch
import lpips
from PIL import Image
import torchvision.transforms as transforms
parser = argparse.ArgumentParser(prog='Chatgpt4 for test datasets', description='Use Chatgpt4 for identification of hidden dangers')
parser.add_argument('--output_dir', type = str, default='./dataset')
parser.add_argument('--image_dir', type = str, default='./dataset/隐患图片')
parser.add_argument('--prompt_type', type = str, default='type_4', choices=['type_1', 'type_2', 'type_3', 'type_4'])
parser.add_argument('--result_num', type = str, default='1', choices=['1,3,5'])
parser.add_argument('--shuffle', type = bool, default=False)
parser.add_argument('--data_check_path',type = str,default='data_check.json')
args = parser.parse_args()
def split_data(image_list, data):
    '''
    每个隐患类别，选择两个放进检索库
    '''
    val_image_list = []
    example_data_image_list = []
    example_data = {}

    cat_id_image_list = {}
    for img in image_list:
        result_name = img.split('.')[0]
        if result_name == '11-23':
            continue
        if result_name == '14-11':
            continue
        if result_name == '15-12':
            continue
        img_cat = img.split('-')[0]
        if img_cat in cat_id_image_list.keys():
            cat_id_image_list[img_cat].append(img)
        else:
            cat_id_image_list[img_cat]=[img]


    for cat in cat_id_image_list:
        # index1, index2 = random.sample(range(len(cat_id_image_list[cat])), 2)
        # index1, index2 = random.sample(range(len(cat_id_image_list[cat])), int(len(cat_id_image_list[cat])/2))

        # ipdb.set_trace()
        # # 获取被选的元素
        # selected_elements = [cat_id_image_list[cat][index1], cat_id_image_list[cat][index2]]
        # 获取被选的元素
        selected_elements = cat_id_image_list[cat][:int(len(cat_id_image_list[cat])/3)]
        example_data_image_list+=selected_elements
        # 获取没有被选的元素
        not_selected_elements = [elem for elem in cat_id_image_list[cat] if elem not in selected_elements]
        val_image_list+=not_selected_elements
        for id in data:
            if data[id]['图片地址'].split('\\')[1] in selected_elements:
                example_data[id] = data[id]

    return example_data, val_image_list

if __name__ == '__main__':
    image_list = os.listdir(args.image_dir)
    data_test=os.path.join(args.output_dir,"data_test.jsonl")
    if args.shuffle:
        random.shuffle(image_list)
        output_dir = os.path.join(args.output_dir, args.prompt_type, args.result_num + '_' + 'shuffle')
    else:
        output_dir = os.path.join(args.output_dir, args.prompt_type, args.result_num)
    os.makedirs(output_dir, exist_ok=True)

    with open(args.data_check_path, "r", encoding='utf8') as file:
        data = json.load(file)
    example_data, val_image_list = split_data(image_list, data)
    print(example_data)
    # text=[]
    for id in example_data:
        img_path=data[id]['图片地址'].replace('\\', '/')
        img_des=data[id]['隐患描述']
        img_class=data[id]['隐患类别']
        t={
            "messages": [{
                "role": "system",
                "content": "你是一个工地隐患检查人员。"
            },
                {
                    "role": "user",
                    "content": "根据施工工地图片描述下列图片存在的安全隐患"
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_path}"
                            }
                        }]
                },
                {
                    "role": "assistant",
                    "content": "隐患类别:"+img_class+"\n"+"隐患描述:"+img_des
                },
                ]
        }
        # text.append(t)
    with open(data_test, 'w',encoding='utf-8') as f:
            json.dump(t, f, allow_nan=False, indent=4,ensure_ascii=False)


