---
layout: post
title: "Enumeracion de los servicios"
date: 2022-01-22
categories: [Recoleccion]
tags: [enumeracion, reconocimiento, servicios, metodologia]
excerpt: "Enumeración de servicios: metodología y herramientas para mapear la superficie de ataque."
---


La enumeración remota de un objetivo es el proceso de recopilar el maximo de información de este a través de la red usando para ello todas las herramientas que se encuentren a nuestra disposición.



Siempre debemos tener en mente, que el proceso de recolección y enumeración de objetivos es la fase mas importante del test de penetración. Existen algunas frases que representan muy bien este proceso, tales como “Si tengo ocho horas para talar un árbol, afilare mi hacha durante las siete primeras” , “La información es poder” o “Si miras cualquier tipo de organización moderna y piensas ‘¿Cuál es el instrumento de poder más potente?’, verás que es la información”, desde estas perspectivas debemos observar el proceso de recolección de información. A modo personal me quedo con una cita de Einstein “Saber dónde encontrar la información y cómo usarla. Ese es el secreto del éxito” , esto es lo que veremos en este artículo, saber buscar información y como usarla para poder en posteriores fases del Pentest, hacer uso de ella.



Mantendremos un esquema metodológico en esta fase tan crucial, escaneo de puertos, servicios operativos y versiones de estos, sistemas operativos, recursos, rutas, etc….



Como ejemplo pondremos un sistema Linux vulnerable (metasploit2)



 Sistemas Operativos y puertos:







El escaneo de puertos tambien puede servir para determinar que sistema operativo esta detrás. Por ejemplo, el puerto TCP 111/rcpbind y el puerto TCP 2049/nfs fueron identificados, lo que nos hace pensar en un host Linux, ya que rara vez esos puertos se encuentran corriendo en sistemas Windows. Sin embargo, Siempre debemos tener en mente, que quizás esos servicios fueron  puestos alli para deshacerse de un atacante, aquí es donde entran en juego los HoneyPots; servicios que basados en un sistema para hacerse pasar por otro y viceversa. Por eso es tan importante la enumeración y la vuelta a la enumeración.







Volviendo a la enumeración, se debe escanear los puertos tanto TCP como UDP incluyendo la versión de estos. Los escaneos sobre los puertos UDP son bastante más lentos y el Pentester se llega a desesperar por momentos.







Tras la espera vemos los servicios y las versiones de estos, esto nos ayudara a ser mas precisos en el momento del futuro ataque.



Vamos a centrarnos en recoger información o “frutos de rama baja”, dicha referencia al nombre es bastante acertada, puesto que como veremos, se puede recoger información de forma bastante sencilla. Para ello usaremos el servicio NFS (Network File System), un protocolo para compartir archivos que se suele encontrar en sistemas UNIX. Por lo general, suelen correr de manera predeterminada sobre el puerto TCP/UDP 2049.







Observamos que se encuentran abiertos, antes de continuar debemos saber que este servicio comparte y depende de otros servicios como por ejemplo “mountd” y que suele correr sobre el puerto TCP/UDP 111, es por ello por lo que recabaremos un poco más de información al respecto.



Directorios:



Si un administrador desea compartir archivos desde un NFS, el servidor configurará estos directorios como “exportaciones” y hará posible su visibilidad para otros usuarios de la red.



Estos archivos, generalmente se encuentran en la ruta …/etc/exports en un hosts local. Sin embargo, el error más común que sufren este tipo de servicios es el HUMANO, malas configuraciones, como permitir la conexión o ejecucion de los directorios sin ningún tipo de autenticación o filtrado, o en casos muy extremos, con permisos de escritura de estos, hacen peligrar toda la red.



Volviendo al escaneo, una vez identificado que el servicio se encuentra corriendo, lo primero que haremos será realizar una consulta con algunos scripts específicos para este servicio:







Ejecutamos los scripts en un solo comando y observamos la información devuelta por los mismos:







Como hemos recalcado, no basta con una sola enumeración para determinar si la información obtenida es la correcta, o la más completa. Como vemos, ante la duda que dos scripts arrojasen error, optamos por la ejecucion individual de los mismos, obteniendo otro resultado distinto al inicial.











Otra opcion es montar el directorio en local desde nuestra consola de comandos, pero veremos que no arrojara más información que la obtenida con nmap:







PORTMAPPER (AKA rcpbind)



Es otro de los servicios que nos podemos encontrar en sistemas basados en LINUX, básicamente es usado para mapear servicios RPC (Open Network Computing Remote Procedure Call o “ONC RPC” y no debemos confundirlo con la implementación de windows RPC).



Este servicio ofrece información sobre los puertos que estan a la escucha en la máquina, pero&nbsp; quizás no sea accesible sobre la red. Por ejemplo, un sistema de destino puede estar ejecutando un&nbsp; servicio RPC personalizado al que solo se puede acceder mediante un host local o puede estar ejecutando &nbsp;NFS, pero solo para un segmento de red o red local.



Conocer este modo de funcionar puede darnos más información sobre qué servicios locales pueden estar ejecutándose en el objetivo y ayudarnos a explotar mas un sistema, ahora bien, este tipo de recolección se debe realizar cuando se ha obtenido una explotación local.



Por lo general portmapper corre sobre los puertos TCP/UDP 111 y en algunos casos sobre el 32771, se puede enumerar mediante script de nmap o usando el comando “rpcinfo” desde consola.



Al realizar una consulta contra el puerto 111, se enumerarán todos los puertos relacionados con el servicio que corre en dicho puerto, sin necesidad escanear dichos puertos individualmente. Además, nos arrojara información de que puertos es sistema tiene abierto localmente (vinculados al host local), que normalmente no se enumerarían o mostrarían en un escaneo normal.







Ejecucion por consola:







&nbsp;SAMBA



Samba, es una implementación de protocolos SMB/CIFS basado en Linux, proporciona servicios de impresión y uso compartido de archivos para cliente windows, las versiones mas recientes tambien se pueden integrar en dominios active Directory.



Samba puede proporcionarnos gran cantidad de información cuando se enumeran correctamente, dependiendo de la configuración podemos encontrar información sobre el S.O, usuario, dominio, cuentas, recursos compartidos, permisos o datos sensibles a un ataque. Los servidores samba configurados incorrectamente tambien pueden provocar errores de ejecucion remota.







Vamos a profundizar un poco más con la información obtenida; hacemos uso de otro script para enumerar directorios.











Podemos hacernos a la idea de los directorios disponibles en el objetivo.



Ahora conectamos con el servidor vía consola, sabemos que permite el logeo anónimo asi que basta con introducir el comando y presionar “enter”, en el pass podemos poner cualquier carácter que queramos.







Haciendo uso de la herramienta smbmap podemos ver los permisos de los directorios







Realizando este tipo de consultas podemos ir filtrando directorios para la posterior explotación, como podemos ver solo permite acceso y escritura en el directorio tmp/



Ahora que tenemos un directorio que se encuentra compartido y accesible, vamos a volver a conectar, pero esta vez solicitando el acceso directo a dicho directorio, para ello introducimos el siguiente comando, los 4 slash invertidos de usan antes de la introducción de la IP y los 2 slash siguientes para el directorio.







Ahora tenemos a nuestra disposición varias opciones para poder continuar con nuestra explotación, pero este no es el caso del tema. Podemos ver las opciones disponibles tecleando “help” desde nuestro prompt.







Usuarios:



Ahora que ya hemos enumerado los directorios, podemos enumerar usuarios usando el protocolo SMB. La enumeración puede resultar a veces un poco complicada, comencemos usando el método “rpcclient”, es una buena herramienta para automatizar la búsqueda de información basado en protocolos SMB, tanto en sistemas LINUX como Windows.



Método manual:



El método que vamos a ver es un ataque por librería, usando como parámetros posibles usuarios.



Primero creamos el archivo txt con los usuarios:







Seguidamente introducimos el script en consola.







Una vez pulsemos “enter” nos aparecerá los usuarios encontrados.







Vemos el funcionamiento del script







Método automatizado 



enum4linux



Es una herramienta ya implementada en Kali y puede enumerar servidores SMB, detalla de manera muy rápida un objetivo, ofreciendo información de logeo, usuarios, dominio….















































Podemos ver el potencial de la herramienta.



ENUMERACION DE CORREOS:



En este apartado, enumeraremos los servicios SMTP y que opciones se encuentran permitidas en estos. Palabras como “HELO”, “RCPT” o “MAIL” nos es de sobra conocidos y seguramente, tambien hemos usado el servicio TELNET (telnet mail.server.site 25)para el envio de algun correo.



Aunque la información es de aplicación para los S.O (Windows o Linux), la mayoría d los servidores de mail estan basados en Linux, pero las técnicas son validas para servidores con arquitectura diferente.



Vamos a usar un script disponible en nmap. Primero comprobar siempre sobre que puerto se encuentra corriendo el servicio (en este caso el 25)











Tambien podemos obtener información usando netcat:







O telnet:







En ambos casos nos responde que el servidor se encuentra activo y listo para recibir.



Usando smtp-user-enum:



Poderosa herramienta creada por pentestmonkey, que sirve para la enumeración de procesos SMTP en un objetivo, creando un&nbsp; diccionario con posibles usuarios, nos ayudara a la hora de obtener información sobre el servicio.



Creamos el diccionario:







Vemos las opciones de uso:







Enviamos una solicitud de verificacion y observamos los resultados:







Vemos que en cinco segundos ha realizado la consulta y obtenido los resultados, esto agiliza mucho el proceso de obtención de usuarios.



Como siempre recordar que existen varias tecnicas y herramientas para conseguir los mismos (y seguramente) mejores resultados, la pericia del pentester, el tiempo, la conexion y el entorno a recopilar informacion marcara en gran medida que tecnicas usar.



Espero que os haya gustado el articulo.







Happy hack!!!











Referencias:







https://en.wikipedia.org/wiki/Server_Message_Block



https://github.com/ShawnDEvans/smbmap




https://pentestmonkey.net/tools/user-enumeration/smtp-user-enum




https://github.com/insidetrust/statistically-likely-usernames



https://cr.yp.to/smtp/mail.html



https://cr.yp.to/smtp/vrfy.html
','Recolección de Información remota de un Objetivo','