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
arr=[]

for i in range(len(grade_list)):
  grade_list[i][5]=grade_list[i][4]+grade_list[i][3]+grade_list[i][2]+grade_list[i][1]
  grade_list[i][6]=float(grade_list[i][5]/4)
  arr.append(grade_list[i][6])

arr=sorted(arr,reverse=True)
print(arr)
for j in range(len(grade_list)):
   for i,num in enumerate(arr):
      if grade_list[j][6]==num:
         grade_list[j][7]=i+1
      
                  

print('姓名\t國文\t英文\t數學\t理化\t總分\t平均\t名次')
print('------------------------------------------------------------')

for i in range(len(grade_list)):
    print(grade_list[i][0], end='\t')
    for j in range(1, len(grade_list[i])):
        print(grade_list[i][j], end='\t')
    print()