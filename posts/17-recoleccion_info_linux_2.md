---
layout: post
title: "Recoleccion de Informacion en Linux"
date: 2022-02-21
categories: [Recoleccion]
tags: [linux, reconocimiento, enumeracion, recoleccion]
excerpt: "Segunda parte de recolección en Linux: profundizando en usuarios, procesos y configuraciones."
---


Bien, parece ser que nos acercamos al final del trayecto en la recopilación adicional de información una vez que tenemos acceso a una máquina dentro de una red/infraestructura. Esto no es el final del viaje, ni mucho menos; es más bien, y continuando con el símil ferroviario, un transbordo o un cambio de ejes de vía (el lector es libre de interpretar dicha similitud como le venga en gana). Ahora que nos estamos acercando al final, observamos por la ventanilla cómo es el destino hacia el que nos dirigimos, puesto que  ya hemos recopilado información suficiente y podemos hacernos una idea de qué nos espera. ¡¡¡Pero!!! Aún quedan unos flecos que cortar. Nos falta saber unos últimos detalles antes de que el tren de la recopilación se detenga. ¿Cómo saber exactamente que tareas se ejecutan (cuándo y qué ciclo tienen) en segundo plano, y si dichas tareas tienen permiso de escritura y por consiguiente, susceptibles a la creación de algún tipo de vulnerabilidad que nos ayude a escalar privilegios? Para esto último, debemos saber quienes son los creadores de dichas tareas programadas, y además, recabar información específica de los distintos software y sus versiones; para que un poquito más tarde, ya en el tren o tramo del mantenimiento y persistencia (estoy en plan ferroviario y no tengo la menor idea del por qué), explotar posibles vulnerabilidades de los mismos. Tras esta breve introducción, y permitan los lectores la licencia que me he tomado con  las similitudes, vamos con el objeto del artículo.



Trabajos y tareas



Lo primero que veremos será ver qué tareas se encuentran programadas para ejecutarse en segundo plano. Dichas tareas deben estar configuradas por ciclos temporales (determinadas por el usuario y que en Linux sólo puede root) y alojadas en algún archivo del sistema. Efectivamente y como hemos visto en artículos anteriores,  casi todo lo ejecutable en un equipo Linux se encuentra en el directorio /etc/ y en el caso que nos ocupa, en el directorio /etc/crontab. ¿Pero qué es cron exactamente? Cron es una herramienta, un administrador regular de procesos en segundo plano, el cual ejecutará los procesos en el ciclo temporal especificado en el archivo crontab. Dicho archivo incluye la variable PATH; lo que hace posible la ejecución de comandos en ubicaciones incluidas en la variable de entorno (PATH), sin especificar la ruta absoluta.



Listar tareas Cron:



Para listar las tareas cron, ejecutaremos los siguientes comandos:











Buscar tareas cron con permisos de escritura:



Es el momento de listar qué archivos regulares pueden ser editados o con permisos de escritura para usuarios de nivel bajo y que residan en el directorio /etc/cron:







Vemos que no se obtiene resultado alguno. Si observamos la captura superior,el permiso de escritura de los archivos sólo corresponde a root:







Buscar tareas cron por usuarios:



También es posible buscar las tareas por usuario. Una vez más, podemos constatar que si queremos o necesitamos modificar alguna tarea o trabajo regular, deberemos escalar privilegios. Estas comprobaciones nos vienen bien a la hora de filtrar vectores de ataque con vistas a la escalada de privilegios.







Información de las versiones  de los software instalados: 



Una vez visto los trabajos y tareas, es el momento de comprobar las versiones de las aplicaciones más comunes que se encuentran instaladas en la máquina vulnerada.



Comprobando las versiones bases de datos:







Comprobación de versión servidores HTTP:



Vemos que el servidor es Apache y su versión la 2.4.29 para Ubuntu



Comprobación de versión de Sudo:



A veces los comandos ,V y -v arroja error, una alternativa es ejecutar el comando completo --versión



Comprobación de las versiones de paquetes .deb mediante dpkg:



Para la comprobación de las versiones de todos los paquetes instalados .deb mediante dpkg, creo que antes deberíamos hacer una pequeña parada pára comprender que es dpkg y cuál es su diferencia con apt.



Éste es el gestor base de paquetes Debian e instala sólo los paquetes que se le ordena, literal. Y pensaremos, ¿cuál es la diferencia entre dpkg y apt? Pues copio literalmente la diferencia desde la página de Debian. \"Se debe ver a dpkg como una herramienta de sistema (tras bambalinas) y apt como una herramienta más cerca del usuario que evita las limitaciones del primero. Estas herramientas trabajan juntas, cada una con sus particularidades, adecuadas para tareas específicas.\" .



Cuando he dicho que el gestor dpkg es literal, no es broma. A diferencia de apt, que crea una lista de dependencias para automatizar las instalaciones al máximo, dpkg, tan solo instalará lo que se le marque, sin tener en cuenta si existe o no dependencias necesarias para su correcta y total instalación.



Para ver la versión de los paquetes instalados debemos ejecutar el siguiente comando:



A diferéncia de los comandos anteriores, usaremos el comando -l



Hasta aquí los pequeños artículos correspondientes a la recolección adicional de información en un sistema vulnerado, ya sea en remoto como el caso en estos artículos o como en local, los comandos son los mísmos.



Espero que les haya gustado.



Un saludo y Happy Hack!!



REFERENCIAS:



https://blog.desdelinux.net/cron-crontab-explicados/



https://voragine.net/linux/crontab-usuarios-sistema-tareas-periodicas-cron-linux



https://rootsudo.wordpress.com/2014/04/06/el-path-la-ruta-de-linux-variables-de-entorno/



https://blog.infranetworking.com/tipos-de-servidores-web/



https://wiki.debian.org/es/dpkg




','Post-Explotación: Recolección adicional información. (Parte 5: Trabajos, tareas e información del software)','