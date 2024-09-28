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
    def grade_sum(self):
        pass

    def grade_avg(self):
        pass

    def grade_rank(self):
        pass

class Excel_grade_list(Base_Grade_list):
    def __init__(self):
        self.grade_list=[]
        # Load the Excel workbook and select the sheet
        workbook = openpyxl.load_workbook('grade_list.xlsx')

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

        for row in cell_range:
            row_list = []
            for cell in row:        
                row_list.append(cell.value)
            self.grade_list.append(row_list)


        print('\nRead Excel file and print the data:\n')
        print_grade_list_data(self.grade_list)


        # Close the workbook (important to release resources)
        workbook.close()  
    
    def grade_sum(self):
        for i in range(1,len(self.grade_list)):
            total=0
            for j in range(1,5):
                total=total+int(self.grade_list[i][j])
            self.grade_list[i][5]=total

    def grade_avg(self):
        for i in range(1,len(self.grade_list)):
            self.grade_list[i][6]=self.grade_list[i][5]/4

    def grade_rank(self):
        grade=[]
        for i in range(1,len(self.grade_list)):
            grade.append(self.grade_list[i][5])

        grade.sort(reverse=True)
        
        for i in range(len(grade)):
            for j in range(1,len(self.grade_list)):
                if self.grade_list[j][5]==grade[i]:
                    self.grade_list[j][7]=i+1

class GS_grade_list(Base_Grade_list):
    def __init__(self):
        gc = gspread.service_account(filename='python_course_access_cred.json')
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nqgiOHVyuIM1p4cBKUsi1HfmkaIhjIQdQYamGbkzOhE/edit#gid=0')

        cell_range_pattern='c5:j12'
        cell_range=sh.sheet1.get(cell_range_pattern)

        #print(cell_range)
        #print(type(cell_range))    

        self.grade_list_data=list(cell_range)

        print('\nRead Google sheet and print the data:\n')
        print_grade_list_data(self.grade_list_data)

    def grade_sum(self):
        for i in range(1,len(self.grade_list_data)):
            total=0
            for j in range(1,5):
                total=total+int(self.grade_list_data[i][j])
            self.grade_list_data[i][5]=total

    def grade_avg(self):
        for i in range(1,len(self.grade_list_data)):
            self.grade_list_data[i][6]=self.grade_list_data[i][5]/4

    def grade_rank(self):
        grade=[]
        for i in range(1,len(self.grade_list_data)):
            grade.append(self.grade_list_data[i][5])

        grade.sort(reverse=True)
        
        for i in range(len(grade)):
            for j in range(1,len(self.grade_list_data)):
                if self.grade_list_data[j][5]==grade[i]:
                    self.grade_list_data[j][7]=i+1


xlsx_data=Excel_grade_list()
xlsx_data.grade_sum()
xlsx_data.grade_avg()
xlsx_data.grade_rank()
print('\n')
print_grade_list_data(xlsx_data.grade_list)
print('\n')
gs_data=GS_grade_list()
gs_data.grade_sum()
gs_data.grade_avg()
gs_data.grade_rank()
print('\n')
print_grade_list_data(gs_data.grade_list_data)