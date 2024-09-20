grade_list = [
    ['John', 72, 88, 88, 84, 0, 0, 0],
    ['Eric', 88, 82, 77, 80, 0, 0, 0],
    ['Rick', 63, 49, 55, 68, 0, 0, 0],
    ['Mary', 72, 64, 82, 74, 0, 0, 0],
    ['Alice', 92, 79, 93, 89, 0, 0, 0],
    ['Match', 81, 72, 62, 70, 0, 0, 0],
    ['Sunny', 78, 77, 51, 72, 0, 0, 0]
]

# 計算總分與平均
for i in range(len(grade_list)):
    total = sum(grade_list[i][1:5])
    average = total / 4
    grade_list[i][5] = total
    grade_list[i][6] = average

# 根據總分進行排序（分數低的在前）
sorted_grade_list = sorted(grade_list, key=lambda x: x[5])

# 計算名次（分數低的名次高）
for i in range(len(sorted_grade_list)):
    sorted_grade_list[i][7] = i + 1

# 輸出標題
print(f"{'姓名':<4}{'國文':>5}{'英文':>6}{'數學':>6}{'理化':>6}{'總分':>6}{'平均':>4}{'名次':>8}")
print('------------------------------------------------------------')

# 輸出每個學生的成績
for student in sorted_grade_list:
    name, chinese, english, math, science, total, avg, rank = student
    print(f"{name:<6}{chinese:>6}{english:>8}{math:>8}{science:>8}{total:>8}{avg:>8.1f}{rank:>8}")
