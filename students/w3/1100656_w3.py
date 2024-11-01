import sys;   
import pandas as pd
import gspread

def read_xlsx_with_pandas(file_path):
    try:
        df = pd.read_excel(file_path)
        df.replace(r'^\s*$', float('Nan'), regex=True, inplace=True)
        df.dropna(how='all', inplace=True) 
        df.dropna(axis=1, how='all', inplace=True)        
        return df
    except Exception as e:
        print(f"error: {e}")
        return None
df = read_xlsx_with_pandas('C:/Users/User/Desktop/python實務/2024_python/teacher/w3/grade_list.xlsx')
df = pd.DataFrame(df)
grade_list = df.values.tolist()

def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1): 
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
arr=[]
arr_sort=[]

for i in range(1,len(grade_list)):
    for j in range(1,4):
        for k in range(0,100):
            if grade_list[i][j]==str(k):
                grade_list=k
            if grade_list[i][j] is float('nan'):
                grade_list[i][j]=int(0)
                


for i in range(1,len(grade_list)):
  grade_list[i][5]=grade_list[i][4]+grade_list[i][3]+grade_list[i][2]+grade_list[i][1]
  grade_list[i][6]=float(float(grade_list[i][5])/4)
  arr.append(grade_list[i][6])

arr_sort=arr
bubbleSort(arr_sort)
for i in range(len(grade_list)-1):
  for j in range(len(grade_list)):
    if grade_list[j][6] == arr_sort[i]:
      grade_list[j][7]=len(grade_list)-i-1


print('------------------Excel Grade List------------------')

for i in range(len(grade_list)):
    print(grade_list[i][0], end='\t')
    for j in range(1, len(grade_list[i])):
        print(grade_list[i][j], end='\t')
    print()
    
def print_grade_list_data(grade_list_data):
        for i in range(len(grade_list_data)):
            print(grade_list_data[i][0], end='\t')
            for j in range(1, len(grade_list_data[i])):
                print(grade_list_data[i][j], end='\t')
            ## new line
            print()
            
gc = gspread.service_account(filename='C:/Users/User/Desktop/python實務/python_course_access_cred.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nqgiOHVyuIM1p4cBKUsi1HfmkaIhjIQdQYamGbkzOhE/edit#gid=0')

cell_range_pattern='c5:j12'
cell_range=sh.sheet1.get(cell_range_pattern)

  

grade_list_data=list(cell_range)




arr=[]
arr_sort=[]

for i in range(1,len(grade_list_data)):
    for j in range(1,4):
        for k in range(0,100):
            if grade_list[i][j]==str(k):
                grade_list=k
            if grade_list[i][j] is float('nan'):
                grade_list[i][j]=int(0)
                


for i in range(1,len(grade_list_data)):
  grade_list_data[i][5]=grade_list[i][4]+grade_list[i][3]+grade_list[i][2]+grade_list[i][1]
  grade_list_data[i][6]=float(float(grade_list[i][5])/4)
  arr.append(grade_list[i][6])

arr_sort=arr
bubbleSort(arr_sort)
for i in range(len(grade_list_data)-1):
  for j in range(len(grade_list)):
    if grade_list_data[j][6] == arr_sort[i]:
      grade_list_data[j][7]=len(grade_list)-i-1

print('------------------Google Sheets Grade List------------------')
print_grade_list_data(grade_list_data)