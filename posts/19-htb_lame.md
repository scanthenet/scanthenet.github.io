---
layout: post
title: "HTB:lame"
date: 2024-01-20
categories: [HTB]
tags: [htb, linux, easy, samba, metasploit]
difficulty: Easy
excerpt: "Walkthrough de HTB Lame: explotación de Samba vulnerable con Metasploit en máquina Linux easy."
---


Introducción:



        Lame fue lanzada en 2017. Se trata de una máquina con S.O. Linux y con servicios FTP, SSH y SAMBA corriendo.  



Enumeración:



        Comencemos por una enumeración de la máquina con el fin de descubrir tanto los servicios que corren como las versiones de los mismos (-sV), además de ejecutar los scripts más comunes sobre los mismos (-sC). 







FTP:



        El primer servicio es FTP versión vsftpd 2.3.4. La definición del mismo viene a ser algo como:



\"El Protocolo de transferencia de archivos (en inglés File Transfer Protocol o FTP) es un protocolo de red para la transferencia de archivos entre sistemas conectados a una red TCP (Transmission Control Protocol), basado en la arquitectura cliente-servidor. Desde un equipo cliente se puede conectar a un servidor para descargar archivos desde él o para enviarle archivos, independientemente del sistema operativo utilizado en cada equipo\" .



        Este servicio es vulnerable en gran parte porque se le dio más importancia a la velocidad que a la seguridad a la hora de transferir los datos, por lo que tanto el login y el password como los datos enviados van en texto plano, siendo fácilmente usados o vulnerados con un capturador de tráfico.



        En el caso de Lame, sin embargo, no es necesario puesto que tenemos logeo Anónimo disponible. Inicialmente pensamos \"Bien.....tenemos acceso y varias posibilidades de trabajo\".















SAMBA:



        El siguiente servicio es SAMBA. Este es el equivalente al smb de Windows pero para Linux. Veamos su definición:



\"Samba es una suite de aplicaciones Unix que habla el protocolo SMB (Server Message Block). Los sistemas operativos Microsoft Windows y OS/2 utilizan SMB para compartir por red archivos e impresoras y para realizar tareas asociadas. Gracias al soporte de este protocolo, Samba permite a las máquinas Unix entrar en el juego, comunicándose con el mismo protocolo de red que Microsoft Windows y aparecer como otro sistema Windows en la red (desde la perspectiva de un cliente Windows).\"



En este caso usaremos enum4linux por ser una herramienta que simplifica mucho el trabajo de recolección de información sobre dicho servicio.



https://github.com/cddmp/enum4linux-ng/blob/master/enum4linux-ng.py



https://github.com/CiscoCXSecurity/enum4linux/blob/master/enum4linux.pl











        La enumeración de directorios compartidos nos indica que tan solo el directorio tmp se encuentra disponible completamente. Ademas, la captura inferior a ésta indica que el user/pass en blanco también se ha realizado con éxito. 











        Tampoco está de más comprobar el acceso mediante smbclient. Ésta herramienta permite la conexión remota desde linea de comandos, para más info:



https://www.samba.org/samba/docs/current/man-html/smbclient.1.html











ANALISIS DE VULNERABILIDADES:



        Bueno, pues llegamos al momento de buscar los ataques correctos a los vectores de ataque perfilados. Lo mejor es ser metódicos con el orden y por ello comenzamos con el protocolo FTP que corre por el puerto 21. Usa simple búsqueda por la red y nos arroja los resultados.







        También es bueno comprobar si en searchploit nos arroja la misma información....Siempre es bueno cotejar la información obtenida por distintas fuentes. 























EXPLOTACIÓN:



        Probamos con el backdoor existente en la versión vsftpd 2.3.4, la cual no tiene éxito debido a que nuestra máquina víctima no dispone del puerto 6200/TCP a la escucha.  Esto me pasa por no leer las descripciones de las vulnerabilidades aunque se trate de una línea......











Efectivamente, el escaneo completo de puertos nos corrobora las sospechas.







        Pasemos al siguiente protocolo nuestro vecino y amigo SAMBA. Este protocolo corre tanto por el puerto 139 como el 445. A modo explicación decir que tanto el puerto 139 como 445 usa el Protocolo de Control de Transmisión (TPC). TCP es uno de los protocolos principales en redes TCP/IP. TCP es un protocolo orientado en la conexión, necesita el apretón de manos (Handshake) para determinar comunicaciones de principio a fin. Sólo cuando la conexión es determinada, los datos del usuario pueden ser mandados de modo bidireccional por la conexión. ¡Atención! 139 y 445 garantiza la entrega de paquetes de datos en el misma orden en que fueron mandados. La comunicación garantizada por los puertos TCP 139 y 445 es la diferencia mayor entre TCP y UDP.



        La diferencia entre ambos puertos radica en el uso de NetBIOS, el 139 hace uso de dicho tráfico mientras que el 445 no. Ambos hospedan NBSession.



        Nuevamente volvemos a encontrar información en la red; la búsqueda inicial en searchploit me puso sobre la pista necesaria!! Así que copiamos el script y lo pegamos en un documento con extensión .py 







https://github.com/amriunix/CVE-2007-2447/blob/master/usermap_script.py







Importante dar los privilegios de ejecución al script con chmod +x usermap_script.py. 







Recordamos poner nuestro listener a la escucha.







!!YA tenemos acceso y root para más INRI!!. Solamente nos resta encontrar las flags.



Con el siguiente comando obtenemos una shell interactiva:



python -c 'import pty; pty.spawn(\"/bin/sh\")'











Happy Hacking!!



REFERENCIAS:



https://es.wikipedia.org/wiki/Protocolo_de_transferencia_de_archivos



https://www.incibe.es/incibe-cert/alerta-temprana/vulnerabilidades/cve-2011-2523



https://learn.microsoft.com/es-es/troubleshoot/windows-server/networking/direct-hosting-of-smb-over-tcpip#more-information



https://www.incibe.es/incibe-cert/alerta-temprana/vulnerabilidades/cve-2007-2447
','Lame','