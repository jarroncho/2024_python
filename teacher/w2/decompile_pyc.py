
import sys
import dis
pyc_path = sys.argv[1]
print(pyc_path)
with open(pyc_path, 'rb') as f:
    code = compile(f.read(), pyc_path, 'exec')    
         
dis.dis(code)   


