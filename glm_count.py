import json
from collections import defaultdict
import re  # 用于忽略标点差异

# 读取JSON文件
with open('.\dataset\gpt_output.json', 'r', encoding='utf-8') as file:
    json_data1 = json.load(file)

with open('.\dataset\gpt_output_4.json', 'r', encoding='utf-8') as file:
    json_data2 = json.load(file)

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
category_dict[14] = [
    "不符合“三级配电两级漏电保护、一机一闸一漏一箱”要求",
    "不符合'三级配电两级漏电保护、一机一闸一漏一箱'要求"
]


def identify(actual_category,predicted_category):
    if isinstance(actual_category, list):  # 如果类别14有多个变体
        # 清理两侧空格并去除所有标点进行比较
        actual_category_clean = [re.sub(r'[^\w\s]', '', cat).strip() for cat in actual_category]
        predicted_clean = re.sub(r'[^\w\s]', '', predicted_category).strip()
        if predicted_clean in actual_category_clean:
            return True
        else:
            return False
    else:
        # 清理两侧空格并去除所有标点进行比较
        actual_category_clean = re.sub(r'[^\w\s]', '', actual_category).strip()
        predicted_clean = re.sub(r'[^\w\s]', '', predicted_category).strip()
        if actual_category_clean == predicted_clean:
            return True
        else:
            return False


def get_json(img_name):
    for entry in json_data2:
        img_name_2=entry["图片名称"]
        if img_name==img_name_2:
            return entry


if __name__ == '__main__':
    for entry in json_data1:
        # 获取图片名称中的数字（类别）
        img_name = entry["图片名称"]
        predicted_category = entry["隐患类别"]
        img_describe= entry["隐患描述"]

        # 提取图片名称前面的数字
        actual_category_num = int(img_name.split('-')[0])

        # 根据数字获取实际类别（注意类别14是一个列表）
        actual_category = category_dict[actual_category_num]

        entry2=get_json(img_name)
        img_name2 = entry2["图片名称"]
        predicted_category2 = entry2["隐患类别"]
        img_describe2 = entry2["隐患描述"]

        # 提取图片名称前面的数字
        actual_category_num2 = int(img_name2.split('-')[0])

        # 根据数字获取实际类别（注意类别14是一个列表）
        actual_category2 = category_dict[actual_category_num2]

        #if (identify(actual_category,predicted_category)==True):
            # if (identify(actual_category2,predicted_category2)!= True):
            #     print(img_name2)
            #     print("base隐患类别:"+predicted_category)
            #     print("base隐患描述:"+img_describe)
            #     print("思维链隐患类别:" + predicted_category2)
            #     print("思维链隐患描述:" + img_describe2)
        if (identify(actual_category,predicted_category)==True):
            if (identify(actual_category2,predicted_category2)!= True):
                print(img_name2)
                print("base隐患类别:"+predicted_category)
                print("base隐患描述:"+img_describe)
                print("思维链隐患类别:" + predicted_category2)
                print("思维链隐患描述:" + img_describe2)



