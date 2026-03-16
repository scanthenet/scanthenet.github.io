---
layout: post
title: "Reversing: ASLR + NX"
date: 2022-01-05
categories: [Reversing]
tags: [reversing, aslr, nx, rop, exploitdev]
excerpt: "Combinación de ASLR y NX: estrategias ROP y ret2libc para explotar binarios con múltiples protecciones."
---


Introducción:



&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; En esta entrada vamos a realizar una explotación por desbordamiento usando para ello librerías, funciones fijas y gadgets (secuencias de código) para poder evadir tanto las contramedida ASLR como NX. Nos basaremos en el desafío CTF de pico del 2013. Además, haremos uso de su binario ROP-3.



https://github.com/ctfs/write-ups-2013/tree/master/pico-ctf-2013/rop-3



Una vez en la página, vemos que además de los archivos necesarios, disponemos de un pequeño tutorial de cómo se puede realizar la explotación. Sin embargo, nosotros analizaremos en profundidad qué es lo que sucede con cada ejecución del binario mediante la introducción y ejecucion de varios scripts, obteniendo la explotación del binario de una forma más detallada. Pero antes de introducirnos en el código, un poco de teoría e historia para que nos suene lo que más adelante realizaremos.



Un poco de historia:



Durante las conferencias &nbsp;Black Hat USA 2008 Briefings dadas en agosto de 2008, Erik Buchanan, Ryan Roemer y Stefan Savage describen dicho ataque de la siguiente manera:



“Describimos la programación orientada al retorno, como una generalización the return-into-libc que permite a un atacante realizar cálculos arbitrarios y completos de Turing sin inyectar código.



Los nuevos cálculos se construyen enlazando fragmentos de código que terminan con una instrucción RET. Estas instrucciones permiten a un atacante que controla la pila encadenar secuencias de instrucciones. Debido a que el código ejecutado se almacena en la memoria marcado como ejecutable, WX y DEP no impedirán que se ejecute.



WX y DEP, junto con muchos otros sistemas de seguridad, suponen que prevenir la introducción de código malicioso es suficiente para evitar la introducción de computación maliciosa. Con el enfoque de computación orientada al retorno “ROP”, esta suposición es falsa. Se puede subvertir el flujo de control en la pila para construir un cálculo arbitrario a partir de un código el cual no es malicioso”



Muy bueno, pero no me queda claro:



&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Las siglas ROP provienen de la palabra inglesa Return Oriented Programming que consiste en la ejecución de pequeñas secuencias de código que ya existen en la memoria de un proceso.



&nbsp;¿Pero cómo vamos a conseguir La dirección exacta de un proceso estando presente la contramedida ASLR? 



&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Estas pequeñas secuencias que se ejecutan en la pila se conocen como gadgets y se caracterizan por acabar con una instrucción cambio de flujo. Normalmente se trata de una instrucción de retorno de subrutina, que permite el encadenamiento de los gadgets.



&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; En otras palabras, este tipo de ataque se basa en inyectar en la pila una secuencia de direcciones que apuntan a los distintos gadgets. De este modo, cuando se ejecuta el retorno de una función, se salta a la dirección inyectada en pila evadiendo así el ASLR y comienza la ejecución del gadget deseado.



Ahora: ¡Al ataque ROP!:



&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Para comenzar echaremos un vistazo al binario sin compilar, recién descargado. Observamos que en la primera función se encuentra el buffer overflow, en la segunda se declara la llamada a bash y en la función principal el programa cierra con un mensaje base en programación.







Comprobación de contramedidas:



&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Comprobamos el estado de las contramedidas para poder ejecutar la explotación según se pide en el desafío. Para ello desde nuestra consola de comandos comprobamos el estado D la contramedida ASRL, y del NX.



Recordamos que el estado del ASRL en el sistema se define mediante 3 números:



0= OFF1=ONà La página virtual dinámica de objetos compartidos y las regiones de memoria compartidas están aleatorizadas.2=ONà Además de lo descrito en el valor 1, los segmentos de datos se encuentran aleatorizados.



Tampoco debemos olvidar que la contramedida NX evita la ejecución de cualquier dato engañoso después de mover el flujo de ejecución de regreso a la pila, lo que provocará la rotura del programa con un SIGSEGV (violación de la segmentación de la señal: señal enviada a un proceso cuando se refiere a un área de memoria inválida; por ejemplo, que no pertenece a ella). No obstante, esta señal puede ser captada para poder modificar su comportamiento.







Comprobando el funcionamiento:



&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Ejecutamos en nuestra consola de comandos el binario. Podemos observar que tras la introducción de algún carácter el programa cierra con el saludo.







Buscando el offset:



Sabemos que el desbordamiento de pila procede de la función vulnerable. Esta vez sí, cargamos el binario en el debugger y procedemos a crear un patrón de 200 caracteres. Con el patrón recién creado hacemos correr el binario, el cual mostrará el error de segmentación y ruptura de la ejecución. Es exactamente lo que queremos que realice.







Descenderemos hasta el final de los datos arrojados por el debugger y solicitaremos que nos muestre cuántos caracteres se han leído antes de proceder a la interrupción del programa. Podemos ver que se trata de 140 caracteres.



Puntero EIP:



&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Debemos determinar si efectivamente el puntero de registro EIP apunta a la siguiente instrucción a ejecutar del segmento de código. Desde nuestra consola de comandos crearemos un nuevo patrón con 140 “A” para finalizar en cuatro bytes con el carácter “B”.







Rebuscando información:



Ya tenemos el control de EIP. ¿Podríamos ejecutar código? Por poder podríamos, pero debemos tener presente la contramedida NX, la cual finalizará el programa ante la detección de introducción de código malicioso. Es en este punto donde las palabras de Erik Buchanan, Ryan Roemer, y Stefan Savage cobran sentido. ¿Qué tal hacer uso de código legitimo para reconducir el comportamiento? Quizás la solución pase por inspeccionar el binario para ver qué funciones pueden ser llamadas. Podemos ver como la contramedida ASLR realiza su trabajo ocultando cualquier cosa que provenga desde libc como system, por ejemplo, pero vemos funciones que están presentes en PLT, y sus direcciones no serán aleatorizadas. De entre las presentes haremos uso de 2 funciones: la función read y la función write. Usaremos dichas funciones para obtener datos desde el binario.







Usaremos dichas funciones de forma contraria. Escribiremos datos en una localización arbitraria utilizando read() y leeremos datos arbitrarios usando write().







Obteniendo la dirección read() y system():



Ahora que sabemos esta información vamos a perfilar nuestro ataque. Usaremos write() Para leer la dirección actual de read() desde LIBC.







Procedemos a cargar el binario en el debugger y haremos uso del comando run únicamente. Una vez que aparezca el prompt del usuario presionaremos las teclas CTRL+C. Es el momento de introducir la dirección de read() mediante el comando X + DIRECCION. Esto nos dará la dirección de la librería. Haciendo uso de la herramienta VMMAP podremos determinar el espacio de ésta, el nombre y, lo más importante, los permisos.







Como ya sabemos, todas las direcciones en LIBC tienen una constante de offset desde la librería base. Teniendo ese principio presente, ahora podemos leer la dirección de system() mediante el offset existente desde red() hasta system().







Ahora podríamos pensar que bastaría con ejecutar las siguientes funciones para sacar los offset necesarios y poder explotar el desbordamiento de búfer. No obstante, como LIBC se encuentra aleatorizada, esas direcciones serían distintas en cada ejecución. Para solucionar este problema volveremos a usar write(), para poder obtener la dirección actual de read(), pero esta vez desde GOT.



Configurando la pila como en un ataque ret2libc:



Debemos configurar la pila como si de un ataque ret2libc se tratase. Para ello necesitamos la dirección de retorno, los argumentos y que éstos llamen a la función. Añadiremos a nuestro script la dirección write@plt, 4 caracteres “C” y los valores que solicita la función write:







Int fd (file descriptor) es 1 , porque stduot es siempre 1; es el valor Linux por defecto (verde)*buf, debe de ser un valor constante y que comience desde el buf, por lo tanto, la dirección de read() (azul)Size_t será de 4, porque solo necesitamos una dirección de 4 bytes (Naranja)



Quedará el script como podemos observar la siguiente imagen:







Siempre es bueno recordar que, si no nos genera el archivo core, puede deberse a falta del archivo en el directorio /proc/sys/kernel/core_pattern, o de existir éste, que se encuentre limitado. Para resolver este problema, podemos ejecutar los comandos que observamos en la imagen superior, anteriores a la ejecucion del script.



Expliquemos con detalle el script:



“A”*140 ---&gt;offset de salida o punto de desbordamiento\\xa0\\x83\\x04\\x08 ---&gt; dirección de la función write@plt“CCCC” ---&gt;lo usaremos como referencia para que el programa finalice con segfaultsEl argumento de file descriptor ---&gt; 0x00000001La dirección de read()---&gt;0x8004a000, usaremos la entrada GOT porque no esta aleatorizada y apunta directamente a libc. Sin embrago PLT sólo apunta a la entrada GOT y no puede ser usado en este momentoEspacio de 4 bytes es ---&gt;0x00000004



Tras la ejecución nos devolverá una violación del segmento y acabará el proceso. Pero ¿qué acaba de pasar? ¿Quizás los bytes nulos sean la razón del error? La respuesta la encontramos si el mismo script lo pasamos a txt y lo ejecutamos en el debugger.







Calculando los bytes comunes de las librerías:



Ya hemos visto como se comporta el binario tras su ejecución. Continuando con la explotación debemos saber qué bytes son comunes a todas las librerías.







Tras la ejecución del comando que podemos observar en la imagen superior, solicitaremos saber la dirección en hexadecimal de la librería y qué espacio ocupa.







Creando el exploit:



Haremos uso nuevamente de pwntools para realizar convenientemente el proceso de retorno de bytes. Es el momento donde comenzaremos el ROP realmente.



Para comprobar que efectivamente se realiza un ROP, crearemos un primer script donde :



Declaramos la variable “leak” con el código a emplear.Declaramos la variable “exploit”, el cual solicita el proceso del binario, así como el permiso de apertura de una Shell.Cuando el binario se ejecute, leak es enviado en una nueva línea.Declaramos la variable “read_addr” donde pedimos que write() devuelva 4 bytes desempaquetado.Por último, solicitamos que imprima en pantalla el resultado obtenido de la variable read_addr.







Ejecutamos el script el cual nos retorna una dirección que no es la correcta. ¿Porqué? Porque el ASLR continúa estando presente.







Acaba de pasar lo que esperábamos que pasara: la siguiente ejecucion seria CCCC y ante eso el binario interrumpe la ejecucion.







Bien, llegados a este punto toca eliminar la dirección “CCCC”. Recordamos que según la función write, necesitamos de una dirección que se encuentre en el bof. Si nos fijamos, la única diferencia que se encuentra en el script anteriormente lanzado con el actual es el cambio de la cadena “CCCC” a la cual apuntaba el registro EIP, por la dirección de la función vulnerable.







Ejecutamos el script y vemos como la&nbsp; dirección no cambia. Podríamos decir que hemos Bypaseado el ASLR ya que hemos conseguido imprimir la dirección dos veces.







Pero ¿cómo ha ocurrido? La función vulnerable no toma ningún argumento, por lo que realmente no importan los argumentos de la pila y realizará la operación de lectura de la vulnerabilidad por segunda vez, dándonos otra oportunidad de explotar la vulnerabilidad.



Una vez confirmado que la operación de desbordamiento puede ser lanzada una segunda vez es el momento de implementar un segundo payload, el cual se encuentra desarrollado al estilo de ataque ret2system.



Segundo payload:



Antes de poder escribir dicho payload, necesitamos escribir las direcciones del sistema, así como la cadena de /bin/sh junto con sus respectivos offset desde la dirección read().



El primer paso es ejecutar el binario en el debugger. Corremos el binario y pulsamos control + C







El segundo paso es conseguir las diferentes direcciones. Para ello bastará con que ejecutemos el comando P seguido de la función sobre la cual queremos saber el offset. Además, con el comando find localizaremos la dirección de la Shell.







Ahora que ya tenemos las direcciones, podemos determinar los offset existentes, tomando como referencia la dirección de la función read.







Ha llegado el momento de implementar nuestro nuevo payload al archivo vulnerable. En la imagen inferior podemos ver el script completamente conformado. Además, también podemos observar remarcado en rojo los offset en sus respectivas variables. Éstas nos ayudarán a calcular los prerrequisitos para llamar a la función System.



Sólo usamos direcciones calculadas dinámicamente en lugar de direcciones codificadas. Para llamar a la función System, simplemente lo invocamos con la dirección de la cadena “bin/sh” como argumentos y después volvemos haciendo uso de la función exit.







En la parte final del script declaramos la variable la cual albergará la cadena con 140 “A” y que a esa cadena le sume para que puedan ser leídas por la máquina las variables ya empaquetadas que acabamos de definir con los offset.



Por último, pediremos a exploit que dicha variable sea leída en una nueva línea y que tras ello inicie una Shell interactiva.







Éste ha sido el ejemplo de cómo funciona un ROP. Hemos usado partes del código permitido en el programa de manera que combinen entre ellos hasta conseguir la explotación.



Espero que os guste.



Happy Hack!!



Quiero hacer mención especial a mi esposa, la cual, con su apoyo y con su inestimable ayuda a la hora de corregir los textos, hace posible que pueda continuar escribiendo estas entradas.



Referencias:



https://github.com/ctfs/write-ups-2013/tree/master/pico-ctf-2013/rop-3



http://webdiis.unizar.es/~ricardo/files/PFCs-TFGs/Prevencion-Ataques-ROP-DBI/Memoria_PFC_PrevencionAtaquesROPDBI.pdf



https://hovav.net/ucsd/talks/blackhat08.html



https://es.frwiki.wiki/wiki/SIGSEGV



http://sop.upv.es/gii-dso/es/t2-arquitectura/tr6.html



https://en.wikipedia.org/wiki/Programming_language_theory
','Ataque ROP','