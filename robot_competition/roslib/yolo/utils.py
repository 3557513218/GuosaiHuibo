import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../lib'))
import cv2
import numpy as np
from ultralytics import YOLO
# from paddleocr import PaddleOCR
import yaml
def get_val(img,data,Ctype):
    x1, y1, x2, y2 = data["box"]

    if len(data["keypoints"]) >= 4:
        #可视化
        center = data["keypoints"][0]  # 假设第一个关键点是表盘中心
        pointer = data["keypoints"][1]  # 假设第二个关键点是指针末端
        qidian = data["keypoints"][2]  # 起点
        zhongdian = data["keypoints"][3]  # 终点
        for i in range(len(data["keypoints"])):
            cv2.circle(img, data["keypoints"][i], 5, (0, 0, 255), -1)
        # 绘制从中心到指针的直线
        cv2.line(img, center, pointer, (0, 255, 0), 2)
        cv2.line(img, center, qidian, (255, 0, 0), 2)
        cv2.line(img, center, zhongdian, (0, 0, 255), 2)
        #cv2.putText(img, Ctype, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        #------------------
        # 计算量程起点和终点的角度
        qidian_angle = calculate_angle(center, qidian)
        zhongdian_angle = calculate_angle(center, zhongdian)
        # print(f"起点角度: {qidian_angle:.2f} degrees, 终点角度: {zhongdian_angle:.2f} degrees")

        # 计算指针的偏转角度
        pointer_angle = calculate_angle(center, pointer)
        # print(f"指针角度: {pointer_angle:.2f} degrees")

        # 计算偏转角度（从起点到指针）
        deflection_angle = pointer_angle - qidian_angle
        if deflection_angle < 0:
            deflection_angle += 360  # 确保偏转角度为正值

        # print(f"偏转角度: {deflection_angle:.2f} degrees")

        # 根据角度读数
        if Ctype == 'mA':
            min_value = 0  # 根据实际需求设置最小读数
            max_value = 20  # 根据实际需求设置最大读数
        elif Ctype == 'V':
            min_value = 0  # 根据实际需求设置最小读数
            max_value = 10  # 根据实际需求设置最大读数
        reading = map_angle_to_value(pointer_angle, min_value, max_value, qidian_angle, zhongdian_angle)
        cv2.imwrite('keypoints.jpg', img)
        return reading

def genJson(path,class_name):
    # 创建要写入 YAML 文件的数据结构，使用 OrderedDict
    # 创建要写入 YAML 文件的数据结构，使用列表保持顺序
    data = {
        "path": path,
        "train": "images/train",  # 示例数据
        "val": "images/val",  # 示例数据
        "test": "images/test",  # 示例数据
        "names": {i: name for i, name in enumerate(class_name)}  # 转换为所需格式
    }

    # 使用一个顺序列表来确保输出顺序
    ordered_data = {
        'path': data['path'],
        'train': data['train'],
        'val': data['val'],
        'test': data['test'],
        'names': data['names']
    }

    # 将数据写入 YAML 文件
    with open('dataset_config.yaml', 'w', encoding='utf-8') as yaml_file:
        yaml.dump(ordered_data, yaml_file, allow_unicode=True, sort_keys=False)

    print("YAML 文件已成功创建。")

    return True


import re
# 添加路径
def get_val_A(img):
    print("检测到目标mA，进入函数 a()")
    model = YOLO('./model/PoseMVP.pt')  # 替换为你自己的关键点检测模型路径
    # 加载图片
    output_data = []
    # 进行预测
    results = model(img)
    for result in results:
        keypoints = result.keypoints  # 关键点的坐标
        boxes = result.boxes  # 边界框

        # 迭代每个检测到的对象
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # 转换为整数
            box_info = {"box": (x1, y1, x2, y2), "keypoints": [], "label": "Ameter"}

            # 如果检测到关键点，绘制第五、六、七、八个关键点
            if keypoints is not None:
                keypoints_data = keypoints.xy  # 提取关键点的 xy 坐标
                kp = keypoints_data[i]  # 获取与当前框对应的关键点
                if len(kp) >= 8:
                    for j, keypoint in enumerate(kp):
                        if j >= 4:
                            x, y = int(keypoint[0]), int(keypoint[1])
                            cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
                            box_info["keypoints"].append((x, y))

                output_data.append(box_info)

            for data in output_data:
                x1, y1, x2, y2 = data["box"]
                label = data["label"]
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                if len(data["keypoints"]) >= 4:
                    center = data["keypoints"][0]  # 假设第一个关键点是表盘中心
                    pointer = data["keypoints"][1]  # 假设第二个关键点是指针末端
                    qidian = data["keypoints"][2]  # 起点
                    zhongdian = data["keypoints"][3]  # 终点

                    # 绘制从中心到指针的直线
                    cv2.line(img, center, pointer, (0, 255, 0), 2)
                    cv2.line(img, center, qidian, (255, 0, 0), 2)
                    cv2.line(img, center, zhongdian, (0, 0, 255), 2)

                    # 计算量程起点和终点的角度
                    qidian_angle = calculate_angle(center, qidian)
                    zhongdian_angle = calculate_angle(center, zhongdian)
                   # print(f"起点角度: {qidian_angle:.2f} degrees, 终点角度: {zhongdian_angle:.2f} degrees")

                    # 计算指针的偏转角度
                    pointer_angle = calculate_angle(center, pointer)
                    #print(f"指针角度: {pointer_angle:.2f} degrees")

                    # 计算偏转角度（从起点到指针）
                    deflection_angle = pointer_angle - qidian_angle
                    if deflection_angle < 0:
                        deflection_angle += 360  # 确保偏转角度为正值

                    #print(f"偏转角度: {deflection_angle:.2f} degrees")

                    # 根据角度读数
                    min_value = 0  # 根据实际需求设置最小读数
                    max_value = 20  # 根据实际需求设置最大读数
                    reading = map_angle_to_value(pointer_angle, min_value, max_value, qidian_angle, zhongdian_angle)
                    # if reading is not None:
                    #     print(f"测量值: {reading:.2f}")

    # 保存带有关键点的图像
    cv2.imwrite('./images/AMETER_with_keypoints.jpg', img)
    return reading




def get_val_B(img):
    print("检测到目标V，进入函数 b()")
    model = YOLO('../model/PoseMVP.pt')  # 替换为你自己的关键点检测模型路径
    # 加载图片
    #img_path = r'C:\Users\WTKS\Desktop\data\TEMP\关键点标注\images\2024-10-14-11-52-22-702466.png'
    #img = cv2.imread(img_path)
    output_data = []

    # 进行预测
    results = model(img)
    for result in results:
        keypoints = result.keypoints  # 关键点的坐标
        boxes = result.boxes  # 边界框

        # 迭代每个检测到的对象
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # 转换为整数
            box_info = {"box": (x1, y1, x2, y2), "keypoints": [], "label": "Voltmeter"}

            # 如果检测到关键点，绘制第五、六、七、八个关键点
            if keypoints is not None:
                keypoints_data = keypoints.xy  # 提取关键点的 xy 坐标
                kp = keypoints_data[i]  # 获取与当前框对应的关键点
                if len(kp) >= 8:
                    for j, keypoint in enumerate(kp):
                        if j >= 4:
                            x, y = int(keypoint[0]), int(keypoint[1])
                            cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
                            box_info["keypoints"].append((x, y))

                output_data.append(box_info)

            for data in output_data:
                x1, y1, x2, y2 = data["box"]
                label = data["label"]
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                if len(data["keypoints"]) >= 4:
                    center = data["keypoints"][0]  # 假设第一个关键点是表盘中心
                    pointer = data["keypoints"][1]  # 假设第二个关键点是指针末端
                    qidian = data["keypoints"][2]  # 起点
                    zhongdian = data["keypoints"][3]  # 终点

                    # 绘制从中心到指针的直线
                    cv2.line(img, center, pointer, (0, 255, 0), 2)
                    cv2.line(img, center, qidian, (255, 0, 0), 2)
                    cv2.line(img, center, zhongdian, (0, 0, 255), 2)

                    # 计算量程起点和终点的角度
                    qidian_angle = calculate_angle(center, qidian)
                    zhongdian_angle = calculate_angle(center, zhongdian)
                    #print(f"起点角度: {qidian_angle:.2f} degrees, 终点角度: {zhongdian_angle:.2f} degrees")

                    # 计算指针的偏转角度
                    pointer_angle = calculate_angle(center, pointer)
                    #print(f"指针角度: {pointer_angle:.2f} degrees")

                    # 计算偏转角度（从起点到指针）
                    deflection_angle = pointer_angle - qidian_angle
                    if deflection_angle < 0:
                        deflection_angle += 360  # 确保偏转角度为正值

                   # print(f"偏转角度: {deflection_angle:.2f} degrees")

                    # 根据角度读数
                    min_value = 0  # 根据实际需求设置最小读数
                    max_value = 10 # 根据实际需求设置最大读数
                    reading = map_angle_to_value(pointer_angle, min_value, max_value, qidian_angle, zhongdian_angle)
                    if reading is not None:
                        print(f"测量值: {reading:.2f}")

    # 保存带有关键点的图像
    cv2.imwrite('./images/Voltmeter_with_keypoints.jpg', img)
    print("reading:{}".format(reading))
    return reading



def get_LED(ledimg,I):
    # 初始化 OCR，指定语言为中文（可选参数 lang='ch'）
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # use_angle_cls 用于文字方向分类
    # 进行 OCR 识别
    results = ocr.ocr(ledimg)
    # 输出识别结果
    max_digits_count=0
    for line in results:
        for word_info in line:
            text = word_info[1][0]  # 识别的文本
            confidence = word_info[1][1]  # 置信度
            print(f"识别文本: {text}, 置信度: {confidence}")
            digits_count = len(re.findall(r'\d', text))  # 计算数字的数量

            if digits_count > max_digits_count:
                max_digits_count = digits_count
                best_result = text

        if best_result:
            print(f"最佳结果: {best_result}, 含数字数量: {max_digits_count}")
        else:
            print("未找到含数字的文本。")
            best_result = ''

    return best_result

# def get_LED_B(ledimg,V):
#     print('get led b')
#
#     return 0

#------------------------------------------------------------------------
def calculate_angle(p1, p2):
    """计算两点之间的角度"""
    delta_x = p2[0] - p1[0]
    delta_y = p2[1] - p1[1]
    angle = np.arctan2(delta_y, delta_x) * 180 / np.pi  # 转换为度
    return angle if angle >= 0 else angle + 360  # 确保角度在0-360度范围内

def map_angle_to_value(angle, min_angle, max_angle, qidian_angle, zhongdian_angle):
    """根据角度映射到读数"""
    # 将角度线性映射到读数
    if qidian_angle < zhongdian_angle:
        if angle < qidian_angle:
            angle += 360  # 处理角度环绕情况
        if angle < zhongdian_angle:
            return np.interp(angle, [qidian_angle, zhongdian_angle], [min_angle, max_angle])
    else:
        if angle > zhongdian_angle:
            angle -= 360  # 处理角度环绕情况
        if angle > qidian_angle:
            return np.interp(angle, [zhongdian_angle, qidian_angle], [max_angle, min_angle])
    return None  # 返回 None 如果角度不在量程范围内

def get_Lighttype(cls_list):
# RedOff=0  GreenOff=1 YellowOff=2 WhiteOff=3 mA=4 V=5 LED_V=6 LED_mA=7 RedOn=8 GreenOn=9 YellowOn=10 WhiteOn=11
    light_state = {
        'Red' : 0 if 0 in cls_list else 1,
        'Green' : 0 if 1 in cls_list else 1,
        'Yellow' : 0 if 2 in cls_list else 1,
        'White' : 0 if 3 in cls_list else 1,
    }
    return light_state
def is_all_digits_and_decimal(s):
    # 确保字符串非空，且只包含数字和最多一个小数点
    return bool(s) and s.count('.') <= 1 and all(c.isdigit() or c == '.' for c in s)

def showmaV(img_path):

    # 加载 YOLO 模型
    model = YOLO('./model/detectionMVP.pt')  # 确保模型路径正确

    # 读取图像
    img = cv2.imread(img_path)
    # 对图像进行推理
    results = model(img_path)
    LED_BOX = None
    cls_list=[]
    maVtext=''
    # 遍历检测结果
    for result in results:
        boxes = result.boxes
        names = result.names# 获取检测框的相关信息
        for box in boxes:
            cls_id = int(box.cls)  # 获取类别ID
            confidence = box.conf  # 获取置信度
            #print(f"检测到的类别ID: {cls_id}, 置信度: {confidence}")

            # 检查是否存在目标类别（例如，类别ID为 0）
            #RedOff=0  GreenOff=1 YellowOff=2 WhiteOff=3 mA=4 V=5 LED_V=6 LED_mA=7 RedOn=8 GreenOn=9 YellowOn=10 WhiteOn=11
            #
            # if cls_id == 6:
            #     LED_BOX = box
            # if cls_id == 7:
            #     LED_BOX = box
            if  names[cls_id]== 'LED_V':
                LED_BOX = box
            if names[cls_id]== 'LED_mA':
                LED_BOX = box
            cls_list.append(names[cls_id])

        print(cls_list)
        light_state=get_Lighttype(cls_list)
        #---------------------------------判断类型---------------------------------------------------
            #类型A:指针式电流表&LED电压表
        if 'mA' in cls_list or 'LED_V' in cls_list:
            Current = get_val_A(img)
            Current = get_val_A(img)
            Current = round(Current,2)
            x1, y1, x2, y2 = map(int, LED_BOX.xyxy[0])
            LED_img = img[y1:y2, x1:x2]

            LED_Voltage = get_LED(LED_img,Current)
            #如果LED检测的结果中还有字符或者为空，则根据电阻计算
            print('LED_Voltage:',LED_Voltage)
            if not is_all_digits_and_decimal(LED_Voltage):
                LED_Voltage = Current * 0.526
                LED_Voltage = f"{round(LED_Voltage, 3):.3f}"
            if '.' not in LED_Voltage:
                LED_Voltage =LED_Voltage[0] + '.' + LED_Voltage[1:]

            print('电流：{} mA, 电压:{} V'.format(Current,LED_Voltage))
            maVtext = '电流：{} mA, 电压:{} V'.format(Current, LED_Voltage)
        #-------------------------------------------------------------------------------------------
            #类型B:指针式电压表&LED电流表
        elif 'V' in cls_list or 'LED_mA' in cls_list:
            Voltage = get_val_B(img)
            Voltage = round(Voltage,2)
            x1, y1, x2, y2 = map(int, LED_BOX.xyxy[0])
            LED_img = img[y1:y2, x1:x2]

            LED_Current = get_LED(LED_img,Voltage)
            # 如果LED检测的结果中还有字符或者为空，则根据电阻计算
            if not is_all_digits_and_decimal(LED_Current):
                LED_Current = Voltage / 0.48
                LED_Current = f"{round(LED_Current, 3):.3f}"
            if '.' not in LED_Current:
                if Voltage < 4.8:
                    LED_Current = LED_Current[0] + '.' + LED_Current[1]
                elif len(LED_Current) == 3:
                    LED_Current = Voltage / 0.48
                    LED_Current = f"{round(LED_Current, 3):.3f}"
                else:
                    LED_Current = LED_Current[:2] + '.' + LED_Current[2:]

            print('电流：{} mA, 电压:{} V'.format(LED_Current, Voltage))
            maVtext= '电流：{} mA, 电压:{} V'.format(LED_Current, Voltage)
        # 保存结果图像
        #result.save(filename="result.jpg")  # 保存检测结果图像
    return maVtext
