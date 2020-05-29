import basic

file1 = open('entrada.txt', 'r') 
file2 = open('salida.txt', 'w') 
lines = file1.readlines()
num_linea = 1

for line in lines:
    if line:
        result, error = basic.run('<stdin>', line, num_linea)
        num_linea += 1
    if error: print(error.as_string())
    else:
        print(result)
        for i in range(0,len(result)):
            file2.write('<'+str(result[i])+'>')
            file2.write("   ")

        file2.write('\n')
    
file1.close()
file2.close()
                    
