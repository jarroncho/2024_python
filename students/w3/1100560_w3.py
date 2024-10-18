import sys
import datetime
import openpyxl
import gspread

# 定義一個函式來打印成績單數據
def print_grade_list_data(grade_list_data):
    for row in grade_list_data:
        print('\t'.join(map(str, row)))

# 定義基礎的成績列表類
class Base_Grade_list:
    def grade_sum(self):
        for i in range(1, len(self.grade_list_data)):
            self.grade_list_data[i][5] = sum(int(self.grade_list_data[i][j]) for j in range(1, 5))

    def grade_avg(self):
        for i in range(1, len(self.grade_list_data)):
            self.grade_list_data[i][6] = self.grade_list_data[i][5] / 4

    def grade_rank(self):
        total_scores = [self.grade_list_data[i][5] for i in range(1, len(self.grade_list_data))]
        sorted_scores = sorted(total_scores, reverse=True)
        for i in range(1, len(self.grade_list_data)):
            self.grade_list_data[i][7] = sorted_scores.index(self.grade_list_data[i][5]) + 1

# 定義 Google Sheets 成績列表類，繼承自基礎類
class GS_grade_list(Base_Grade_list):
    def __init__(self):
        gc = gspread.service_account(filename='python_course_access_cred.json')
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nqgiOHVyuIM1p4cBKUsi1HfmkaIhjIQdQYamGbkzOhE/edit#gid=0')
        cell_range = sh.sheet1.get('c5:j12')

        self.grade_list_data = [cell_range[i:i + 8] for i in range(0, len(cell_range), 8)]
        print('\nRead Google sheet and print the data:\n')
        print_grade_list_data(self.grade_list_data)

# 執行 Google Sheets 成績處理
gs_data = GS_grade_list()
gs_data.grade_sum()
gs_data.grade_avg()
gs_data.grade_rank()
print('\n')
print_grade_list_data(gs_data.grade_list_data)
