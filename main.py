import basic

file1 = open('entrada.txt', 'r') 
file2 = open('salida.txt', 'w') 
lines = file1.readlines()

for line in lines:
    if line:
    	result, error = basic.run('<stdin>', line)
    	if error: print(error.as_string())
    	else:
    		print(result)
    		file2.write(str(result))
    
file1.close()
file2.close()
