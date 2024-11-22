# Load the TensorBoard notebook extension
# %load_ext tensorboard
import tensorflow as tf
import numpy as np  
from matplotlib import pyplot as plt

import datetime
import os

# 載入 MNIST 資料庫的訓練資料，並自動分為『訓練組』及『測試組』
mnist = tf.keras.datasets.mnist

(x_train, y_train),(x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0



def create_model():
  return tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28), name='layers_flatten'),
    tf.keras.layers.Dense(512, activation='relu', name='layers_dense'),
    tf.keras.layers.Dropout(0.2, name='layers_dropout'),
    tf.keras.layers.Dense(10, activation='softmax', name='layers_dense_2')
  ])

model = create_model()
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

log_dir = "logs\\fit\\" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)

train_history=model.fit(x=x_train, y=y_train, epochs=5,  validation_data=(x_test, y_test),  callbacks=[tensorboard_callback])

plt.plot(train_history.history['accuracy'])  
plt.plot(train_history.history['val_accuracy'])  
plt.title('Train History')  
plt.ylabel('acc')  
plt.xlabel('Epoch')  
plt.legend(['acc', 'val_acc'], loc='upper left')  
plt.show() 