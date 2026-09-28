# import torch
# from PIL import Image
# from transformers import AutoModelForCausalLM, AutoTokenizer
# import os
# import argparse
# import ipdb
#
# parser = argparse.ArgumentParser(prog='glm-4v for test datasets', description='Use glm-4v for identification of hidden dangers')
# parser.add_argument('--output_dir', type = str, default='./glm4_output')
# parser.add_argument('--image_dir', type = str, default='./image')
# parser.add_argument('--prompt_type', type = str, default='type_1', choices=['type_1', 'type_2', 'type_3', 'type_4'])
# args = parser.parse_args()
#
# # Function to get prompt
# def get_prompt(prompt_type):
#     if prompt_type == 'type_1':
#         prompt = "作为一个工地隐患检查人员，你的任务是根据施工工地图片，首先给出最明显的隐患类别，然后写出对应的隐患描述和整改意见。"
#     elif prompt_type == 'type_2':
#         prompt = "作为一个工地隐患检查人员，你的任务是根据施工工地图片，首先给出最明显的隐患类别，然后写出对应的隐患描述和整改意见。\n"\
#                  "其中，隐患类别的共11类包括：\n"\
#                  "1）高处作业未正确使用安全带 \n" \
#                  "2）基坑支护措施不到位 \n" \
#                  "3）灭火器未按规定要求放置 \n" \
#                  "4）配电箱未及时锁闭 \n" \
#                  "5）起重吊装设备钢丝绳磨损、断丝严重，搭接长度不足 \n" \
#                  "6）汽车吊、随车吊、泵车支腿未全部伸出、未垫枕木进行作业 \n" \
#                  "7）设备安全防护设施、装置缺失或失效 \n" \
#                  "8）未按规定穿戴反光安全服 \n" \
#                  "9）未按规定配置灭火器、消防设施等 \n" \
#                  "10）未按规定设置接地线或接地不良 \n" \
#                  "11）现场防护栏等安全防护设施缺失、破损或设置不规范"
#     elif prompt_type == 'type_3':
#         prompt = "作为一个工地隐患检查人员，你的任务是根据施工工地图片，首先给出最明显的隐患类别，然后写出对应的隐患描述和整改意见。具体格式如下：\n" \
#                  "隐患类别：\n" \
#                  "隐患描述：\n" \
#                  "整改意见："
#     else:
#         prompt = "作为一个工地隐患检查人员，你的任务是根据施工工地图片，首先给出最明显的隐患类别，然后写出对应的隐患描述和整改意见。具体格式如下：\n" \
#                  "隐患类别：\n" \
#                  "隐患描述：\n" \
#                  "整改意见：\n" \
#                  "其中，隐患类别的共11类包括：\n" \
#                  "1）高处作业未正确使用安全带 \n" \
#                  "2）基坑支护措施不到位 \n" \
#                  "3）灭火器未按规定要求放置 \n" \
#                  "4）配电箱未及时锁闭 \n" \
#                  "5）起重吊装设备钢丝绳磨损、断丝严重，搭接长度不足 \n" \
#                  "6）汽车吊、随车吊、泵车支腿未全部伸出、未垫枕木进行作业 \n" \
#                  "7）设备安全防护设施、装置缺失或失效 \n" \
#                  "8）未按规定穿戴反光安全服 \n" \
#                  "9）未按规定配置灭火器、消防设施等 \n" \
#                  "10）未按规定设置接地线或接地不良 \n" \
#                  "11）现场防护栏等安全防护设施缺失、破损或设置不规范"
#     return prompt
#
# os.environ['CUDA_VISIBLE_DEVICES'] = '0' # 设置 GPU 编号，如果单机单卡指定一个，单机多卡指定多个 GPU 编号
# MODEL_PATH = "THUDM/glm-4v-9b"
# device = "cuda" if torch.cuda.is_available() else "cpu"
# tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
#
#
# image_list = os.listdir(args.image_dir)
# output_dir = os.path.join(args.output_dir, args.prompt_type)
# os.makedirs(output_dir, exist_ok=True)
#
# for img in image_list:
#     image_path = os.path.join(args.image_dir, img)
#     image = Image.open(image_path).convert('RGB')
#     ipdb.set_trace()
#
#     # Getting the prompt
#     query = get_prompt(args.prompt_type)
#
#     inputs = tokenizer.apply_chat_template([{"role": "user", "image": image, "content": query}],
#                                            add_generation_prompt=True, tokenize=True, return_tensors="pt",
#                                            return_dict=True)  # chat mode
#
#     inputs = inputs.to(device)
#     model = AutoModelForCausalLM.from_pretrained(
#         MODEL_PATH,
#         torch_dtype=torch.bfloat16,
#         low_cpu_mem_usage=True,
#         trust_remote_code=True,
#         device_map="auto"
#     ).eval()
#
#     gen_kwargs = {"max_length": 2500, "do_sample": True, "top_k": 1}
#     with torch.no_grad():
#         outputs = model.generate(**inputs, **gen_kwargs)
#         outputs = outputs[:, inputs['input_ids'].shape[1]:]
#         print(tokenizer.decode(outputs[0]))
#         ipdb.set_trace()
#     result = ''
#     image_name = img.split('.')[0]
#     output_filename = os.path.join(output_dir, f'{image_name}.txt')
#     with open(output_filename, 'w', encoding='utf-8') as file:
#         file.write(result)


import base64
import random
import json
from zhipuai import ZhipuAI
import argparse
import ipdb
import os
import os.path as op

from tool.image_similarity import clip_img_score
from dotenv import load_dotenv

load_dotenv()

# 获取密钥
key = os.getenv("GLM_API_KEY")

parser = argparse.ArgumentParser(prog='glm-4v for test datasets', description='Use glm-4v for identification of hidden dangers')
parser.add_argument('--output_dir', type = str, default='./glm4_new_images_similarity_in_context_learning_output')
parser.add_argument('--image_dir', type = str, default='./dataset/隐患图片')
parser.add_argument('--prompt_type', type = str, default='type_4', choices=['type_1', 'type_2', 'type_3', 'type_4'])
parser.add_argument('--result_num', type = str, default='1', choices=['1,3,5'])
parser.add_argument('--shuffle', type = bool, default=False)
parser.add_argument('--data_check_path',type = str,default='data_check.json')
args = parser.parse_args()
image_cat_name = {
    '1':'未按规定穿戴反光安全服',
    '2':'高处作业未正确使用安全带',
    '3':'配电箱未及时锁闭',
    '4':'未按规定配置灭火器、消防设施等',
    '5':'现场防护栏等安全防护设施缺失、破损或设置不规范',
    '6':'设备安全防护设施、装置缺失或失效',
    '7':'起重吊装设备钢丝绳磨损、断丝严重，搭接长度不足',
    '8':'汽车吊、随车吊、泵车支腿未全部伸出、未垫枕木进行作业',
    '9':'基坑支护措施不到位',
    '10':'灭火器未按规定要求放置',
    '11':'未按规定设置接地线或接地不良',
    '12':'安全警示标志标识缺失或设置不规范',
    '13':'灭火器压力不足，灭火器、消防设施等未按规定进行检查、维护',
    '14':"不符合'三级配电两级漏电保护、一机一闸一漏一箱'要求",
    '15':':电缆外皮破损或敷设不规范',
}

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# def retrieve_exmaple(image_cat, image_name, data):
#     cat_name = image_cat_name[image_cat]
#     for id in data:
#         if data[id]["隐患类别"] == cat_name and data[id]["图片地址"].split('\\')[1].split('.')[0]!=image_name:
#             return data[id]
#     return data[str(random.randint(1, 325))]
def retrieve_exmaple(image_path, data):
    clip_img_scores = {}
    for id in data:
        clip_img_scores[id] = clip_img_score(data[id]['图片地址'], image_path)

    max_key = max(clip_img_scores, key=clip_img_scores.get)
    print(image_path)
    print(clip_img_scores)
    print(max_key)
    # ipdb.set_trace()
    return data[max_key]



def get_example(image_path, result_num, data):
    # image_cat = image_path.split('\\')[1].split('.')[0].split("-")[0]
    # image_name = image_path.split('\\')[1].split('.')[0]

    # example = retrieve_exmaple(image_cat, image_name, data)
    example = retrieve_exmaple(image_path, data)
    pic_path = example["图片地址"]
    type_text = example["隐患类别"]
    con_text = example["隐患描述"]
    if not op.isabs(pic_path):
        pic_path = op.join(args.image_dir, pic_path)
    base64_example = encode_image(pic_path)
    print(pic_path)

    example_text = "隐患类别的共15类包括:['未按规定穿戴反光安全服', '高处作业未正确使用安全带', '配电箱未及时锁闭', '未按规定配置灭火器、消防设施等', " \
                 "'现场防护栏等安全防护设施缺失、破损或设置不规范', '设备安全防护设施、装置缺失或失效', '起重吊装设备钢丝绳磨损、断丝严重，搭接长度不足', " \
                 "'汽车吊、随车吊、泵车支腿未全部伸出、未垫枕木进行作业', '基坑支护措施不到位', '灭火器未按规定要求放置', '未按规定设置接地线或接地不良', " \
                 "'安全警示标志标识缺失或设置不规范', '灭火器压力不足，灭火器、消防设施等未按规定进行检查、维护'," \
                 "'不符合'三级配电两级漏电保护、一机一闸一漏一箱'要求', '电缆外皮破损或敷设不规范']\n\n" \
                 f"作为一个工地隐患检查人员，你的任务是根据施工工地图片，写出{result_num}条最明显的隐患类别，然后写出对应的隐患描述。具体格式如下：\n" \
                 "隐患类别:<隐患类别>\n" \
                 "隐患描述:<隐患描述>\n"
    example_answer = f"隐患类别:{type_text}\n" \
                     f"隐患描述:{con_text}\n"

    return example_text, base64_example, example_answer



# Function to get prompt
def get_prompt(prompt_type, result_num):
    # Getting example
    # example = get_example(random.randint(1, 325))
    # pic_path = example["图片地址"]
    # type_text = example["隐患类别"]
    # con_text = example["隐患描述"]
    # base64_example = encode_image(pic_path)
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
    else:
        prompt = "隐患类别的共15类包括:['未按规定穿戴反光安全服', '高处作业未正确使用安全带', '配电箱未及时锁闭', '未按规定配置灭火器、消防设施等', " \
                 "'现场防护栏等安全防护设施缺失、破损或设置不规范', '设备安全防护设施、装置缺失或失效', '起重吊装设备钢丝绳磨损、断丝严重，搭接长度不足', " \
                 "'汽车吊、随车吊、泵车支腿未全部伸出、未垫枕木进行作业', '基坑支护措施不到位', '灭火器未按规定要求放置', '未按规定设置接地线或接地不良', " \
                 "'安全警示标志标识缺失或设置不规范', '灭火器压力不足，灭火器、消防设施等未按规定进行检查、维护'," \
                 "'不符合'三级配电两级漏电保护、一机一闸一漏一箱'要求', '电缆外皮破损或敷设不规范']\n\n" \
                 f"作为一个工地隐患检查人员，你的任务是根据施工工地图片，写出{result_num}条最明显的隐患类别，然后写出对应的隐患描述和整改意见。具体格式如下：\n" \
                 "隐患类别:<隐患类别>\n" \
                 "隐患描述:<隐患描述>\n" \
                 "整改意见:<整改意见>\n"\

    return prompt

def split_data(image_list, data):
    '''
    每个隐患类别，选择两个放进检索库
    '''
    val_image_list = []
    example_data_image_list = []
    example_data = {}

    cat_id_image_list = {}
    for img in image_list:
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
    if args.shuffle:
       random.shuffle(image_list)
       output_dir = os.path.join(args.output_dir, args.prompt_type, args.result_num+'_'+'shuffle')
    else:
       output_dir = os.path.join(args.output_dir, args.prompt_type, args.result_num)
    os.makedirs(output_dir, exist_ok=True)

    with open(args.data_check_path, "r", encoding='utf8') as file:
        data = json.load(file)

    example_data, val_image_list = split_data(image_list, data)

    for image in val_image_list:
        # image_dir = os.path.join(args.image_dir, image)
        # image_name = os.listdir(image_dir)[0]
        # image_path = os.path.join(args.image_dir, image, image_name)
        image_path = os.path.join(args.image_dir, image)
        result_name = image.split('.')[0]
        output_filename = os.path.join(output_dir, f'{result_name}.txt')

        #if result_name != '11-23':
            #continue

        # if op.exists(output_filename):
        #     continue

        # Getting the base64 string
        base64_image = encode_image(image_path)

        # Getting the prompt
        print(image_path)
        example_text, example_image, example_answer = get_example(image_path, args.result_num, example_data)
        prompt = get_prompt(args.prompt_type, args.result_num)
        print(example_answer)

        client = ZhipuAI(api_key=key)  # 填写您自己的APIKey

        response = client.chat.completions.create(
            model="glm-4v-plus",  # 填写需要调用的模型名称
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": example_text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": example_image
                            }
                        },
                        {
                            "type": "text",
                            "text": example_answer
                        },
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": base64_image
                            }
                        },
                    ]
                }
            ]
        )
        print(response.choices[0].message)

        result = response.choices[0].message.content

        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(result)
