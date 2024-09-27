grade_list = [['John', 72, 88, 88, 84, 0, 0, 0], 
              ['Eric', 88, 82, 77, 80, 0, 0, 0], 
              ['Rick', 63, 49, 55, 68, 0, 0, 0], 
              ['Mary', 72, 64, 82, 74, 0, 0, 0], 
              ['Alice', 92, 79, 93, 89, 0, 0, 0], 
              ['Match', 81, 72, 62, 70, 0, 0, 0], 
              ['Sunny', 78, 77, 51, 72, 0, 0, 0]]

for student in grade_list:
    total = sum(student[1:5])
    average=total/4
    student[5] = total
    student[6] = average

sorted_grade_list = sorted(grade_list, key=lambda x: x[5], reverse=True)
for rank,student in enumerate(sorted_grade_list, start=1):
    student[7] = rank

for sorted_student in sorted_grade_list:
    for original_student in grade_list:
        if sorted_student[0] == original_student[0]:
            original_student[7] = sorted_student[7]

print('姓名\t國文\t英文\t數學\t理化\t總分\t平均\t名次')
print('------------------------------------------------------------')

for student in sorted_grade_list:
    print(f"{student[0]}\t{student[1]}\t{student[2]}\t{student[3]}\t{student[4]}\t{student[5]}\t{student[6]:.2f}\t{student[7]}")