#version 0.5
import os #para ejecutar cosas de sistemas
import paramiko #conexion ssh

#-------- Con este Script vamos a seleccion un archivo de nuestro ordenador personal
#-------- pasarlo por scp a un servidor
#-------- y si queremos ejecutarlo en impala o hive
#-------- se necesita definir nuestro directorio de donde van a listar los archivo en la variable home
#-------- para elegir el fichero a pasar se van a listar los ficheros con extension .sql, hql y txt.
# ------- esto se puede cambiar en la variable ext.
#-------- se necesita definir el directorio destino en el servidor en la variable destino
#-------- el usuario para ssh y scp se define en la variable user


print("Con este script vamos a:\n\n"
      "1) conectarnos por scp\n\n"
      "2) listar los ficheros del directorio jiras\n\n"
      "3) Seleccionar el fichero que quiero llevarme\n\n"
      "4) llevar el fichero al servidor donde lo voy a guardar\n\n"
      "5) ejecutar comando de impala\n\n")

#-------- variables principales ---------------
user = 'userssh'
serverprod = 'server1'
serverdev = 'server2'
servercua = 'server3'
destinoprod = '/ruta/server1'
destinodev = '/ruta/server2'
destinocua = '/ruta/server3'
home = '/home/user' # -- Directorio home local --
k = paramiko.RSAKey.from_private_key_file("/home/user/.ssh/id_rsa")
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #no se que hace

#-------------------------------- Funciones principales --------------------------------------------------

#--------------------- Funcion para pasar a fichero a server ---------------------------------------------

def pasar_destino():
    if entorno == "1": # -- desarrollo
        os.system('scp ' +  home + '/' + str(seleccion)  + ' ' + user + '@' + serverdev + ':' + str(destinodev))

    if entorno == "2": # -- cua
        os.system('scp ' + home + '/' + str(seleccion)  + ' ' + user + '@' + servercua + ':' + str(destinocua))
        

    if entorno == "3":  # -- produccion
        os.system('scp ' + home + '/' + str(seleccion)  + ' ' + user + '@' + serverprod + ':' + str(destinoprod))


#------- Funcion para listar el directorio destino para comprarobar que se haya pasado el fichero --------

def ls_destino():
    if entorno == "1":  # -- desarrollo
        os.system('ssh ' + user + '@' + serverdev + ' ls -ltr ' + str(destinodev))

    if entorno == "2":  # -- cua
        os.system('ssh ' + user + '@' + servercua + ' ls -ltr ' + str(destinocua))

    if entorno == "3":  # -- produccion
        os.system('ssh ' + user + '@' + serverprod + ' ls -ltr ' + str(destinoprod))


#--------------------- Funcion para traer la salida.txt a nuestro home -------------------------------------

def traer_salida():
    if entorno == "1": # -- desarrollo
        os.system('scp ' + user + '@' + serverdev + ':' + str(destinodev) + ' ' + 'salida_' + str(seleccion) + '.txt')

    if entorno == "2": # -- cua
        os.system('scp ' + user + '@' + servercua + ':' + str(destinocua) + ' ' + 'salida_' + str(seleccion) + '.txt')

    if entorno == "3":  # -- produccion
        os.system('scp ' + user + '@' + serverprod + ':' + str(destinoprod) + ' ' + 'salida_' + str(seleccion) + '.txt')


#--------- Funcion para listar el directorio home y comprarobar que se haya traido la salida ---------------

def ls_home():
    os.system('ls -ltr ' + str(home))


#------------------Funcion para ejecutar el fichero seleccionado con impala --------------------------------
#------- Esta funcion es llamada desde la funcion ejecutar -------------------------------------------------

def impala():
    if entorno == "1": # ejecucion impala en Desarrollo
        print("se va a ejecutar el fichero seleccionado: " + seleccion + " en impala "
                                                                         "en el entorno de Desarrollo:\n" )
        continuar_ejecucion = input((str("Continuamos?: (si/no\n")))

        if continuar_ejecucion == "si":
            #--- conexion por ssh
            c.connect(hostname=serverdev, username=user, pkey=k)
            #--- ejecucion de comando
            c.exec_command('nohup impala-shell -i impala.server1 -d default -k '
                           '--ssl --ca_cert=/opt/cloudera/security/truststore/ca-truststore.pem -f '
                           + destinodev + '/' + seleccion + '>&' + destinodev + '/salida_' + seleccion + '.txt')
            #--- cierre de conexion
            c.close()


        if continuar_ejecucion == "no": #-- no se ejecuta pero si se pasa el fichero.
            print("El fichero de paso, pero no se ejecuto.\n"
                  "BYE")

    if entorno == "2": #-- ejecucion impala en Cua
        print("se va a ejecutar el fichero seleccionado: " + seleccion + " en impala "
                                                                         "en el entorno de Cua:\n")
        continuar_ejecucion = input((str("Continuamos?: (si/no\n")))

        if continuar_ejecucion == "si":
            # --- conexion por ssh
            c.connect(hostname=servercua, username=user, pkey=k)
            # --- ejecucion de comando
            c.exec_command('nohup impala-shell -i impala.server2 -d default -k '
                           '--ssl --ca_cert=/opt/cloudera/security/truststore/ca-truststore.pem -f '
                           + destinocua + '/' + seleccion + '>&' + destinocua + '/salida_' + seleccion + '.txt')
            # --- cierre de conexion
            c.close()

        if continuar_ejecucion == "no": #-- no se ejecuta pero si se pasa el fichero.
            print("El fichero de paso, pero no se ejecuto.\n"
                  "BYE")

    if entorno == "3": #--  ejecucion impala en Produccion
        print("se va a ejecutar el fichero seleccionado: " + seleccion + " en impala "
                                                                         "en el entorno de Produccion:\n")
        continuar_ejecucion = input((str("Continuamos?: (si/no\n")))

        if continuar_ejecucion == "si":
            # --- conexion por ssh
            c.connect(hostname=serverprod, username=user, pkey=k)
            # --- ejecucion de comando
            c.exec_command('nohup impala-shell -i impala.server3 -d default -k '
                           '--ssl --ca_cert=/opt/cloudera/security/truststore/ca-truststore.pem -f '
                           + destinoprod + '/' + seleccion + '>&' + destinoprod + '/salida_' + seleccion + '.txt')
            # --- cierre de conexion
            c.close()

        if continuar_ejecucion == "no": #-- no se ejecuta pero si se pasa el fichero.
            print("El fichero se paso, pero no se ejecuto.\n"
                  "BYE")


#---------------- Funcion para ejecutar el fichero seleccionado con hive -----------------------------------
#------- Esta funcion es llamada desde la funcion ejecutar -------------------------------------------------
def hive():
    if entorno == "1": #-- ejecucion hive en Desarrollo
        print("se va a ejecutar el fichero seleccionado: " + seleccion + " en hive "
                                                                         "en el entorno de Desarrollo:\n" )
        continuar_ejecucion = input((str("Continuamos?: (si/no\n")))

        if continuar_ejecucion == "si":
            # --- conexion por ssh
            c.connect(hostname=serverdev, username=user, pkey=k)
            # --- ejecucion de comando
            c.exec_command('nohup ' + 'beeline -u "jdbc:hive2://hive.server1;'
                                      'ssl=true;sslTrustStore=/opt/cloudera/security/jks/truststore.jks;'
                                      'trustStorePassword=pass;'
                                      'principal=hive/hive.server1"  -f ' +
                           destinodev + '/' + seleccion + '>&' + destinodev + '/salida_' + seleccion + '.txt')
            # --- cierre de conexion
            c.close()

        if continuar_ejecucion == "no": #-- no se ejecuta pero si se pasa el fichero.
            print("El fichero se paso, pero no se ejecuto.\n"
                  "BYE")

    if entorno == "2": #-- ejecucion hive en Cua
        print("se va a ejecutar el fichero seleccionado: " + seleccion + " en hive "
                                                                         "en el entorno de Cua:\n")
        continuar_ejecucion = input((str("Continuamos?: (si/no\n")))

        if continuar_ejecucion == "si":
            # --- conexion por ssh
            c.connect(hostname=servercua, username=user, pkey=k)
            # --- ejecucion de comando
            c.exec_command('nohup ' + 'beeline -u  "jdbc:hive2://hive.server2;'
                                      'ssl=true;sslTrustStore=/opt/cloudera/security/jks/truststore.jks;'
                                      'trustStorePassword=pass;'
                                      'principal=hive/hive.server2"  -f '
                           + destinocua + '/' + seleccion + '>&' + destinocua + '/salida_' + seleccion + '.txt')
            # --- cierre de conexion
            c.close()

        if continuar_ejecucion == "no": #-- no se ejecuta pero si se pasa el fichero.
            print("El fichero se paso, pero no se ejecuto.\n"
                  "BYE")

    if entorno == "3": # -- ejecucion hive en Produccion
        print("se va a ejecutar el fichero seleccionado: " + seleccion + " en hive "
                                                                         "en el entorno de Produccion:\n")

        continuar_ejecucion = input((str("Continuamos?: (si/no\n")))

        if continuar_ejecucion == "si":
            # --- conexion por ssh
            c.connect(hostname=serverprod, username=user, pkey=k)
            # --- ejecucion de comando
            c.exec_command('nohup ' + 'beeline -u  "jdbc:hive2://hive.server3;'
                                      'ssl=true;sslTrustStore=/opt/cloudera/security/jks/truststore.jks;'
                                      'trustStorePassword=pass;'
                                      'principal=hive/hive.server3" -f '
                           + destinoprod + '/' + seleccion + '>&' + destinoprod + '/salida_' + seleccion + '.txt')
            # --- cierre de conexion
            c.close()

        if continuar_ejecucion == "no": #-- no se ejecuta pero si se pasa el fichero.
            print("El fichero se paso, pero no se ejecuto.\n"
                  "BYE")



# -------------- Funcion para ejecutar fichero en el servidor -------------------------

def ejecutar():
    print("Vamos a ejecutar el fichero: \n" + seleccion)
    respuesta = input(str("Quieres ejecutar el o los ficheros elegidos? (selecciona un numero):\n"
              "1) En Impala\n"
              "2) En Hive\n"
              "3) solo llevar fichero/s\n"))

    if respuesta == "1":
        impala() #-- se llama a la funcion impala
    if respuesta == "2":
        hive()  #--se llama a la funcion hive
    if respuesta == "3":
        print("No se ejecuta, pero si se pasa el fichero.\n"
              "BYE ")  #--  no se ejecuta nada.
        exit()

def seguir():
    resp = input(str("Ya se paso el fichero: " + seleccion + " y lo vamos a ejecutar.\n"
                                                             "Continuamos ?(si/no):\n"))
    if resp == "si":
        ejecutar() # llamamos a la funcion ejecutar, que llama a la funcion impala o a hive
    if resp == "no":
        print("No se ejecuta, pero si se pasa el fichero.\n") #-- se sale sin ejecutar nada
        exit()


#--------------------- El usuario elige con que entorno o servidor trabajar ---------------------------------
#---------------------- De acuerdo al servidor elegido, continua el Script ----------------------------------

print("\nVamos a definir con que entorno trabajar, y automaticamente se seleccionara\n"
      "  el directorio destino correspondiente\n")

#-- variable para elegir entorno
entorno = input(str("Selecciona el numero correspondiente del entorno con el cual vas a trabajar:\n"
                    "1) Desarrollo: " + serverdev + "\n"
                    "2) Cua: " + servercua + "\n"
                    "3) Producción: " + serverprod + "\n"))

if entorno == "1":
    print("Estamos trabajando con:\n"
      "el usuario: ", user + "\n"
      "el home: ", home + "\n"
      "el server: Desarrollo ==> ", serverdev + "\n" 
      "y el destino de desarrollo: ", destinodev + "\n")

if entorno == "2":
    print("Estamos trabajando con:\n"
          "el usuario: ", user + "\n"
          "el home: ", home + "\n"
          "el server: cua ==> ", servercua + "\n"
          "y el destino de cua: ",  destinocua + "\n")

if entorno == "3":
    print("Estamos trabajando con:\n"
          "el usuario: ", user + "\n"
          "el home: ", home + "\n"
          "el server: Produccion ==> ", serverprod + "\n"
          "y el destino de produccion: ",  destinoprod + "\n")



comenzar = str(input("Continuamos? (si/no):\n"))
# -- Comienzan las opciones para ejecucion del Script
if comenzar == 'si':
    # -- tupla para definir las extensiones de los ficheros a listar --
    ext = [".txt", ".sql", ".hql"]
    # -- se convierte tupla en lista --
    lista_dir = os.listdir(home)
    # --  bucle para indexar lista y elegir por numero --
    for index, item in enumerate(lista_dir):
        if item.endswith(tuple(ext)):
            print(index, item)

    # -- variable para guardar el fichero que nos vamos a llevar --
    file = input(str("Selecciona el numero de fichero que necesitas llevarte:\n"))


    # -- variable para guardar la busqueda del fichero elegido de la lista(antes tupla) --
    seleccion0 = lista_dir[int(file)]
    print("Seleccionaste el fichero: ", seleccion0)
    seleccion = ("'" + seleccion0 + "'")
    

    consulta = input(str("Continuamos? (si/no):\n"))

    if consulta == "si":
        print("Te llevas el fichero : ", seleccion)
        pasar_destino()
        ls_destino()
        seguir()
        # traer_salida()
        # ls_home()
    if consulta == "no":
        print("No has hecho nada.\n"
              "BYE")
        exit()


if comenzar == "no": # --  el script no sigue y no se hace nada.
    print("No has hecho nada.\n"
          "BYE")
    exit()

