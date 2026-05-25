import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../lib'))
from ultralytics import YOLO
#1.数据配置 输入：选择文件夹的路径   输出：在yaml文件里进行更改   √
#2.参数配置 输入：epoch  lr  batchsize  输出：直接传参更改 √
#3.训练过程可视化 直接将result图片放在软件上 √
#4.模型测试  加载图片进行预测 结果图 bbox  class 展示√
#5.模型保存√
def on_train_epoch_end(trainer,app):
    """Custom logic for additional metrics logging at the end of each training epoch."""
    #additional_metric = compute_additional_metric(trainer)
    #app.showLog(trainer.epoch,trainer.loss,trainer.metrics)
    if trainer.epoch%5==0:
        app.showLog(f"Epoch: {trainer.epoch}:, Loss: {trainer.loss},\n Metrics: {trainer.metrics}\n")
def trainyolo(lr,epochs,batch,name,app):
    data = 'dataset_config.yaml'
    #model = YOLO('./model/detectionMVP.pt')
    model = YOLO('model/yolov8n.pt')
    model.add_callback("on_train_epoch_end", lambda trainer: on_train_epoch_end(trainer,app))
    try:
        results = model.train(data=data, epochs=epochs, batch=batch, name=name, lr0=lr, workers=0)
    except Exception as e:
        app.update_training_log(e)

if __name__ == '__main__':
    trainyolo()
