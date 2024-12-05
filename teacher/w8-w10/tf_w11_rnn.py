# 導入函式庫
import numpy as np  
import tensorflow as tf
from tensorflow.keras import layers
#fto_categorical  # 用來後續將 label 標籤轉為 one-hot-encoding 
from tensorflow.keras.utils import to_categorical
#from tensorflow.keras import losses

from matplotlib import pyplot as plt








# 載入 MNIST 資料庫的訓練資料，並自動分為『訓練組』及『測試組』
(X_train, Y_train), (X_test, Y_test) = tf.keras.datasets.mnist.load_data()
#x_train = X_train.reshape(60000, 1, 28, 28)/255
#x_test = X_test.reshape(10000, 1, 28, 28)/255
x_train, x_test = X_train / 255.0, X_test / 255.0

print("x_train shape",tf.shape(x_train))
#print(x_train)
y_train = to_categorical(Y_train)
y_test = to_categorical(Y_test)



# 建立簡單的線性執行的模型
model = tf.keras.models.Sequential()

#CNN
'''
model.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, input_shape=(1, 28, 28), activation='relu', padding='same'))
model.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2, padding="same"))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Flatten())

#fully connected to get all relevant data
model.add(tf.keras.layers.Dense(256, activation='relu'))
#one more dropout for convergence' sake :) 
model.add(tf.keras.layers.Dropout(0.5))
#output a softmax to squash the matrix into output probabilities
model.add(tf.keras.layers.Dense(10, activation='softmax'))
'''
#RNN
#layers.SimpleRNN(128),       
# layers.LSTM(128),  
# tf.keras.layers.GRU

#
#define networking and train 
batch_size = 64
# Each MNIST image batch is a tensor of shape (batch_size, 28, 28).
# Each input sequence will be of size (28, 28) (height is treated like time).
input_dim = 28
epochs=10
units = 64
output_size = 10  # labels are from 0 to 9
model.add(layers.SimpleRNN(units, input_shape=(None, input_dim)))
model.add(layers.BatchNormalization())
#model.add(layers.Dropout(0.2))
model.add(layers.Dense(output_size, activation='softmax'))
  

# Train
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), optimizer='adam', metrics=['accuracy'])
print(model.summary())


#tfboard_dir
#logdir = os.path.join("tfboard_dir", datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
#tensorboard_callback = tf.keras.callbacks.TensorBoard(logdir, histogram_freq=1)

#train_history = model.fit(x_train, y=y_TrainOneHot, validation_split=0.2, epochs=10, batch_size=64, verbose=1)  
#train_history=model.fit(x_train, y_train, epochs=3, batch_size=64, verbose=1)
train_history=model.fit(x_train, y_train, validation_split=0.2,epochs=epochs, batch_size=batch_size, verbose=1)
                        #callbacks=[tensorboard_callback])
# 顯示訓練成果(分數)
scores = model.evaluate(x_test, y_test)  
print()  
print("\t[Info] Accuracy of testing data = {:2.1f}%".format(scores[1]*100.0))  

#not done
'''
x0=x_test[0].reshape(1,28,28)
predictions_score = model.predict(x0)
print ("predictions_score",predictions_score)
print("x_test shape",tf.shape(x0))
print("x_test shape",tf.shape(x_test[0]))
plt.imshow(x_test[0],cmap=plt.cm.gray)
plt.show() 
'''
# Test
loss, accuracy = model.evaluate(x_test, y_test)
print('Test:')
print('Loss: %s\nAccuracy: %s' % (loss, accuracy))



plt.plot(train_history.history['accuracy'])  
plt.plot(train_history.history['val_accuracy'])  
plt.title('Train History')  
plt.ylabel('acc')  
plt.xlabel('Epoch')  
plt.legend(['accuracy', 'val_accuracy'], loc='upper left')  
plt.show() 
