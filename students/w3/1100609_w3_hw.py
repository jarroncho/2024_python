import gspread
import openpyxl
from abc import ABC, abstractmethod

class Base_Gradelist(ABC):
    
    @abstractmethod
    def fetch_grade_list(self):
        pass
    
    def print_grade_list_data(self):
        for i in range(len(self.grade_list_sort)):
            print(self.grade_list_sort[i][0], end='\t')
            for j in range(1, len(self.grade_list_sort[i])):
                print(self.grade_list_sort[i][j], end='\t')
            print()
            
    def cal_sum(self):
        for i in range(1, len(self.grade_list_data)):
            for j in range(1,5):
                self.grade_list_data[i][5] = self.grade_list_data[i][5]+self.grade_list_data[i][j]
                
    def cal_average(self):
        for i in range(1, len(self.grade_list_data)):
            self.grade_list_data[i][6] = self.grade_list_data[i][5] / 4
            
    def cal_ranking(self):
        self.grade_list_sort = sorted(self.grade_list_data[1:], key=lambda x: x[5], reverse=True)
        for i in range(len(self.grade_list_sort)):
            self.grade_list_sort[i][7] = i + 1
            
    def get_gradelist_data(self):
        return self.grade_list_data
    
class Excel_gradelist(Base_Gradelist):
    
    def __init__(self, filename):
        self.filename = filename
        
    def fetch_grade_list(self):
        workbook = openpyxl.load_workbook(self.filename)
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
        #print(self.grade_list_data)
        return self.grade_list_data
print('-------------------Excel Grade List-------------------')
excel_grade_list = Excel_gradelist('.\\grade_list.xlsx')
excel_grade_list.fetch_grade_list()

excel_grade_list.cal_sum()
excel_grade_list.cal_average()
excel_grade_list.cal_ranking()
excel_grade_list.print_grade_list_data()
class GS_gradelist(Base_Gradelist):
    
    def fetch_gradelist(self):
        gc = gspread.service_account(filename='python_course_access_cred.json')
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nqgiOHVyuIM1p4cBKUsi1HfmkaIhjIQdQYamGbkzOhE/edit#gid=0')

        cell_range_pattern = 'c5:j12'
        cell_range = sh.sheet1.get(cell_range_pattern)
        self.grade_list_data = []
        
        for row_index in range(len(cell_range)):
            row_list = []
            for col_index in range(len(cell_range[row_index])):
                if row_index == 0 or col_index == 0:
                    row_list.append(cell_range[row_index][col_index])
                else:
                    row_list.append(int(cell_range[row_index][col_index]))
            self.grade_list_data.append(row_list)
        return self.grade_list_data
print('------------------GS Grade List-------------------')
gs_grade_list = GS_gradelist()
gs_grade_list.fetch_grade_list()
gs_grade_list.cal_sum()
gs_grade_list.cal_average()
gs_grade_list.cal_ranking()
gs_grade_list.print_grade_list_data()