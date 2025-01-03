
# 導入函式庫
import numpy as np  
import tensorflow as tf
from matplotlib import pyplot as plt
import os
import datetime


# mse for loss, sgd for optimizer
use_relu = True
epoch_num = 15
if use_relu:
    activation_function = 'relu'
else:
    activation_function = 'sigmoid'


# sparse_categorical_crossentropy for loss, adam for optimizer

loss_function = 'sparse_categorical_crossentropy'
optimizer_function = 'SGD'
    

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


#tfboard lordir
log_dir = "logs\\fit\\" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir, histogram_freq=1)


# 建立5層layer,2、3、4Dropout模型
def create_model():
  return tf.keras.models.Sequential([
    tf.keras.layers.Dense(units=768, input_dim=784,  kernel_initializer='normal',activation=activation_function, name='layers_dense'),
    tf.keras.layers.Dense(units=64, kernel_initializer='normal',activation=activation_function, name='layers_dense_2'),
    tf.keras.layers.Dropout(0.2, name='layers_dropout'),
    tf.keras.layers.Dense(units=64, kernel_initializer='normal',activation=activation_function, name='layers_dense_3'),
    tf.keras.layers.Dropout(0.2, name='layers_dropout_2'),
    tf.keras.layers.Dense(units=64, kernel_initializer='normal',activation=activation_function, name='layers_dense_4'),
    tf.keras.layers.Dropout(0.2, name='layers_dropout_3'),
    tf.keras.layers.Dense(units=10,  kernel_initializer='normal',activation='softmax', name='layers_dense_5'),
  ])

# 建立3層layer模型
def create_model2():
  return tf.keras.models.Sequential([
    tf.keras.layers.Dense(units=768, input_dim=784,  kernel_initializer='normal',activation=activation_function, name='layers_dense'),
    tf.keras.layers.Dense(units=512, kernel_initializer='normal',activation=activation_function, name='layers_dense_2'),
    tf.keras.layers.Dense(units=10,  kernel_initializer='normal',activation='softmax', name='layers_dense_3'),
  ])

# training 的 input 資料轉為1維  28*28=784 

model = create_model()

# 編譯: 選擇損失函數、優化方法及成效衡量方式
# 進行訓練, 訓練過程會存在 train_history 變數中
 
#model1編譯結果  
model.compile(loss='sparse_categorical_crossentropy', optimizer='SGD', metrics=['accuracy']) 
train_history=model.fit(x=x_train_norm, y=y_train, epochs=epoch_num,  validation_data=(x_test_norm, y_test),batch_size=100, 
                        verbose=2,callbacks=[tensorboard_callback])
# 顯示訓練成果(分數)
scores = model.evaluate(x_test_norm, y_test)  
print("\t[Info] Accuracy of testing data = {:2.1f}%".format(scores[1]*100.0)) 
# 預測(prediction)
X = x_test_norm[0:1,:]
predictions = model.predict(X)
print(predictions)
    
    

# 顯示訓練成果(分數)
#scores = model.evaluate(x_test_2D, y_test_one_hot)  
#scores = model.evaluate(x_test_norm, y_test_one_hot)  
# used for loss function is sparse_categorical_crossentropy
#scores = model.evaluate(x_test_norm, y_test)  

#print("\t[Info] Accuracy of testing data = {:2.1f}%".format(scores[1]*100.0))  

# 預測(prediction)
#X = x_test_2D[0:1,:]
#predictions = model.predict(X)
# get prediction result
#print(predictions)
#plt.imshow(x_test[0])
#plt.show() 

# Create side-by-side plots
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.imshow(x_test[0])

#train_history.history.keys()
plt.subplot(1, 2, 2)
plt.plot(train_history.history['accuracy'])  
plt.plot(train_history.history['val_accuracy'])  
plt.plot(train_history.history['loss'])  
plt.plot(train_history.history['val_loss'])  

plt.title('Train History')  
plt.ylabel('acc')  
plt.xlabel('Epoch')  
plt.legend(['acc', 'val_acc','loss', 'val_loss'], loc='upper left')  
plt.show() 

#model2編譯結果
log_dir = "logs\\fit\\" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir, histogram_freq=1)

model2 = create_model2()

model2.compile(loss='sparse_categorical_crossentropy', optimizer='SGD', metrics=['accuracy'])
train_history2=model2.fit(x=x_train_norm, y=y_train, epochs=epoch_num,  validation_data=(x_test_norm, y_test),batch_size=100, 
                          verbose=2,callbacks=[tensorboard_callback])
scores2 = model2.evaluate(x_test_norm, y_test)
print("\t[Info] Accuracy of testing data = {:2.1f}%".format(scores2[1]*100.0))
X2 = x_test_norm[0:1,:]
predictions2 = model2.predict(X2)
print(predictions2)


plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.imshow(x_test[0])

plt.subplot(1, 2, 2)
plt.plot(train_history2.history['accuracy'])
plt.plot(train_history2.history['val_accuracy'])
plt.plot(train_history2.history['loss'])
plt.plot(train_history2.history['val_loss'])

plt.title('Train History2')
plt.ylabel('acc')
plt.xlabel('Epoch')
plt.legend(['acc', 'val_acc','loss', 'val_loss'], loc='upper left')
plt.show()
