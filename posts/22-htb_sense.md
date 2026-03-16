---
layout: post
title: "HTB:Sense"
date: 2024-02-13
categories: [HTB]
tags: [htb, freebsd, easy, pfsense, web]
difficulty: Easy
excerpt: "Walkthrough de HTB Sense: explotación de pfSense vulnerable en sistema FreeBSD."
---


Recolección de información:



        Comencemos realizando un mapeo del sitio.







        Con wappalyzer obtenemos un poco más de información, como las librerías  JS y el lenguaje de programación PHP.







        Usemos dirbuster para encontrar directorios ocultos. Por suerte encontramos dos, /changelog.txt y system-users.txt. Veamos que contienen.











        Bueno!! Aquí hay oro. En el archivo system-users.txt encontramos el nombre de usuario y la credencial por defecto, ni más ni menos.











        El archivo changelog.txt nos dice que la versión instalada a sido actualizada.







Análisis de vulnerabilidades:



        Introducimos las credenciales y nos devuelve error? Tras unas pruebas dimos con la tecla del asunto: el usuario es el minúscula.











        Podemos ver la versión instalada dentro del cuadro de información del sistema.







Explotación:



        Una breve (por una vez) búsqueda con searchsploit nos arroja el exploit que buscábamos.







          Configuramos el exploit tal como nos indica el mismo.







        Una vez lanzado obtenemos nuestra shell, para sorpresa con id root, tan solo resta buscar las flags.







Happy Hacking!!
','Sense','