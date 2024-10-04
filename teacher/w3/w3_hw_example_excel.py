# pip install openpyxl
# show read excel 

import sys;   
import datetime
import openpyxl



def print_grade_list_data(grade_list_data):
        for i in range(len(grade_list_data)):
            print(grade_list_data[i][0], end='\t')
            for j in range(1, len(grade_list_data[i])):
                print(grade_list_data[i][j], end='\t')
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
grade_list_data = []

for row in cell_range:
    row_list = []
    for cell in row:        
        row_list.append(cell.value)
    grade_list_data.append(row_list)



print('\nRead Excel file and print the data:\n')
print_grade_list_data(grade_list_data)


# Close the workbook (important to release resources)
workbook.close()
