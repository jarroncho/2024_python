import sys;
import datetime
import openpyxl
import gspread

class Base:
    def __init__(self):
        pass

    def sum_average_ranking(self):
        for i in range(1, len(self.grade_list_data)):
            self.grade_list_data[i][5] = int(self.grade_list_data[i][1]) + int(self.grade_list_data[i][2]) + int(self.grade_list_data[i][3]) + int(self.grade_list_data[i][4])
            self.grade_list_data[i][6] = self.grade_list_data[i][5] / 4
        header = self.grade_list_data[0]
        data = self.grade_list_data[1:]
        sorted_data = sorted(data, key=lambda x: int(x[5]), reverse=True)
        self.grade_list_sort = [header] + sorted_data
        for i in range(1, len(self.grade_list_sort)):
            self.grade_list_sort[i][7] = i

    def print_grade_list_data(self):
        for i in range(len(self.grade_list_data)):
            print(self.grade_list_data[i][0], end='\t')
            for j in range(1, len(self.grade_list_data[i])):
                print(self.grade_list_data[i][j], end='\t')
            print()
    
class Excel(Base):
    def __init__(self, filename, cell_range_pattern):
        workbook = openpyxl.load_workbook(r'teacher\w3\grade_list.xlsx')

        # Get the sheet names
        sheet_names = workbook.sheetnames
        sheet_name=sheet_names[0]
        sheet = workbook[sheet_name]

        # Specify the cell coordinates (row and column indices, 1-based index)
        # Access the cell range
        cell_range = sheet[cell_range_pattern]

        # Initialize a 2D list to store cell values
        self.grade_list_data = []

        for row in cell_range:
            row_list = []
            for cell in row:        
                row_list.append(cell.value)
            self.grade_list_data.append(row_list)

        # Close the workbook (important to release resources)
        workbook.close()

cell_range_pattern='c5:j12'

EXgrade=Excel('grade_list.xlsx',cell_range_pattern)
EXgrade.sum_average_ranking()

print('\nRead Excel file and print the data:\n')
EXgrade.print_grade_list_data()
################################

class GS(Base):
    def __init__(self,sh,cell_range_pattern):
        cell_range=sh.sheet1.get(cell_range_pattern)
        self.grade_list_data = list(cell_range)

gc = gspread.service_account(filename='python_course_access_cred.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nqgiOHVyuIM1p4cBKUsi1HfmkaIhjIQdQYamGbkzOhE/edit#gid=0')


Ggrade=GS(sh,cell_range_pattern)
Ggrade.sum_average_ranking()

print('\nRead Google sheet and print the data:\n')
Ggrade.print_grade_list_data()
