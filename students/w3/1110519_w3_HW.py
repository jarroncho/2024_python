import sys
import datetime
import openpyxl
import gspread

# 定義一個函式來打印成績單數據
def print_grade_list_data(grade_list_data):
    for i in range(len(grade_list_data)):
        print(grade_list_data[i][0], end='\t')
        for j in range(1, len(grade_list_data[i])):
            print(grade_list_data[i][j], end='\t')
        print()  # 換行

# 定義基礎的成績列表類
class Base_Grade_list:
    def grade_sum(self):
        pass

    def grade_avg(self):
        pass

    def grade_rank(self):
        pass
'''
# 定義 Excel 成績列表類，繼承自基礎類
class Excel_grade_list(Base_Grade_list):
    def __init__(self):
        self.grade_list = []  # 儲存成績的列表
        
        # 加載 Excel 工作簿並選擇工作表
        workbook = openpyxl.load_workbook('grade_list.xlsx')
        sheet_names = workbook.sheetnames  # 獲取所有工作表名稱
        sheet_name = sheet_names[0]  # 選擇第一個工作表
        print("Sheet names:", sheet_names)  # 打印工作表名稱
        sheet = workbook[sheet_name]  # 選擇工作表

        # 定義要讀取的範圍，C5 到 J12
        cell_range_pattern = 'c5:j12'
        cell_range = sheet[cell_range_pattern]

        # 逐行讀取單元格數據
        for row in cell_range:
            row_list = []
            for cell in row:
                row_list.append(cell.value)
            self.grade_list.append(row_list)

        print('\nRead Excel file and print the data:\n')  # 打印 Excel 的成績數據
        print_grade_list_data(self.grade_list)

        workbook.close()  # 關閉工作簿以釋放資源
    
    # 計算每位學生的成績總和
    def grade_sum(self):
        for i in range(1, len(self.grade_list)):
            total = 0
            for j in range(1, 5):
                total += int(self.grade_list[i][j])
            self.grade_list[i][5] = total

    # 計算每位學生的平均成績
    def grade_avg(self):
        for i in range(1, len(self.grade_list)):
            self.grade_list[i][6] = self.grade_list[i][5] / 4

    # 計算每位學生的成績排名
    def grade_rank(self):
        grade = []
        for i in range(1, len(self.grade_list)):
            grade.append(self.grade_list[i][5])
        grade.sort(reverse=True)  # 成績從高到低排序
        
        for i in range(len(grade)):
            for j in range(1, len(self.grade_list)):
                if self.grade_list[j][5] == grade[i]:
                    self.grade_list[j][7] = i + 1
'''
# 定義 Google Sheets 成績列表類，繼承自基礎類
class GS_grade_list(Base_Grade_list):
    def __init__(self):
        # 使用 Google 雲端帳戶憑證
        gc = gspread.service_account(filename='python_course_access_cred.json')
        # 打開 Google 試算表
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nqgiOHVyuIM1p4cBKUsi1HfmkaIhjIQdQYamGbkzOhE/edit#gid=0')

        # 讀取範圍 C5 到 J12
        cell_range_pattern = 'c5:j12'
        cell_range = sh.sheet1.get(cell_range_pattern)

        self.grade_list_data = list(cell_range)

        print('\nRead Google sheet and print the data:\n')  # 打印 Google 試算表的成績數據
        print_grade_list_data(self.grade_list_data)

    # 計算每位學生的成績總和
    def grade_sum(self):
        for i in range(1, len(self.grade_list_data)):
            total = 0
            for j in range(1, 5):
                total += int(self.grade_list_data[i][j])
            self.grade_list_data[i][5] = total

    # 計算每位學生的平均成績
    def grade_avg(self):
        for i in range(1, len(self.grade_list_data)):
            self.grade_list_data[i][6] = self.grade_list_data[i][5] / 4

    # 計算每位學生的成績排名
    def grade_rank(self):
        grade = []
        for i in range(1, len(self.grade_list_data)):
            grade.append(self.grade_list_data[i][5])
        grade.sort(reverse=True)  # 成績從高到低排序
        
        for i in range(len(grade)):
            for j in range(1, len(self.grade_list_data)):
                if self.grade_list_data[j][5] == grade[i]:
                    self.grade_list_data[j][7] = i + 1

# 執行 Google Sheets 成績處理
gs_data = GS_grade_list()
gs_data.grade_sum()
gs_data.grade_avg()
gs_data.grade_rank()
print('\n')
print_grade_list_data(gs_data.grade_list_data)

'''
# 執行 Excel 成績處理
xlsx_data = Excel_grade_list()
xlsx_data.grade_sum()
xlsx_data.grade_avg()
xlsx_data.grade_rank()
print('\n')
print_grade_list_data(xlsx_data.grade_list)
print('\n')
'''

