import sys;

# hello world 

print('hello world for Jarron')


# print hellowrld with variable 
def hello(name,id):
    print('hello world in function')
    print('my name is:',name)
    print('my id is:',id)

def showpythonversion():
    print('python version is :', sys.version)

#my name and id
my_name="盧彥伶"
my_id=1100609
# call hello function
hello(my_name,my_id)

showpythonversion()