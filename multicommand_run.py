import os,sys

print("\nVamos a ejecutar comando por cada linea del fichero rutas.txt\n")
print("\nEs necesario tener un fichero con las rutas o llamado rutas.txt\n")
comando = str(input("\nEscribi el comando que necesitar ejecutar:\n"))

if (len(sys.argv)>1):
    print('Archivo tablas: ' + sys.argv[1])
    archivo_tablas=sys.argv[1] ##archivo donde estan los parametros pasado por parametro
else:
    archivo_tablas = 'rutas.txt' ##archivo donde estan los parametros para ejecutar el script

listado = open("rutas.txt", 'r')
lineas = (len(listado.readlines())) #cuento las lineas de rutas.txt
listado.close()

listado = open(archivo_tablas, 'r')

for i in range(lineas):
    linea = (listado.readline().replace("\n", ""))
    split_parametro = linea.split('\n')
    parametro = str(split_parametro[0])
    log = os.system(str(comando + ' ') + str(parametro))

listado.close()  # cerramos la lectura de parametros


