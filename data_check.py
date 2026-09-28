import json
import os
import re
import argparse
parser = argparse.ArgumentParser(prog='database for check', description='Use example in database for check')
parser.add_argument('--image_dir', type = str, default='./dataset/隐患图片')
parser.add_argument('--output_dir', type = str, default='.')
args = parser.parse_args()


def get_imgpath(filename):
    img_dir = os.listdir(args.image_dir)
    for image in img_dir:
        if(image.split('.')[0].casefold()==filename.casefold()):
            img_path=os.path.join(args.image_dir, image)
            return img_path



def read_txt(inputpath):
    i=0
    json_text=""

    data_check = os.path.join(args.output_dir,"data_check.json")

    with open(inputpath, 'r', encoding='utf-8') as infile:
            for line in infile:
                i=i+1
                data_line = line.strip("\n") # 去除首尾换行符
                if(data_line.strip("	") == ""):
                    break
                #去除空白行
                title = str(re.findall("\d.*?(?=:)",data_line)).strip("[]'") # 提取序列
                context = data_line.strip(": 	"+title)
                type_num = str(re.findall("\d.*?(?=-)",title)).strip("[]'")
                img_path=get_imgpath(title)
                if(type_num == "1"):
                    type="未按规定穿戴反光安全服"
                elif(type_num == "2"):
                    type="高处作业未正确使用安全带"
                elif (type_num == "3"):
                    type="配电箱未及时锁闭"
                elif (type_num == "4"):
                    type="未按规定配置灭火器、消防设施等"
                elif (type_num == "5"):
                    type="现场防护栏等安全防护设施缺失、破损或设置不规范"
                elif (type_num == "6"):
                    type="设备安全防护设施、装置缺失或失效"
                elif (type_num == "7"):
                    type="起重吊装设备钢丝绳磨损、断丝严重，搭接长度不足"
                elif (type_num == "8"):
                    type="汽车吊、随车吊、泵车支腿未全部伸出、未垫枕木进行作业"
                elif (type_num == "9"):
                    type="基坑支护措施不到位"
                elif (type_num == "10"):
                    type="灭火器未按规定要求放置"
                elif (type_num== "11"):
                    type="未按规定设置接地线或接地不良"
                elif (type_num == "12"):
                    type="安全警示标志标识缺失或设置不规范"
                elif (type_num == "13"):
                    type="灭火器压力不足，灭火器、消防设施等未按规定进行检查、维护"
                elif (type_num == "14"):
                    type="不符合'三级配电两级漏电保护、一机一闸一漏一箱'要求"
                elif (type_num == "15"):
                    type="电缆外皮破损或敷设不规范"
                text ='"'+str(i)+'":{"图片地址":"'+img_path+'","隐患类别":"'+type+'","隐患描述":"'+context+'"}'
                #print(text)
                if(i==1):
                    json_text='{'+json_text+text;
                elif(i==325):
                    json_text=json_text+','+text+'}';
                else:
                    json_text=json_text+','+text
    t=json_text.replace('\\','\\\\')
    json_dict=json.loads(t)
    with open(data_check, 'w', encoding='utf-8') as file:
        json.dump(json_dict, file, allow_nan=False, sort_keys=True, indent=4,ensure_ascii=False)
    with open(data_check, "r", encoding='utf8') as file:
        data2 = json.load(file)  # 注意转换之后得类型 至于json.load文章后面会讲
        #print(data2["3"])


if __name__ == "__main__":
    input_path = './dataset/隐患描述文档.txt'
    read_txt(input_path)
