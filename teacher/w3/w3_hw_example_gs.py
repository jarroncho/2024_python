#pip install gspread oauth2client
import gspread


def print_grade_list_data(grade_list_data):
        for i in range(len(grade_list_data)):
            print(grade_list_data[i][0], end='\t')
            for j in range(1, len(grade_list_data[i])):
                print(grade_list_data[i][j], end='\t')
            ## new line
            print()

gc = gspread.service_account(filename='python_course_access_cred.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nqgiOHVyuIM1p4cBKUsi1HfmkaIhjIQdQYamGbkzOhE/edit#gid=0')

cell_range_pattern='c5:j12'
cell_range=sh.sheet1.get(cell_range_pattern)

#print(cell_range)
#print(type(cell_range))    

grade_list_data=list(cell_range)

print('\nRead Google sheet and print the data:\n')
print_grade_list_data(grade_list_data)