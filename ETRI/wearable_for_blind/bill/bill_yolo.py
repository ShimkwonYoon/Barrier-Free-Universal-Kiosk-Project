import torch
import cv2
import numpy as np
import os


model_path = './bill/models/money_F.pt'
# model_path = './models/money_F.pt'
# img = './images/5000_b.jpg'

def detector(src):
    os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"
    device = torch.device("cuda")
    
    labels = []
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
    model.to(device)
    
    # print('Count of using GPUs:', torch.cuda.device_count()) 
    # print('Current cuda device:', torch.cuda.current_device()) 
    # print("GPU memory allocated: ", torch.cuda.memory_allocated())
    # print("GPU memory reserved: ", torch.cuda.memory_reserved())
    torch.cuda.empty_cache()
    
    
    src = np.fromstring(src, dtype = np.uint8)
    src = cv2.imdecode(src, cv2.IMREAD_COLOR)
    pred = model(src)
    for i in range(len(pred.xyxy[0].tolist())):
        labels.append(pred.pandas().xyxy[0]['name'].loc[i])
    
    return labels

# if __name__ == '__main__':
#     label = detector(img)
#     print(label)