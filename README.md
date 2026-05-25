# 汇博机器人视觉项目集

计算机视觉 + 工业机器人控制项目集合，涵盖 YOLO 模型训练、仪表读数识别、云台相机控制和多机器人协同搬运。

## 项目结构

```
518/
├── lib/ultralytics/          # 共享的 YOLOv8 推理/训练库（仅一份）
├── tools/
│   ├── yolo_train_test/      # YOLO 训练+测试+仪表读数工具
│   └── ptz_camera/           # 海康威视云台相机采集控制工具
└── robot_competition/        # 第三届人工智能竞赛 - 服务机器人巡检
```

---

## 1. tools/yolo_train_test — YOLO 训练与仪表读数

基于 YOLOv8 + PySide6 的桌面工具，支持目标检测模型训练、测试，以及指针式仪表自动读数。

### 功能

| 模块 | 文件 | 功能 |
|------|------|------|
| 训练 | `train.py` | 图形化 YOLO 训练（参数设置、日志显示、实时图表） |
| 测试 | `test.py` | 模型批量测试与指标评估 |
| 仪表读数 | `meter_reading.py` | 指针式电流表/电压表读数 + LED 数码管 OCR 识别 |
| 检测识别 | `recognition.py` | 仪表类型检测 + 关键点定位 + 角度映射读数 |
| 训练引擎 | `train_engine.py` | YOLO 训练入口（带 epoch 回调） |
| 配置 | `config.py` | 训练参数配置类 |

### 仪表读数工作流程

1. **目标检测** → 识别 mA 电流表 / V 电压表 / LED 数码管
2. **关键点检测** → 定位表盘中心、指针、量程起点/终点
3. **角度映射** → 将指针角度线性映射为读数
4. **LED 识别** → PaddleOCR 识别 LED 数码管数值
5. **逻辑关联** → 电流表 + LED 电压表 / 电压表 + LED 电流表 配对推算

### 使用

```bash
cd tools/yolo_train_test
pip install -r ../../requirements.txt
python train.py       # 启动训练界面
python test.py --folder testA  # 启动批量测试
```

---

## 2. tools/ptz_camera — 云台相机控制

海康威视 PTZ 云台相机桌面控制工具。

### 功能

- **ONVIF 协议连接** → 自动发现并初始化相机
- **RTSP 实时预览** → 实时显示视频流
- **云台控制** → 绝对/相对角度移动（Pan/Tilt）
- **图像采集** → 支持多种分辨率（原始/1080p/640×480/320×240）
- **自动保存** → 时间戳命名的 PNG 图片

### 文件

| 文件 | 说明 |
|------|------|
| `hk_ptz_camera.py` | 海康云台相机底层接口（ONVIF + RTSP） |
| `camera_client.py` | QThread 后台相机线程 |
| `云台图像采集测试助手.py` | PySide6 桌面主界面 |
| `config.yaml` | 相机 IP/用户名/密码配置 |
| `wsdl/` | ONVIF WSDL 协议文件 |

### 使用

```bash
cd tools/ptz_camera
# 编辑 config.yaml 设置相机参数
python 云台图像采集测试助手.py
```

---

## 3. robot_competition — 服务机器人巡检

第三届人工智能竞赛项目，多机协作完成新能源电池搬运任务。

### 机器人组成

| 机器人 | 角色 | 通信 |
|--------|------|------|
| 阿克曼车 (SongLingCar) | 导航运输 | HTTP API |
| AGV 小车 (HbCar) | 接驳搬运 | HTTP API |
| 桥吊 (Carry) | 三轴天车抓取 | TCP 串口 |
| 机械臂 (FrRobot) | 6轴协作臂 | TCP 协议 |

### 工作流程

```
阿克曼车 → 吊桥下
    ↓
桥吊视觉定位 → ArUco 码识别 → 电磁铁抓取 → 放置到 AGV
    ↓
阿克曼车 → 存储区
    ↓
AGV 对接 → 机械臂取电池 → 视觉定位 → 放置到安全处置柜
```

### 关键文件

| 文件 | 说明 |
|------|------|
| `main.py` | 主流程控制（状态机驱动） |
| `config.py` | 所有机器人的坐标/相机参数/点位配置 |
| `car.py` | 阿克曼车 + AGV 小车控制接口 |
| `carry.py` | 桥吊控制 |
| `fr_robot.py` | 法奥机械臂控制 |
| `utils.py` | 坐标变换、ArUco 码定位、图像处理 |
| `roslib/` | ROS 基础通信库 + 云台相机 + YOLO 检测 |
| `巡检任务.py` | 简单的云台相机 + 导航测试脚本 |

---

## 依赖

```
PySide6
ultralytics（已内置在 lib/ultralytics/）
opencv-python
numpy
paddleocr
PyYAML
torch
```

## 注意事项

- 相机配置在 `tools/ptz_camera/config.yaml` 中修改 IP/用户名/密码
- 机器人坐标和相机内参在 `robot_competition/config.py` 中配置
- `lib/ultralytics/` 是共享的 YOLO 库，所有模块共用一份
- 模型文件（.pt）位于各工具的 `model/` 目录下
