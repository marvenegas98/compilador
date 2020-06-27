import main
import sys

def main2():
    
    file1 = open('prueba3.txt', 'r') 
    file2 = open('salida.txt', 'w+') 
    lines = file1.readlines()
    num_linea = 0

    for line in lines:
        if line:
            result, error = main.run('<stdin>', line, num_linea)
            num_linea += 1
        if error: 
            """
            for i in range(0,len(result)):
                file2.write('<'+str(result[i])+'>')
                file2.write("   ")
            """
            print(error.as_string())
            exit()

        file2.write('\n')
        for i in range(0,len(result)):
            file2.write('<'+str(result[i])+'>')
            file2.write("   ")

        file2.write('\n')

    file1.close()
    file2.close()
    exit()

main2()
