import sys
sys.path.append('./Detection')
from utils import genJson,showmaV
from config import Config
from main import trainyolo
from ultralytics import YOLO




def test_image(image_path, model_path):
    model = YOLO(model_path)
    results = model(image_path)
    # Process results list
    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        obb = result.obb  # Oriented boxes object for OBB outputs
        names = result.names
        result.save(filename="./images/result.jpg")  # save to disk
    # 初始化空列表存储结果
    detections = []
    for box in result.boxes:
        # print(f"Class: {box.cls}, Confidence: {box.conf}, Box Coordinates: {box.xyxy}")
        class_id = int(box.cls)  # 类别ID（通常是整数）
        confidence = float(box.conf)  # 置信度（通常是浮点数）
        detections.append({
            "class_id": class_id,
            "confidence": confidence
        })
    pre_image = './images/result.jpg'
    # names:{0:'fish',1:'xzc'}
    detection_text = ""
    for i, detection in enumerate(detections):
        if i >= 6:  # 显示前6个物体
            break
        detection_text += f"类别名称: {names[detection['class_id']]}, 置信度: {detection['confidence']}\n"

    # 更新标签的文本，将结果显示在 self.additional_label 中
    print(detection_text)
    #self.result_label.setText(detection_text)
    # 检测仪表盘
    ybptext = showmaV(image_path)
    #print()
    #self.maV_label.setText(ybptext)
    return pre_image, detections


if __name__ == '__main__':
    image_path = r'C:\Users\WTKS\Desktop\data\第二版补充版\images\2024-10-14-11-43-01-589810.png'
    model_path = './model/detectionMVP.pt'
    # model_path = 'model/detectionMVP.pt'
    pre_image, detections = test_image(image_path, model_path)
    ybptext = showmaV(image_path)