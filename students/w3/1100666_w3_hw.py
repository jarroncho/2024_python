# pip install openpyxl
# show read excel 

import sys;   
import datetime
import openpyxl



def print_grade_list_data(grade_list_data_data_data):
        for i in range(len(grade_list_data_data_data)):
            print(grade_list_data_data_data[i][0], end='\t')
            for j in range(1, len(grade_list_data_data_data[i])):
                print(grade_list_data_data_data[i][j], end='\t')
            ## new line
            print()

# Load the Excel workbook and select the sheet
workbook = openpyxl.load_workbook(r'teacher\w3\grade_list.xlsx')

# Get the sheet names
sheet_names = workbook.sheetnames
sheet_name=sheet_names[0]
# Print the sheet names
print("Sheet names:", sheet_names)
sheet = workbook[sheet_name]

# Specify the cell coordinates (row and column indices, 1-based index)
# Access the cell range
cell_range_pattern='c5:j12'
cell_range = sheet[cell_range_pattern]

# Initialize a 2D list to store cell values
grade_list_data_data = []

for row in cell_range:
    row_list = []
    for cell in row:        
        row_list.append(cell.value)
    grade_list_data_data.append(row_list)
arr=[]
for i in range(1,len(grade_list_data_data)):
  grade_list_data_data[i][5]=grade_list_data_data[i][4]+grade_list_data_data[i][3]+grade_list_data_data[i][2]+grade_list_data_data[i][1]
  grade_list_data_data[i][6]=float(int(grade_list_data_data[i][5])/4)
  arr.append(grade_list_data_data[i][6])

arr=sorted(arr,reverse=True)
print(arr)
for j in range(len(grade_list_data_data)):
   for i,num in enumerate(arr):
      if grade_list_data_data[j][6]==num:
         grade_list_data_data[j][7]=i+1

print('\nRead Excel file and print the data:\n')
print_grade_list_data(grade_list_data_data)


# Close the workbook (important to release resources)
workbook.close()
#------------------------------------------------------------
#pip install gspread oauth2client
import gspread


def print_grade_list_data(grade_list_data):
        for i in range(len(grade_list_data)):
            print(grade_list_data[i][0], end='\t')
            for j in range(1, len(grade_list_data[i])):
                print(grade_list_data[i][j], end='\t')
            ## new line
            print()

gc = gspread.service_account(filename='C:/Users/1108e/Documents/GitHub/2024_python/students/w3/python_course_access_cred.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nqgiOHVyuIM1p4cBKUsi1HfmkaIhjIQdQYamGbkzOhE/edit#gid=0')

cell_range_pattern='c5:j12'
cell_range=sh.sheet1.get(cell_range_pattern)

#print(cell_range)
#print(type(cell_range))    

grade_list_data=list(cell_range)
print(grade_list_data)
arr=[]
for i in range(1,len(grade_list_data)):
  grade_list_data[i][5]=int(grade_list_data[i][4])+int(grade_list_data[i][3])+int(grade_list_data[i][2])+int(grade_list_data[i][1])
  grade_list_data[i][6]=float(int(grade_list_data[i][5])/4)
  arr.append(grade_list_data[i][6])

arr=sorted(arr,reverse=True)
print(arr)
for j in range(len(grade_list_data_data)):
   for i,num in enumerate(arr):
      if grade_list_data[j][6]==num:
         grade_list_data[j][7]=i+1

print('\nRead Google sheet and print the data:\n')
print_grade_list_data(grade_list_data)
