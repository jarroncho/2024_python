# 導入函式庫
import tensorflow as tf
import numpy as np  
from matplotlib import pyplot as plt


# 載入 MNIST 資料庫的訓練資料，並自動分為『訓練組』及『測試組』
# X is image data , Y is label
# 載入 MNIST 資料庫的訓練資料，並自動分為『訓練組』及『測試組』
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()


# 將 training 的 input 資料轉為1維
x_train_2D = x_train.reshape(60000, 28*28).astype('float32')
x_test_2D = x_test.reshape(10000, 28*28).astype('float32')

# normalize inputs from 0-255 to 0-1
x_train_norm = x_train_2D/255.0
x_test_norm = x_test_2D/255.0

# 將 training 的 label 進行 one-hot encoding，例如數字 7 經過 One-hot encoding 轉換後是 0000001000，即第7個值為 1
y_train_one_hot = tf.keras.utils.to_categorical(y_train) 
y_test_one_hot = tf.keras.utils.to_categorical(y_test) 


#plt.figure(figsize=(width, height)) # 設定顯示圖形的大小
plt.figure(figsize=(20, 10))
# 顯示前25 張圖
for index in range(25):
  plt.subplot(5, 5, index + 1)
  print("y_TrainOneHot[%d]="%index,y_test_one_hot[index])
  plt.title("i=%d"%index+"\nlabel=%d"%y_test[index])
  plt.imshow(x_test[index], cmap=plt.cm.gray)

# pad with 0.5 inch bewteen subplots  
plt.tight_layout(pad=0.5)  
plt.show() 


