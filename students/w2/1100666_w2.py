
import sys;   


"""
姓名	國文	英文	數學	理化	總分	平均	名次
John	72	    88	    88	    84			
Eric	88	    82	    77	    80			
Rick	63	    49	    55	    68			
Mary	72	    64	    82	    74			
Alice	92	    79	    93	    89			
Match	81	    72	    62	    70			
Sunny	78	    77	    51	    72			
"""

grade_list = [['John', 72, 88, 88, 84, 0, 0, 0], 
              ['Eric', 88, 82, 77, 80, 0, 0, 0], 
              ['Rick', 63, 49, 55, 68, 0, 0, 0], 
              ['Mary', 72, 64, 82, 74, 0, 0, 0], 
              ['Alice', 92, 79, 93, 89, 0, 0, 0], 
              ['Match', 81, 72, 62, 70, 0, 0, 0], 
              ['Sunny', 78, 77, 51, 72, 0, 0, 0]]
for i in range(len(grade_list)):
    grade_list[i][5]=grade_list[i][1]+grade_list[i][2]+grade_list[i][3]+grade_list[i][4]
    grade_list[i][6]=(grade_list[i][5])/4

grade_list_sort = sorted(grade_list, key=lambda x: x[5],reverse=True)
print(grade_list_sort)

for i in range(len(grade_list_sort)):    
    grade_list_sort[i][7]=i+1

a=[0,0,0,0,0,0,0]
b=[0,0,0,0,0,0,0]

for i in range(len(grade_list)):
    grade_list[i][5] = grade_list[i][1] + grade_list[i][2] + grade_list[i][3] + grade_list[i][4]
    grade_list[i][6] = grade_list[i][5] / 4
    a[i]=grade_list[i][6]

c=sorted(a)

for j in range(7): 
    for i in range(7):
        if a[j] == c[i]:
            b[j]=7-i
            break
    
        

for i in range(len(grade_list)):
    grade_list[i][7]=b[i]



print('姓名\t國文\t英文\t數學\t理化\t總分\t平均\t名次')
print('------------------------------------------------------------')

for i in range(len(grade_list)):
    print(grade_list[i][0], end='\t')
    for j in range(1, len(grade_list[i])):
        print(grade_list[i][j], end='\t')
    print()