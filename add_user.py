import os
print("Scrip para agregar un usuario sftp\n")
print("Con este Script, vas a modificar un fichero del sistema(ojo!).\n")
print("vas a agregar al final del fichero sftp_config un usuario con el siguiente formato:\n")
print("<User nuevo_usuario>\n"
      "        Home    /home/del/usuario\n"
      "</User>\n")

######### Funcion para agregar Usuario al fichero sftp_config ############
def datos_usuario():
    user_nuevo = str(input("ingresa el nuevo usuario: "))
    home = str(input("ingresa home del usuario nuevo: "))
    print("lo que vas a agregar es esto al final del fichero:\n" + "<user " + user_nuevo +">\n" + "        Home    " + home + "\n</user>")
    continuar = str(input("Estas de acuerdo?: si o no:\n "))
    if continuar == "si":
        file = open("/etc/ssh/sftp_config", "a") # Abro para escritura al final
        file.write("\n<User "+ user_nuevo + "> \n        Home    " + home + "\n</User>\n" ) # agrego al final
        file.close() # Cierro
        print ("las ultimas lineas del fichero ha quedado así:\n")
        os.system('tail' + " /etc/ssh/sftp_config") #para ver como quedo el fichero
    elif continuar == "no":
        print("comenzamos de nuevo:")
        salir = str(input("Quieres agregar de nuevo el usuario?: si o no:\n"))
        if salir == "si":
            DatosUsuario()
        elif salir == "no":
            print("lo volvemos a intertar luego. ")
            exit()

continuamos = str(input("continuamos?(si/no):\n"))
if continuamos == "si":
    datos_usuario()





