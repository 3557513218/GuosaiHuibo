import sys, os
import cv2
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../lib'))
from ultralytics import YOLO
from meter_reading import get_val
from config import Config

def get_val_point(img, pos):
    print("检测到目标mA，进入函数 get_val_point()")
    model = YOLO('./model/PoseMVP.pt')  # 替换为你的关键点检测模型路径

    # 进行预测
    output={}
    results = model(img)

    boxes_with_keypoints = []  # 存储框及其对应的关键点

    for result in results:
        boxes = result.boxes  # 边界框
        keypoints = result.keypoints  # 关键点的坐标


        for i, box in enumerate(boxes):
            tempkp = []
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # 转换为整数
            # 转换为 numpy 数组
            if keypoints is not None:
                keypoints_data = keypoints.xy  # 提取关键点的 xy 坐标
                kp = keypoints_data[i]  # 获取与当前框对应的关键点
                if len(kp) >= 8:
                    for j, keypoint in enumerate(kp):
                        if j >= 4:
                            x, y = int(keypoint[0]), int(keypoint[1])
                            cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
                            tempkp.append((x, y))

            boxes_with_keypoints.append({
                'box': (x1, y1, x2, y2),
                'keypoints': tempkp
            })
    #如果只有一个框 默认为TOP：
    if len(boxes_with_keypoints)==1:
        boxes_with_keypoints[0]['relation']='top'
    # 处理两个框的位置关系
    elif len(boxes_with_keypoints)==2:
        for i in range(len(boxes_with_keypoints)):
            for j in range(i + 1, len(boxes_with_keypoints)):
                box1 = boxes_with_keypoints[i]['box']
                box2 = boxes_with_keypoints[j]['box']

                # 计算框的 ymin 和 ymax 的平均值
                box1_avg = (box1[1] + box1[3]) / 2  # box1 的中心 y
                box2_avg = (box2[1] + box2[3]) / 2  # box2 的中心 y

                # 判断框1和框2的位置关系
                if box1_avg < box2_avg:  # box1 的平均 y < box2 的平均 y
                    boxes_with_keypoints[i]['relation'] = 'top'
                    boxes_with_keypoints[j]['relation'] = 'bottom'
                else:
                    boxes_with_keypoints[i]['relation'] = 'bottom'
                    boxes_with_keypoints[j]['relation'] = 'top'

    # 根据 position 执行不同的函数  box keypoints relation
    count=0
    visual = cv2.imread(('images/result.jpg'))
    for item in boxes_with_keypoints:
        count+=1
        relation = item.get('relation')  #关键点检测中  框是top或者bottom
        if relation == 'top':
            func_to_call = pos.get('top')
            reading = get_val(visual,item,func_to_call)
            output.update({'num:{} class:{}'.format(count,func_to_call):reading})
        elif relation == 'bottom':
            func_to_call = pos.get('bottom')
            reading = get_val(visual,item, func_to_call)
            output.update({'num:{} class:{}'.format(count,func_to_call):reading})
    return output
#RedOff=0  GreenOff=1 YellowOff=2 WhiteOff=3 mA=4 V=5 LED_V=6 LED_mA=7 RedOn=8 GreenOn=9 YellowOn=10 WhiteOn=11
def Det(img,model_path):
    model = YOLO(model_path)
    results = model(img)
    record = {}
    boxes_with_names = []
    # Process results list
    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        names = result.names
        result.save(filename="./images/result.jpg")  # save to disk
        for i, box in enumerate(boxes):
            if int(box.cls) == 4 or int(box.cls) == 5:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # 转换为整数
                boxes_with_names.append({
                    'box': (x1, y1, x2, y2),
                    'class': names[int(box.cls)]
                })
    # 如果只有一个指针仪表盘，默认位置为top
    if len(boxes_with_names)==1:
        record.update({'top': boxes_with_names[0]['class']})
    elif len(boxes_with_names)==2:
        for i in range(len(boxes_with_names)):
            for j in range(i + 1, len(boxes_with_names)):
                box1 = boxes_with_names[i]['box']
                box2 = boxes_with_names[j]['box']

                # 计算框的 ymin 和 ymax 的平均值
                box1_avg = (box1[1] + box1[3]) / 2  # box1 的中心 y
                box2_avg = (box2[1] + box2[3]) / 2  # box2 的中心 y

                # 判断框1和框2的位置关系
                if box1_avg < box2_avg:  # box1 的平均 y < box2 的平均 y
                    record.update({'top': boxes_with_names[i]['class'],'bottom':boxes_with_names[j]['class']})
                else:
                    record.update({'top': boxes_with_names[j]['class'], 'bottom': boxes_with_names[i]['class']})
    return record

if __name__ == "__main__":
    #第一步 目标检测  识别一个或是两个仪表盘 并将其类型写入一个字典例如  一个表默认位置为top：{'top':'V'}  两个表分为top和bottom：{‘top’:'mA','bottom':'V'}
    img = cv2.imread('images/vma.jpg')
    position = Det(img,model_path='./model/DETMVP.pt')
    print(position)
    #第二步 关键点检测 检测出仪表盘的数量和位置关系 和第一步输出的字典记录的位置关系进行匹配确定类别，执行相应的读数函数
    out = get_val_point(img, position)
    print(out)


