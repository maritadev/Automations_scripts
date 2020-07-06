import os, sys
import stat


#Script para generar fichero para ejecutar varios scripts o comandos a la vez
#El Script necesita un listado de parametros. Este listado se tiene que llamar rutas.txt
#cada parametro debe ser una linea por que se splitea con \n
print("\nEste script sirve para cuando necesitas ejecutar muchas veces un mismo comando o script, con diferentes parametros.\n")
print("Vas a necesitar tener las rutas o los parametros en un fichero que se llame rutas.txt"
      " Lo ideal es que al final no tenga lineas vacias\n")
print("Vamos a generar un nuevo archivo con todas las lineas"
      " del fichero rutas.txt y por delante, el script o comando que necesitas lanzar muchas veces.\n ")
print("Una vez creado el fichero, se le dan permisos de ejecución.\n")

continuar = str(input("continuamos? (si/no):\n"))

if (len(sys.argv) > 1):
    print('Archivo tablas: ' + sys.argv[1])  # -- Para ver si se han pasado valores por parametro.
    archivo_tablas = sys.argv[1]  # -- archivo donde estan los parametros pasado por parametro
else:
    archivo_tablas = 'rutas.txt'  # -- archivo donde estan los parametros para ejecutar el script
    listado = open("rutas.txt", 'r')  # -- abro listado rutas.txt
    lineas = (len(listado.readlines()))  # -- cuento las lineas de rutas.txt
    listado.close()  # cierro listado rutas.txt

archivo_resultado='file_accion_por_parametro' # nombre del nuevo archivo .py
resultado = open( archivo_resultado , 'w') #abro nuevo archivo para escritura
listado = open(archivo_tablas, 'r') # abro archivo rutas.txt como parametros.

if continuar == 'si':
    opcion = input(str("Necesitas poner al princio o al principio y al final?\n"
                     "elige el numero de opcion (1/2):\n"
                     "1) Solo al principio.\n "
                     "2) Al principio y al final.\n "))

    ####### pasar a parametro cada linea del fichero rutas.txt ############
    if opcion == "1":
        print("solo se va a gregar el nombre del comando o script al principio de cada linea del fichero rutas.txt")
        script = str(input("\nEscribe el nombre del script o comando\n\n"
                           "Si es un script escribi source nombre_del_scrip.extension sin espacio al final.\n\n"
                           "Si es comando solo el comando sin espacio al final: \n")) #defino el nombre del script



        ############# escritura del nuevo script ############

        for i in range(lineas): # por linea del fichero rutas.txt
            linea = (listado.readline().replace("\n","")) #remplazo /n por nada
            split_parametro = linea.split('/n') # spliteo cada linea al final
            parametro = split_parametro[0] #defino cada linea como parametro
            resultado.write(script + ' ' + parametro + '\n') #escribo en el nuevo script el script parametro por cada linea de rutas.txt

            ###### nombre del nuevo script y su ubicacion #####
            print('Archivo '+ archivo_resultado + ' con el nombre del script o comando y sus parametros se creado en  ' + os.getcwd())
            resultado.close() #cerramos la escritura
            listado.close() #cerramos la lectura de parametros
            print("ahora vamos a darle permisos de ejecucion al nuevo fichero:" + archivo_resultado)
            os.chmod(archivo_resultado, os.stat(archivo_resultado).st_mode | stat.S_IXUSR ) #le damos un chmod +x

    if opcion == "2":
        print("Se va a gregar el nombre del comando o script al principio de cada linea del fichero rutas.txt y "
              "al final el directorio que vas a indicar a continuacion. ")

        home = '/local/local/user'

        if (len(sys.argv) > 1):
            print('Archivo tablas: ' + sys.argv[1])  # -- Para ver si se han pasado valores por parametro.
            archivo_tablas = sys.argv[1]  # -- archivo donde estan los parametros pasado por parametro
        else:
            archivo_tablas = 'rutas.txt'  # -- archivo donde estan los parametros para ejecutar el script
            listado = open("rutas.txt", 'r')  # -- abro listado rutas.txt
            lineas = (len(listado.readlines()))  # -- cuento las lineas de rutas.txt
            listado.close()  # cierro listado rutas.txt

            script = input(str("\nEscribe el nombre del script o comando\n\n"
                               "Si es un script escribi source nombre_del_scrip.extension sin espacio al final.\n\n"
                               "Si es comando solo el comando sin espacio al final: \n"))  # defino el nombre del script

            nvo_dir = input(str("\nEscribe el nombre del nuevo directorio. Al final de cada linea se va a agregar "
                                + home + '/el nombre del directorio que escribas ahora.\n'))

            archivo_resultado = 'file_accion_por_parametro'  # nombre del nuevo archivo .py
            resultado = open(archivo_resultado, 'w')  # abro nuevo archivo para escritura
            listado = open(archivo_tablas, 'r')  # abro archivo rutas.txt como parametros.

            ############# escritura del nuevo script ############

            for i in range(lineas):  # por linea del fichero rutas.txt
                linea = (listado.readline().replace("\n", ""))  # remplazo /n por nada
                split_parametro = linea.split('/n')  # spliteo cada linea al final
                parametro = split_parametro[0]  # defino cada linea como parametro
                resultado.write(
                    script + ' ' + parametro + ' ' + home + '/' + nvo_dir + '\n')  # escribo en el nuevo script el script parametro por cada linea de rutas.txt

            ###### nombre del nuevo script y su ubicacion #####
            print('Archivo ' + archivo_resultado + ' con el nombre del script o comando y sus parametros se creado en  ' + os.getcwd())
            resultado.close()  # cerramos la escritura
            listado.close()  # cerramos la lectura de parametros
            print("ahora vamos a darle permisos de ejecucion al nuevo fichero:\n" + archivo_resultado)
            os.chmod(archivo_resultado, os.stat(archivo_resultado).st_mode | stat.S_IXUSR)  # le damos un chmod +x


if continuar == "no":
    print("BYE")
    exit()

