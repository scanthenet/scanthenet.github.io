---
layout: post
title: "Rerversing: Formato de cadenas printf"
date: 2022-01-12
categories: [Reversing]
tags: [reversing, format-string, printf, exploitdev]
excerpt: "Vulnerabilidades de cadenas de formato con printf: lectura y escritura arbitraria en memoria."
---


Introducción:



Para poder entender esta vulnerabilidad, debemos saber cómo los argumentos se pasan a las funciones (a través de la pila antes de una llamada a función) y cómo funciona la pila durante el tiempo de ejecución de un programa. Lo que vamos a ver a continuación se conoce como vulnerabilidad en el formato de cadenas.



Esta vulnerabilidad está directamente relacionada con la familia de las funciones printf, además de funciones análogas:



frintf - Imprime el fujo de un archivoprintf - Imprime el flujo de los stdoutsprintf - Imprime en una cadenasnprintf - Imprime en una cadena con chequeo de longitudsetproctitle - Establece argv[]syslog - Salida de Syslog



¿ Qué tienen en común estas funciones?



Todas ellas se utilizan para imprimir datos en un destino específico, pero lo especial de todo es que hacen uso de argumentos que funcionan como modificadores de cadenas. Por ejemplo, ya hemos visto argumentos como los siguientes:



printf(“%s”, variable); Imprime la variable como cadena en su formato



printf(“%p”, variable); Imprime la variable como puntero



Un poco de historia:



A principios de los 2000, los hackers comenzaron a abusar del comportamiento de la función printf(). Si un usuario obtenía el control de los argumentos de dicha función, podía obligar al programa a modificar su comportamiento. En esta prueba de concepto veremos que las técnicas a usar pueden conducir a fuga de información de la memoria o a un DoS si se provoca un error de segmentación.



Esta vulnerabilidad se consideró obsoleta hasta el &nbsp;2019, cuando varios exploits fueron publicados por varios investigadores de seguridad informática que explotaban una vulnerabilidad de formato de cadenas para obtener una pre-autenticación RCE sobre un&nbsp; popular servicio VPN.



Dado que esta vulnerabilidad ha vuelto a resurgir de sus cenizas, quizás sea bueno comprender como funciona ¿no?



Funcionamiento:



Printf() Una vez proporcionado el argumento del formato de cadena y otra variable como argumento, usaremos el formato de cadena (primer argumento) para imprimir la variable (segundo argumento) de manera específica. Los modificadores más comunes son %x (hex), %p (puntero), %d (decimal) y %s (string).



Vamos a crear un código sobre el que poder poner en práctica la prueba de concepto.







Compilamos el archivo de forma predeterminada y lo ejecutamos directamente desde nuestra consola de comandos. Podemos ver como las variables son impresas en los formatos codeados (primero como decimal, segundo como puntero y tercero como cadena).







Ahora cambiemos el código para que los formatos printf no coincidan con los argumentos proporcionados a %x. Además, agregaremos un modificador adicional asi que ahora tenemos 4 modificadores y 3 argumentos. Volvemos a compilar.











Una vez lanzado el programa vemos que no realiza un error de segmento; imprime todos los valores y &nbsp;además añade un nuevo valor.







Antes de continuar con el depurador, y para evitar problemas de lectura, desactivamos el ASLR.







Vamos a ejecutar el binario en el depurador para observar cómo funciona desde dentro. Estableceremos un punto de ruptura en printf y hacemos correr el programa.







Si nos paramos a mirar el diseño de la pila justo antes de la llamada a printf, reconoceremos algunos valores. La primera dirección es la dirección de retorno y la segunda apunta al argumento de formato, que se mantiene en la memoria como cadena.











Notamos que no existe información sobre las variable que queremos imprimir. La función printf() funciona de la siguiente manera: el usuario es responsable de proporcionar la cantidad adecuada de argumentos y modificadores. Entonces, como con cualquier otra función, durante la llamada a esta, los argumentos son colocados en la pila. Primero la parte de formato y luego los argumentos a formatear.







Si el número de modificadores es mayor que el de los argumentos, los siguientes elementos de la pila se supone que son los argumentos. Volvamos a modificar nuestro binario a ver si se cumple lo argumentado.







Como podemos ver , en este caso, printf() comienza a coger elementos desde la &nbsp;memoria e imprimirlos.







Espero que os haya gustado, en la siguiente entrada mostraremos como explotar esta vulnerabilidad.



Happy Hack!!







REFERENCIAS:



https://blog.orange.tw/2019/07/attacking-ssl-vpn-part-1-preauth-rce-on-palo-alto.html



https://cs155.stanford.edu/papers/formatstring-1.2.pdf
','Vulnerabilidad en el formato de cadenas','