---
layout: post
title: "HTB: Bank"
date: 2024-03-10
categories: [HTB]
tags: [htb, linux, easy, web, upload]
difficulty: Easy
excerpt: "Walkthrough de HTB Bank: enumeración web, bypass de restricciones y escalada de privilegios."
---


Recolección de información:



        Lancemos Nmap para hacernos una vista general de la máquina.







Introduzcamos los comandos -sC (scripts por defecto) y -sV (Detección de Versión) para ampliar la información.







Puerto 22: SSH



       \"SSH&nbsp;(o&nbsp;Secure&nbsp;SHell) es el nombre de un&nbsp;protocolo&nbsp;y del&nbsp;programa&nbsp;que lo implementa cuya principal función es el&nbsp;acceso remoto&nbsp;a un servidor por medio de un canal seguro en el que toda la información está cifrada. Además de la conexión a otros dispositivos, SSH permite copiar datos de forma segura (tanto archivos sueltos como simular sesiones&nbsp;FTP&nbsp;cifradas), gestionar&nbsp;claves RSA&nbsp;para no escribir contraseñas al conectar a los dispositivos y pasar los datos de cualquier otra aplicación por un canal seguro&nbsp;tunelizado&nbsp;mediante SSH y también puede redirigir el tráfico del (Sistema de Ventanas X) para poder ejecutar programas gráficos remotamente. El puerto TCP asignado es el 22\"







      Podemos ver que se encuentra encriptado y no tenemos aún suficiente información del objetivo. Luego regresaremos.







Puerto 53: DNS



        Veamos que nos muestra el puerto 53. El mapeo devuelto por Nmap nos indica lo siguiente \"ISC BIND 9.9.5-3ubuntu0.14 (Ubuntu Linux)\", veamos de que  se trata. 







\"El dominio de nombres de Internet de Berkeley (BIND o Berkeley Internet Name Domain) implementa un dominio de Internet nombre del servidor. BIND es el software de servidor de nombres más utilizado en el mundo. Internet, y cuenta con el respaldo del Internet Software Consortium, www.isc.org.\"



\"Los Sistemas de Nombres de Dominio (DNS o Domain Name Systems) son la guía telefónica de Internet. Los humanos acceden a la información en línea a través de nombres de dominio, como nytimes.com o espn.com. Los navegadores web interactúan a través de direcciones de Protocolo de Internet (IP). DNS traduce los nombres de dominio a direcciones IP para que los navegadores puedan cargar recursos de Internet.\"



        Intentemos recolectar la información necesaria sobre este dominio mediante las herramientas \"dig\". Podemos ver que obtenemos nuevos nombres que debemos añadir los nombres al archivo /etc/hosts/ .







        Como siempre es bueno intentar distintos métodos, encontramos que con dnsrecon obtenemos una salida interesante. \"DNSSEC no esta configurado\"... Interesante.







        Añadimos el dominio y los subdominios al archivo /etc/hosts..







         Comprobemos si resuelve los nombres DNS. Al  poner solamente la IP tomará de forma predeterminada el puerto 80, con lo cual, podríamos decir que acabamos de enlazar de forma automática con la recolección de información del siguiente puerto abierto.



PUERTO 80: HTTP



        Bank.htb nos redireciona directamente al login.php. Esto nos recuerda que deberemos fuzzear un poco más adelante.







En ns.bank.htb tenemos la página principal de Ubuntu corriendo.







wwww.bank.htb nos muestra la misma pagina.







Y lo mismo pasa con chris.bank.htb







        Al encontrar el directorio login.php disponible, debemos de echar un ojo, no vaya a ser que dejemos otros ocultos. Para ello usaremos alguna herramienta que automatice la búsqueda. En este caso gobuster y observamos que obtenemos directorios nuevos.







        Sigamos el nuevo rastro a ver que podemos encontrar...



Analisis de Vulnerabilidades:



        Usamos nuestro Burp para realizar reenvío de los directorios encontrados. Todas salvo /header.php devuelve 200.



















        El resto de directorios no nos dice nada y nos encontramos un poco perdidos, así que volvemos a realizar nuevas búsquedas de directorios.







        Nos dirigimos al nuevo directorio y observamos lo que parece un registro. Abrimos el primero y vemos que los datos están encriptados. Bien, si ordenamos por tamaño hay uno que destaca, esto se debe a que no esta encriptado. 











Bien!! Tenemos nuestras primeras credenciales, a guardar se ha dicho.







Con nuestro archivo guardado para futuros usos vamos a logearnos a ver que obtenemos







En Support encontramos un formulario, sobre el cual intentaremos lograr nuestra primera intrusión.







        Sabiendo los puertos, servicios y versiones llegamos al momento de encontrar los vectores de ataque que nos indiquen como será la futura explotación del objetivo.



Explotación:



Descargamos una shell en php, la configuramos  y la cargamos en el objetivo.



















Oopps!!! Eso digo yo. Tenemos que incrustar la shell en una imagen para que sea cargada.















         De nuevo sin conexión, sigamos buscando. Encontramos información donde dice que la extensión debe contener la doble extensión .php.png. Probemos.







También comprobamos los metadatos de la imagen.















        Nuevamente perdido, me lleva unos minutos comprender que quizás sea más sencillo. Qué tal si ponemos el script en el cajón del mensaje directamente?







El netcat no recibe nada.....Tenemos un problema. Veamos el código fuente a ver si se nos escapa algo. Efectivamente encontramos un mensaje el cual dice que \"por motivos de depuracion la extension.htb se añade como php\"







Pues volvamos a probar cambiando la extension del script







Bien!!! Tenemos acceso, pero antes de nada mejoremos nuestra shell.











Comenzamos a husmear y rápidamente obtenemos la flag user.txt.







Intentamos ir al directorio root pero tenemos permiso denegado....Había que intentarlo







Escalada de privilegios:



        Vamos a comprobar si existen archivos de los que podamos hacer uso con nuestro usuario sobre archivos con permisos de usuarios elevados.







Crucemos dedos!!







BINGO!!!! Tenemos la flag de root.







Happy Hacking!!



Referencias:



https://nmap.org/book/man-version-detection.html



https://es.wikipedia.org/wiki/Secure_Shell



https://goteleport.com/blog/comparing-ssh-keys/



https://book.hacktricks.xyz/network-services-pentesting/pentesting-dns



https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php



https://gist.github.com/ElenaMLopez/88c37c58a0c9ff7242a77c9a8eaea553
','BANK','