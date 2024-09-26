
import sys;

# hello world 

print('hello world for Jarron')



# print hellowrld with variable 
def hello(姓名,ID):
    print('hello world in function')
    print('姓名是:',姓名)
    print('ID是:',ID)


def showpythonversion():
    print('python version is :', sys.version)

# call hello function
hello(姓名 = '宋致遠',ID = 1110605)

showpythonversion()