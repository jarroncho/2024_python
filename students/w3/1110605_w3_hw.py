#pip install gspread oauth2client
import sys;   
import datetime
import gspread
import openpyxl
from abc import ABC, abstractmethod

#執行前先需確認是否在資料夾內

#基礎的class
class Base_Grade_list(ABC):
    @abstractmethod
    def area(self):
        pass    
        
    def print_grade_list_data(self):
        for i in range(len(self.grade_list_data)):
            print(self.grade_list_data[i][0], end='\t')
            for j in range(1, len(self.grade_list_data[i])):
                print(self.grade_list_data[i][j], end='\t')
            print()

    def ranking(self):
        
        for i in range(1,len(self.grade_list_data)):
            self.grade_list_data[i][5] = self.grade_list_data[i][1] + self.grade_list_data[i][2] + self.grade_list_data[i][3] + self.grade_list_data[i][4]
            self.grade_list_data[i][6] = self.grade_list_data[i][5] / 4
      
        grade_list_sort = sorted(self.grade_list_data[1:len(self.grade_list_data)], key=lambda x: x[5], reverse=True)
        

        for i in range(len(grade_list_sort)):
            grade_list_sort[i][7]=i+1
    
    def get_grade_list_data(self):
        return self.grade_list_data

#子class_1
class ExcelGradeList(Base_Grade_list):    
    
    def __init__(self, file):
        self.file = file
        
    def area(self):
        workbook = openpyxl.load_workbook(self.file)
        sheet_names = workbook.sheetnames
        sheet_name=sheet_names[0]
        sheet = workbook[sheet_name]
        cell_range_pattern='c5:j12'
        cell_range = sheet[cell_range_pattern]
        self.grade_list_data = []
        for row in cell_range:
            row_list = []
            for cell in row:
                row_list.append(cell.value)
            self.grade_list_data.append(row_list)

        return self.grade_list_data
    
print('\nRead Excel file and print the data:\n')
excel_grade_list=ExcelGradeList('.\\grade_list.xlsx')
excel_grade_list.area()

excel_grade_list.ranking()
excel_grade_list.print_grade_list_data()        

#子class_2
class GsGradeList(Base_Grade_list):    
    
           
        
    def area(self):
        gc = gspread.service_account(filename='python_course_access_cred.json')
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nqgiOHVyuIM1p4cBKUsi1HfmkaIhjIQdQYamGbkzOhE/edit#gid=0')

        cell_range_pattern='c5:j12'
        cell_range=sh.sheet1.get(cell_range_pattern)
        self.grade_list_data = []
    
        for row_index in range(len(cell_range)):
            row_list = []
            for col_index in range(len(cell_range[row_index])):
                if(row_index==0 or col_index==0):
                    row_list.append(cell_range[row_index][col_index])                   
                else: 
                    row_list.append(int(cell_range[row_index][col_index]))
            self.grade_list_data.append(row_list)

        return self.grade_list_data


print('\nRead Google sheet and print the data:\n')
gs_grade_list=GsGradeList()
gs_grade_list.area()
gs_grade_list.ranking()
gs_grade_list.print_grade_list_data()

