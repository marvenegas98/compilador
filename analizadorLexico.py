import basic
import sys
file1 = open(sys.argv[1], 'r') 
file2 = open(sys.argv[2], 'w+') 
lines = file1.readlines()
num_linea = -1

for line in lines:
    if line:
        result, error = basic.run('<stdin>', line, num_linea)
        num_linea += 1
    if error: 
        #print(result)
        for i in range(0,len(result)):
            file2.write('<'+str(result[i])+'>')
            file2.write("   ")
        print(error.as_string())
        exit()

    file2.write('\n')
    #print(result)
    for i in range(0,len(result)):
        file2.write('<'+str(result[i])+'>')
        file2.write("   ")

    file2.write('\n')

file1.close()
file2.close()
exit()
                    
