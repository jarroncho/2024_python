import sys
import datetime
import openpyxl
import gspread

def print_grade_list_data(grade_list_data):
    for i in range(len(grade_list_data)):
        print(grade_list_data[i][0], end='\t')
        for j in range(1, len(grade_list_data[i])):
            print(grade_list_data[i][j], end='\t')
        print()  


class Base_Grade_list:
    def grade_sum(self):
        pass

    def grade_avg(self):
        pass

    def grade_rank(self):
        pass


class GS_grade_list(Base_Grade_list):
    def __init__(self):
        gc = gspread.service_account(filename='python_course_access_cred.json')
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nqgiOHVyuIM1p4cBKUsi1HfmkaIhjIQdQYamGbkzOhE/edit#gid=0')
        cell_range_pattern = 'c5:j12'
        cell_range = sh.sheet1.get(cell_range_pattern)

        self.grade_list_data = list(cell_range)

        print('\nRead Google sheet and print the data:\n')  
        print_grade_list_data(self.grade_list_data)


    def grade_sum(self):
        for i in range(1, len(self.grade_list_data)):
            total = 0
            for j in range(1, 5):
                total += int(self.grade_list_data[i][j])
            self.grade_list_data[i][5] = total


    def grade_avg(self):
        for i in range(1, len(self.grade_list_data)):
            self.grade_list_data[i][6] = self.grade_list_data[i][5] / 4


    def grade_rank(self):
        grade = []
        for i in range(1, len(self.grade_list_data)):
            grade.append(self.grade_list_data[i][5])
        grade.sort(reverse=True)  
        
        for i in range(len(grade)):
            for j in range(1, len(self.grade_list_data)):
                if self.grade_list_data[j][5] == grade[i]:
                    self.grade_list_data[j][7] =
