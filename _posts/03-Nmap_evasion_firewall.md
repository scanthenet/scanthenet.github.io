---
layout: post
title: "Evasion de firewall con Nmap"
date: 2021-06-10
categories: [Recoleccion]
tags: [nmap, evasion, firewall, reconocimiento]
excerpt: "Técnicas de evasión de firewall con Nmap para realizar reconocimiento sin ser detectado."
---


Hoy voy ha escribir sobre como usar Nmap para poder evadir firewall y poder asi recolectar información de nuevos puertos y el estado de los mismo.



Como bien sabéis, Nmap es una fantástica herramienta para el descubrimiento de puertos, amén de poseer otras capacidades tales como información del OS y vulnerabilidades, traceroute, carga de scripts....etc. Si leéis el manual de Nmap descubriréis infinidad de técnicas y la compatibilidad existente entre ellas (dejo el link de referencia al pie de la entrada). Con todo explicare de forma sencilla las opciones más comunes y rápidas ( y que generalmente se nos olvida).Nmap dispone de varias técnicas evasivas, pero hoy nos centraremos en la fragmentación de paquetes, el control del tiempo y el uso de señuelos.



FRAGMENTACION DE PAQUETES (-f  --mtu)



como su nombre indica, esta técnica consiste en dividir la cabecera de paquete TCP en varios paquetes mas pequeños, dificultando asi la detección por parte del Firewall o el IPS (Intrusion Prevention System o Sistema de Detección de Intrusiones en Español). Si usamos la opción -f Nmap dividirá la cabecera del paquete en paquetes de 8 bytes , como ya sabemos, una cabecera tiene entre 20 y 60 bytes, siendo el estándar 20 bytes, por lo tanto, nmap dividirá la cabecera en paquetes de 8 bytes, enviando al destino 3 paquetes, 2 de 8 bytes  y 1 de 4. Tambien podemos enviar paquetes de 16 bytes usando -f nuevamente o como opción mas personalizada, usando el comando --mtu podemos seleccionar el tamaño que deseemos fragmentar la cabecera del paquete. Si optamos por la opcion --mtu debemos tener en cuenta que no se puede usar conjuntamente con el comando -f , además, los paquetes deben ser múltiplos de 8 bytes.



En la siguiente imagen se puede observar un escaneo a la web objetivo, (en este caso es de mi propiedad y yo me doy permiso a mi mismo para escanearla) podemos ver que wireshark ha capturado el trafico de red. He elegido el paquete de TCP/IP  sobre el puerto 80. Realizamos un sondeo TCP SYN por varias razones, es relativamente rapido y poco ruidoso, no establece una conexión total con el objetivo, sino que se envía un paquete SYN esperando respuesta, si se devuelve un paquete SYN/ACK  indica que el puerto está en escucha (abierto), mientras que si se recibe un RST (reset) indica que no hay nada escuchando en el puerto (cerrado). Si no se recibe ninguna respuesta después de realizar algunas retransmisiones entonces el puerto se marca como filtrado. También se marca el puerto como filtrado si se recibe un error de tipo ICMP no alcanzable (tipo 3, códigos 1,2, 3, 9, 10, ó 13).



Realizamos un primer escaneo sin obtener respuesta:







Aqui podemos ver la captura con wireshark sobre el puerto 80 sin fragmentar:







 Realizamos un nuevo escaneo esta vez usando la fragmentación por defecto -f .Podemos ver que arroja información de puertos.







Ahora veremos como nmap fracciona los paquetes usando -f, como he dicho anteriormente, por defecto los fraccionara la cabecera del paquete en paquetes de 8 bytes. Nuevamente revisamos el paquete sobre el puerto 80 del nuevo escaneo.







Tambien podemos fragmentar las cabeceras de los paquetes del tamaño 16 bytes con la opcion -f -f. Como se puede observar nos a devuelto un puerto mas 7778/tcp interwise.







Observamos la captura del paquete con wireshark.







Tambien disponemos de la opción personalizada de tamaño del paquete fragmentado, con el comando --mtu, podemos introducir el tamaño del paquete teniendo en cuenta un par de consideraciones, no es valido con el uso conjunto de -f y que el tamaño debe ser múltiplo de 8. Ahora podremos ver como el escaneo con este comando arroja el mismo resultado que realizando un escaneo con -f.







Podemos observar que el paquete de control arroja los mismos datos que un escaneo -f:







CONTROL DE TIEMPO (-T):



Como se puede ver, hemos obtenido más información del objetivo a medida que realizamos distintas técnicas, pues bien, ahora le toca el turno al tiempo, el comando mas conocido es -T el cual tienen un rango de 0 a 5, siendo 0 el mas lento y 5 el mas rapido. Como norma suelo utilizar el 3, para el escaneo de una dirección bajando a 2 para escaneo de puertos específicos. Ateniéndonos al manual y según dice el mismo, el valor 3 es como realizar un escaneo normal y no se notara la diferencia de ponerlo o no....veamos la siguiente imagen:







Para no notarse la diferencia nos ha devuelto varios puertos.



USO DE SEÑUELOS (-D):



Ahora veremos el uso de señuelos durante un escaneo. Siendo más bien una técnica de ocultación mas que de evasión de firewall, nunca está de más si queremos realizar un escaneo un poco más disimulado. Hay que tener en cuenta tres consideraciones... a más señuelos más se ralentizará el escaneo y puede arrojar datos erróneos, el comando ME determina el lugar que ocupara nuestra IP en la lista de solicitudes, si no marcamos ME, Nmap nos otorgara una posición aleatoria, por ultimo, los señuelos irán separados por comas SIN ESPACIO:







Vemos la captura de paquetes, como se puede ver el señuelo realiza la petición al puerto 80 y tras el lo realiza la IP real, seguida de la respuesta por parte del objetivo solo a la IP real (esto desmonta la teoría de la ocultación, puesto que cualquier administrador de sistemas detectará nuestra Ip filtrando solo las respuestas) por otro lado el saber no ocupa lugar.







Pues esto es todo por ahora, espero que os guste el articulo. 



Un saludo y Happy Hacking.



Referencias:



https://nmap.org/man/es/man-bypass-firewalls-ids.html

