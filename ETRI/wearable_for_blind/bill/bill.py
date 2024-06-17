import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
import os
import random


def predict(src):
    labels = ['50000', '10000', '5000', '1000']
    
    # model load
    model_path = './bill/models/bill_tensorflow'
    model = tf.keras.models.load_model(model_path)
    
    # image load & preprocess
    src = np.fromstring(src, dtype = np.uint8)
    src = cv2.imdecode(src, cv2.IMREAD_COLOR)[None, ..., [2, 1, 0]]
    src = tf.image.resize(src, (480, 480))
    src = keras.applications.vgg16.preprocess_input(src)
    
    # prediction
    prob = model.predict(src)
    prob = prob[0].tolist()
    idx = prob.index(max(prob))
    result = labels[idx]
    
    return result


# if __name__ == "__main__":
#     predict(src)
