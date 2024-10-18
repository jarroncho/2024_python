import sys;
import datetime
import openpyxl
import gspread


def print_grade_list_data(grade_list_data):
    for i in range(len(grade_list_data)):
        print(grade_list_data[i][0], end='\t')
        for j in range(1, len(grade_list_data[i])):
            print(grade_list_data[i][j], end='\t')
        ## new line
        print()

class Base_Grade_list:
    def __init__(self):
        pass

    def sum(self):
        for i in range(1, len(self.grade_list_data)):
            self.grade_list_data[i][5] = int(self.grade_list_data[i][1]) + int(self.grade_list_data[i][2]) + int(self.grade_list_data[i][3]) + int(self.grade_list_data[i][4])

    def average(self):
        for i in range(1, len(self.grade_list_data)):
            self.grade_list_data[i][6] = self.grade_list_data[i][5] / 4

    def ranking(self):
        header = self.grade_list_data[0]  # 取得第一列 (通常是標題行)
        data = self.grade_list_data[1:]  # 取得剩餘的數據
        sorted_data = sorted(data, key=lambda x: int(x[5]), reverse=True)
        self.grade_list_sort = [header] + sorted_data
        for i in range(1, len(self.grade_list_sort)):
            self.grade_list_sort[i][7] = i

class Excel_grade_list(Base_Grade_list):
    def __init__(self, filename, cell_range_pattern):
        # Load the Excel workbook and select the sheet
        workbook = openpyxl.load_workbook(filename)

        # Get the sheet names
        sheet_names = workbook.sheetnames
        sheet_name = sheet_names[0]
        # Print the sheet names
        #print("Sheet names:", self.sheet_names)
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

    def grade_list_data(self):
        return self.grade_list_data

class GS_grade_list(Base_Grade_list):
    def __init__(self, sh, cell_range_pattern):
        cell_range = sh.sheet1.get(cell_range_pattern)
        self.grade_list_data = list(cell_range)

    def grade_list_data(self):
        return self.grade_list_data


if __name__ == '__main__':
    gc = gspread.service_account(filename='python_course_access_cred.json')
    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1nqgiOHVyuIM1p4cBKUsi1HfmkaIhjIQdQYamGbkzOhE/edit#gid=0')
    cell_range_pattern = 'c5:j12'

    Ggrade = GS_grade_list(sh, cell_range_pattern)
    Egrade = Excel_grade_list('grade_list.xlsx', cell_range_pattern)


    print('Read Google sheet and print the data:')
    Ggrade.sum()
    Ggrade.average()
    Ggrade.ranking()
    print_grade_list_data(Ggrade.grade_list_data)


    print('\n\nRead Excel file and print the data:')
    Egrade.sum()
    Egrade.average()
    Egrade.ranking()
    print_grade_list_data(Egrade.grade_list_data)
