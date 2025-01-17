import shutil
import random 
import os
import time
from PIL import Image




import matplotlib.pyplot as plt
from cv2 import imread

def display_imgs_from_path(path='', rows = 1, cols = 1):
  """
  Displays random rows * cols images from a directory
    
  Arguments:
      path: a string representing the path for the directory with the images to displat 
      rows: an integer representing the number of rows in the plots figure
      cols: an integer representing the number of columns in the plots figure

  Returns:
      None

  """
  fig = plt.figure(figsize=(8, 5))

# Get list of image files in the specified path
  img_files = os.listdir(path)

# Ensure that we do not try to sample more images than available
  num_samples = min(rows * cols, len(img_files))  # The number to sample

# Randomly sample images
  sampled_images = random.sample(img_files, num_samples)

  #print(sampled_images)

  for i , img_name in enumerate(sampled_images):
    
    img = imread(path + '/' + img_name)
    fig.add_subplot(rows, cols, i+1)
    plt.imshow(img)
    plt.axis('off')
    plt.title(img_name[:8])
    
# start
print("Cat samples : {}".format(len(os.listdir("PetImages/Dog"))))
print("Dog samples : {}".format(len(os.listdir("PetImages/Cat"))))




original_dataset_path = 'PetImages'
clean_dataset_path = 'working/Dataset'
test_path = 'working/test'
train_path = 'working/train'
validation_path = 'working/validation'



display_imgs_from_path(path=test_path +'/Cat', rows = 1, cols = 5)
display_imgs_from_path(path=train_path +'/Cat', rows = 1, cols = 5)
display_imgs_from_path(path=validation_path +'/Cat', rows = 1, cols = 5)

display_imgs_from_path(path=test_path +'/Dog', rows = 1, cols = 5)
display_imgs_from_path(path=train_path +'/Dog', rows = 1, cols = 5)
display_imgs_from_path(path=validation_path +'/Dog', rows = 1, cols = 5)

plt.show() 
