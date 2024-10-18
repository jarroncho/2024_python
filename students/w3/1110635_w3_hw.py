import gspread
import openpyxl
from abc import ABC, abstractmethod

class GradeList(ABC):
    @abstractmethod
    def fetch_grade_list(self):
        pass
    
    def print_grade_list_data(self):
        for i in range(len(self.grade_list_sort)):
            print(self.grade_list_sort[i][0], end='\t')
            for j in range(1, len(self.grade_list_sort[i])):
                print(self.grade_list_sort[i][j], end='\t')
            print()
    
    def calculate_ranking(self):
        for i in range(1, len(self.grade_list_data)):
            self.grade_list_data[i][5] = self.grade_list_data[i][1] + self.grade_list_data[i][2] + self.grade_list_data[i][3] + self.grade_list_data[i][4]
            self.grade_list_data[i][6] = self.grade_list_data[i][5] / 4
        
        self.grade_list_sort = sorted(self.grade_list_data[1:], key=lambda x: x[5], reverse=True)
        for i in range(len(self.grade_list_sort)):
            self.grade_list_sort[i][7] = i + 1

    def get_grade_list_data(self):
        return self.grade_list_data

class ExcelGradeList(GradeList):
    def __init__(self, filename):
        self.filename = filename
    
    def fetch_grade_list(self):
        filename = 'C:\\Users\\kaits\\Desktop\\禮拜五程式設計\\2024_python-main\\teacher\\w3\\grade_list.xlsx'
        workbook = openpyxl.load_workbook(filename)
        sheet = workbook[workbook.sheetnames[0]]
        cell_range = sheet['C5:J12']
        self.grade_list_data = [[cell.value for cell in row] for row in cell_range]
        return self.grade_list_data

print('-------------------ExcelGradeList-------------------')
excel_grade_list = ExcelGradeList('.\\grade_list.xlsx')
excel_grade_list.fetch_grade_list()
excel_grade_list.calculate_ranking()
excel_grade_list.print_grade_list_data()



