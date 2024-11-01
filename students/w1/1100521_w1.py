import sys;

print('hello world for Jarron')

#print hellowrld with variable 
def hello(name,id):
    print("Hello World in function 'hello'.")
    print('My name is ',name,' and my id is ',id,'.')

def showpythonversion():
    print('python version is ', sys.version)
    
#call hello function
hello('鄧晴陽',1100521)
showpythonversion()