---
layout: post
title: "Reversing:RELRO"
date: 2021-12-29
categories: [Reversing]
tags: [reversing, relro, got, exploitdev]
excerpt: "RELRO (Relocation Read-Only): protección de la GOT y técnicas de bypass."
---


Introducción:



Entre las contramedidas de las que dispone Linux para fortalecer sus binarios (ELF), se encuentra la que veremos a continuación, comúnmente llamada RELRO (RELocation Read Only). Para la ejecución de esta prueba de concepto usaremos un sistema operativo Ubuntu 18 de 64 bits sobre el cual crearemos nuestro binario vulnerable de 32 bits. Como viene siendo habitual, primero veremos en qué consiste.



Historia y funcionamiento:



En 2004 Jakup Jelinek de RedHat, introdujo una nueva técnica conocida como RELRO. Esta técnica de mitigación o contramedida fue implementada para fortalecer las secciones de datos de los binarios ELF y consistía en la reordenación de las secciones internas de los mismos. Estando presente en el binario, el intento de desbordamiento por sobreescritura de la tabla de compensación global (GOT) no es posible puesto que dicha tabla se remapea a modo “solo lectura”, evitando las cadenas de formato de cuatro bytes. Hoy en día, RELRO es una característica estándar del compilador GCC y puede ser usado de 2 formas diferentes: RELRO parcial (-z relro) y RELRO completo (-z relro -z now).



¡Ahora toca jugar un poco!



1)  Creación del binario:







El programa hace uso de los argumentos de la línea de comandos. Cogerá el primer argumento y lo salvará en memoria; como una dirección (dónde escribir). A continuación, el segundo argumento es copiado en esa dirección (qué escribir). Podemos ver como en strncpy no hay posibilidad de realizar un desbordamiento puesto que utiliza una longitud fuerte como un argumento. Esto previene al usuario frente a escrituras de datos más largos que cuatro bytes.



2) Compilación y comprobación de las contramedidas:







A la hora de compilar tendremos en cuenta lo siguiente: tras la invocación del compilador mostramos el tipo de arquitectura con el comando -m32 , seguidamente introducimos la opción de depurador con el comando -g y por último, introducimos el comando de -no-pie que con ello impedimos la introducción de ejecutable independiente de posición (PIE, es como el ASLR, pero para binarios ELF).



Hacemos uso de la herramienta checksec para ver las contramedidas. Podemos observar cómo RELRO se encuentra en parcial. De otra manera, no podríamos llevar a cabo la explotación que da lugar a esta prueba de concepto.



3) &nbsp;Preparando el entorno



Antes de ejecutar nuestro binario por primera vez, debemos de realizar unas comprobaciones: la primera es asegurarnos que el ASLR tiene el valor cero y la segunda, solicitar información sobre el espacio del fichero core. Si el resultado resultase 0, debemos ejecutar ulimit -c unlimited y volver a comprobar si el espacio en dicho archivo ha cambiado y tiene valor unlimited.







4) Ejecución del binario



Ejecutamos el binario desde nuestra línea de comandos y añadimos dos cadenas de cuatro bytes. Vemos como efectivamente se produce en primer lugar la creación de la dirección y, en segundo lugar,  la copia de la segunda cadena en la dirección recién creada. Esto nos dará una violación del segmento, lo cual no nos debe de sorprender puesto que estamos intentando copiar algo en una dirección que realmente no existe.







5) &nbsp;Analizando el comportamiento



Vamos a analizar el código fuente. Solicitamos información de las funciones disponibles y hacemos uso de la función strncpy para crear un punto de ruptura.







Hacemos correr el binario con las dos cadenas; las cuales, se tratan de AAAA y BBBB. En un primer momento podemos observar cómo se le asigna una dirección a la primera cadena.







Pero si hacemos uso del comando C, vemos que el binario vuelve a realizar el proceso de ejecución asignando esta vez a la cadena B la dirección de la cadena A. Además, la primera cadena pasa al acumulador EAX y la segunda cadena queda registrada en EDX, puesto que en el acumulador no hay espacio.







Ahora bien, si procedemos a pulsar nuevamente sobre C el programa nos indicará una violación del segmento. Si observamos los registros podemos ver como en EAX continúa la cadena A y en EDX la cadena B, pero ambas cadenas han pasado a los punteros para funciones que requieren un origen y un destino estos son ESI y EDI.







También podemos pedir que nos muestre las 8 últimas palabras que tiene el registro ESP. Vemos que efectivamente se encuentran las dos cadenas: la primera con la cadena A y la segunda, cadena B, en un registro de memoria.







Es en este momento cuando podemos comenzar con la sobre escritura del binario.



6) Buscando el desbordamiento:



Primeramente, desensamblamos la función principal con el comando disas main. Podemos observar la función printf() después de la función vulnerable strncpy, y que dicha función se encuentra en un registro de memoria.







Procedemos a comprobar dicho registro mediante el uso del comando vmmap, el cual nos mostrará la longitud, los permisos y la ruta donde se encuentra. Determinamos que el programa está llamando a una función en la localización que acabamos de introducir y que se encuentra en PLT; además los permisos son solo de lectura y ejecución, por lo tanto, no podemos escribir en dicha localización.







Pedimos que nos muestre las 10 primeras líneas del registro que estamos investigando, vemos que se tratade un stub de función y que la primera instrucción es la ejecucion de un salto hacia otra localización que se encuentra el PTR, vamos entonces a investigar esta nueva dirección.







Solicitamos la información que necesitamos nuevamente con vmmap  y esta vez el resultado es el deseado, la localización si tiene permiso de escritura.







Vamos a ver los encabezados de las secciones del binario y si los puntos GOT y GOT.PLT tienen permisos de escritura. Para ello, desde la consola principal, ejecutamos el comando readelf -S ./poc_relro







Como hemos podido observar en imágenes previas, sólo nos resta conocer la dirección de la función system(). Podríamos volver a reingresar en GDB o haberla obtenido previamente antes de la ejecucion de readelf. En ambos casos lo solicitaremos de la misma forma mediante el comando p system.







7) Explotando la vulnerabilidad:



Para poder explotar dicha vulnerabilidad, debemos sobrescribir el valor de .GOT.PLT por la dirección de system. Tambien se puede cambiar la dirección de system por un shellcode. Ambas soluciones, sólo tendrán éxito si el ASLR no se encuentra activo.



Por último, insertamos el código que nos ejecutara la Shell. Ambas direcciones han de introducirse en código máquina. Vemos como se inserta la dirección en primer lugar y como es copiado el segundo argumento en la dirección recién creada; lo que genera nuestra Shell.











En la imagen os muestro los pasos a seguir desde la consecución de ambas direcciones hasta la obtención de la Shell:







Espero que disfrutéis del tutorial.



Happy Hack!!!











Fuentes:



https://www.redhat.com/en/blog/hardening-elf-binaries-using-relocation-read-only-relro



https://blog.softtek.com/es/explotaci%C3%B3n-de-software-en-arquitecturas-x86-i-introducci%C3%B3n-y-explotaci%C3%B3n-de-un-buffer-overflow



https://en.wikipedia.org/wiki/Global_Offset_Table




https://countuponsecurity.com/2016/04/11/evolution-of-stack-based-buffer-overflows/





','PoC Linux RELRO','