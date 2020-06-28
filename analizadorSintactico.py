import main
import sys
file1 = open(sys.argv[1], 'r') 
file2 = open(sys.argv[2], 'w+') 
lines = file1.readlines()
num_linea = 0

for line in lines:
    if line:
        line = line.lstrip()
        line = line.rstrip()
        print("Linea del archivo :", line)
        result, error = main.run('<stdin>', line,num_linea)
        if error: 
            print(error.as_string())
            exit()
        num_linea += 1
        print(result)
        print("\n")
    if error: 
        print(error.as_string())
        exit()
"""
    file2.write('\n')
    for i in range(0,len(result)):
        file2.write('<'+str(result[i])+'>')
        file2.write("   ")

    file2.write('\n')
    """

file1.close()
file2.close()
exit()
                    
