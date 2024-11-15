import sys;

print('hello world for Jarron')

#print hellowrld with variable 
def hello():
    print("Hello World in function 'hello'.")
    print('My name is ',name,' and my id is ',id,'.')

def showpythonversion():
    print('python version is ', sys.version)
    
#call hello function
name='傅宣文'
id=1100516
hello()
showpythonversion()
