# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RfSbC4ujDlA_O_sku8iTyVt8ZG0EUL26
"""

def calculate_scores(grade_list):
    for student in grade_list:
        total = sum(student[1:5])
        average = total / 4
        student[5] = total
        student[6] = average

grade_list = [['John', 72, 88, 88, 84, 0, 0, 0],
              ['Eric', 88, 82, 77, 80, 0, 0, 0],
              ['Rick', 63, 49, 55, 68, 0, 0, 0],
              ['Mary', 72, 64, 82, 74, 0, 0, 0],
              ['Alice', 92, 79, 93, 89, 0, 0, 0],
              ['Match', 81, 72, 62, 70, 0, 0, 0],
              ['Sunny', 78, 77, 51, 72, 0, 0, 0]]

calculate_scores(grade_list)

sorted_grades = sorted(grade_list, key=lambda x: x[5], reverse=True)
rank_dict = {student[0]: rank + 1 for rank, student in enumerate(sorted_grades)}

for student in grade_list:
    student[7] = rank_dict[student[0]]

print('姓名\t國文\t英文\t數學\t理化\t總分\t平均\t名次')
print('------------------------------------------------------------')

for student in grade_list:
    print(student[0], end='\t')
    for score in student[1:]:
        print(score, end='\t')
    print()

