---
layout: post
title: "Powershell-Empire"
date: 2021-05-31
categories: [Pentest]
tags: [powershell, empire, c2, windows, red-team]
excerpt: "Uso de PowerShell Empire como framework de Command & Control en entornos Windows."
---


Hoy os traigo un framework mas que conocido en el mundo del pentesting, una de esas \"navajas suizas\" que todo Pentester debe conocer y poseer en su bolsa de trabajo.







Pero antes de entrar en la prueba de concepto, veamos de que trata este framework y como puede ser de gran utilidad en la fase de post explotacion.



Un poco de Historia:



&nbsp;Se trata de un framework&nbsp;post-explotación, nacida de la unión de dos proyectos Powershell Empire y Python Empire, siendo lanzados en 2015 y 2016 respectivamente. Framework centrado en Python, pronto paso a ser la referencia en la fase para el que fue creado, pero las continuas actualizaciones de los sistemas operativos, y las limitaciones de software (python2.X) hicieron predecir el final del proyecto.



Durante la edición 27 de Defcon BC-Security anunció que continuaría el desarrollo haciendo un fork del proyecto, incorporando funcionalidades de bypass de AMSI y posteriormente reparando funcionalidades que iban dejando de estar operativas por actualizaciones en los sistemas operativos modernos. El siguiente gran paso fue la migración de los componentes de server a Python 3. Ha dia de hoy el proyecto se encuentra Archivado y su repositorio esta disponible en modo lectura en su Hithub.







Ahora bien, si nos encontramos frente a una herramienta archivada, por que hablo hablo de ella en esta entrada? La respuesta es la siguiente, la versión de Powershell-Empire se encuentra disponible para Kali-Linux. Aqui os dejo el enlace donde se habla de lo expuesto aqui amteriormente, asi como los pasos para la instalacion de esta fantastica herramienta en nuestros equipos.



 https://www.kali.org/blog/empire-starkiller/



Como funciona Powershell-Empire:



Consta de 3 componentes que debemos configurar previamente siguiendo el siguiente orden:



1º configurar el Listener:  Se encarga de esperar las conexiones de los agentes y sera a traves de este donde el Pentester se comunicara con la maquina objetivo.



2º configurar el Stager: Se trata del código generado y que una vez ejecutado en la maquina comprometida se convertirá en Agent.



3º configurar el Agent: Son el stager ejecutándose en la maquina, estos portaran los módulos a ejecutar por el Pentester.



Prueba de concepto:



Bien ahora si que vamos a entrar en materia, para ello comenzamos por levantar el servidor Apache de nuestro Kali:







Ya con el servidor arriba, procedemos a lanzar el framework:











Como se puede observar, tras la carga inicial, se nos muestra información sobre la cantidad de opciones disponibles activos, bien, lo primero que debemos hacer lógicamente es tener una maquina, nosotros ya tenemos nuestra sesion de meterpreter en una maquina con windows 10, asi que primero cargaremos el modulo de powershell para poder lanzar mas adelante la orden de cargar y ejecutar nuestro agente.











Regresamos a Empire y entramos en harina, usamos un listener, existen varios, pero nosotros nos hemos decantado por el de http, para ello tecleamos 'uselistener http' e 'info' para poder visualizar las opciones de configuracion. 











Como podemos ver, Empire funciona muy similar a metasploit, asi que no se nos debe de hacer muy dificil su uso. Una vez configurado los parametros, ejecutamos con el comando 'execute' lo que nos arrojara un mensaje de ejecucion correcta, volvemos con 'back' y listamos con 'listeners'. Observamos que el listener se encuentra activo:







Ahora le toca el turno al stager, vamos a crear un archivo.bat , este archivo creara una ventana de powershell no interactiva, el codigo cargado creara la conexion en busca de nuestro listener, una vez encontrado tendremos el agente listo par funcionar. Su carga no es inmediata, puesto que debemos esperar a que el listener prepare las ordenes mientras el agente realiza conexiones no continuas. 



solicitamos usar el stager mediante la orden usestager mas el stager que queremos usar, en nuestro caso 'usestager windows/launcher_bat', en la opcion Listener debemos introducir el nombre del listener activo y una vez configurado los parámetros ejecutamos con 'execute'. Recibimos el aviso de creación y la ruta de guardado:







Movemos nuestro archivo a la ruta de archivo compartido de nuestro apache:











Es el momento de regresar a nuestra sesión de meterpreter y lanzamos la orden de descarga y ejecución del archivo. Como hemos dicho anteriormente, debemos esperar a que la conexión y preparación se realice, es el caso de la imagen izquierda







comprobamos que nuestro agente se encuentra cargado y activo, con el comando 'agents' es importante visualizarlo, porque necesitamos el nombre del mismo en el ultimo paso:







Ahora solo nos queda configurar nuestro modulo, para ello usaremos el comando 'usemodule powershell/trollsploitmessage' :







Seteamos los parámetros que necesitemos y ponemos lo que queramos que aparezca en pantalla de la victima:











si todo a marchado correctamente, podemos ver que aparece la ventana de PowerShell con el aviso que hemos escrito.



Pues esto es todo, os dejo referencias para mas info:



https://www.kali.org/blog/empire-starkiller/



https://www.elladodelmal.com/2016/02/powershell-empire-post-explotacion-en.html




https://ethicalhackingguru.com/how-to-use-powershell-empire-3-the-powershell-empire-3-tutorial/




Espero que este articulo os haya gustado.



Un Saludo y Happy Hacking!!
