import sys;

list=[['John',72,88,88,84],
      ['Eric',88,83,77,80],
      ['Rick',63,49,55,68],
      ['Mary',73,64,82,74],
      ['Alice',92,79,93,89],
      ['Match',81,72,62,70],
      ['Sunny',78,77,51,72]]

print('姓名\t國文\t英文\t數學\t理化\t總分\t平均\t名次')
print('------------------------------------------------------------')

total=[]
place=[]


for i in range(len(list)):
    addd=0
    for j in range(1,5):   
        addd+=int(list[i][j])
    total.append(addd)        

for i in range(len(total)):
    p=1
    for j in range(len(total)):
        if total[i]<total[j]:
            p+=1
    place.append(p)
   


for i in range(len(list)):
    print(list[i][0],end='\t')
    for j in range(1,len(list[i])):
        print(list[i][j],end='\t')
        add=0
    for k in range(1,5):   
        add+=int(list[i][k])
    print(add,end='\t')    
    print(add/4,end='\t')
    print(place[i])      
