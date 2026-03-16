---
layout: post
title: "Ingenieria social"
date: 2021-07-04
categories: [OSINT]
tags: [osint, ingenieria-social, recoleccion]
excerpt: "Recolección de información mediante ingeniería social: técnicas y vectores de ataque humano."
---


Hoy no hablaremos sobre intrusión o escalada de privilegios. Si bien es cierto que todo dispositivo conectado a la red es susceptible de ser vulnerado, hay que recordar que el factor humano, es decir, los errores que comete una persona en el manejo de los diferentes dispositivos que tiene en su negocio, es el gran vector de ataque para la consecución de una intrusión exitosa, o por lo menos, trastornar el buen funcionamiento del sistema. Está claro que todo es mejorable y que cada cual es libre de realizar con su red y sus dispositivos lo que le venga en gana, pero por favor, pongámoselo difícil a los ciberdelincuentes (MAL LLAMADOS HACKERS).







Como bien sabe cualquiera que se dedique a la seguridad informática, lo primero que debemos realizar es la recopilación de información. ¿En qué consiste esta fase? Pues bien, es la más importante de todas puesto que las siguientes fases dependerán de los datos obtenidos en ésta. Por poner un símil, son los cimientos de la casa que se va a construir. Si estos cimientos son débiles, no están bien anclados y bien nivelados, la casa podrá ser construida pero de forma ardua y sufrirá continuos fallos e incluso llegar a no construirse. Ahora bien, y en modo un poco mas técnico, se trata recabar toda la información posible del objetivo, para luego ocuparnos de filtrar y desechar el montón de información recolectada. Vamos a suponer que el objetivo es una tienda de telefonía. Hoy día es muy común que éstas sean espacios abiertos, diáfanos y con grandes cristaleras donde al entrar nos encontramos varios mostradores a cada lado en disposición de espiga para evitar aglomeraciones de los posibles compradores, y los mismos puedan acceder hasta el fondo de la tienda para poder tener una vista general de la misma.







Bien, como auditor comenzaría a recopilar información sobre horarios de entrada del personal. Podemos ver que desde la calle se pueden ver los puestos de trabajo. Una vez que sé cuando comienzan a entrar e iniciar los dispositivos, grabaría con una cámara la introducción de contraseñas. ¿¿¿Para qué quieres grabar esto??? Para saber las pulsaciones que realiza el vendedor sobre en teclado, un keylogger visual vamos. Si el espacio exterior, como es el caso, me lo permite, realizaría un \"shouldersurfer\" o \"shouldersurfering (esto que suena tan extraño no es más que una técnica conocida y realizada por todos nosotros en el colegio: mirar por el hombro a ver si podías copiar algo del compañero de pupitre). También suele ser normal en los negocios que abran a los clientes sin las sesiones iniciadas. Si es el caso, entraría el primero, fingiendo tener mucha prisa, lo cual me permitiría acercarme al vendedor para contar los pulsos y quizás, coger alguna tecla al vuelo. 







Si nos fijamos en la primera fotografía, el segundo banco es ideal para poder mirar los tres puestos de trabajo. Ahora sólo necesitamos ir en hora de máxima afluencia de clientes, sentarnos y esperar a ser atendidos. Durante esta franja horaria, con las prisas y el agobio, los vendedores suelen dejar la sesión y el ordenador desbloqueado mientras realizan alguna gestión de entrega de dispositivos, sacar algo del almacén, cosas por el estilo. En ese instante, mientras fingimos estirar las piernas, podremos pasar al lado grabando el paseo, luego visualizaremos las pantallas activas, información de plataformas, iconos de escritorio (tal como vemos en las imágenes siguientes)



En esta captura podemos ver que este dispositivo, tiene ejecutando los motores de búsqueda Opera, Explorer, Chrome y Firefox. Ademas ejecuta Skype, Microsoft Word. Por ultimo tiene el Dropbox en modo sincronizado y se conecta por WI-FI.



Acabamos de  limitar vectores de ataque. Ya sabemos que el sistema operativo es un Windows 10, que podemos intentar un ataque con malware (un keylogger o grabador de pulsación de teclado en español) e insertarlo en las macros de Word para enviar al vendedor un correo con una factura en formato Word y comprimido en Zip, intentar ataques a las vulnerabilidades conocidas de los buscadores, conseguir privilegios de sistema a través de Skype o comprometer el dispositivo a través Dropbox. Increíble lo que se puede obtener con una imagen, no?



Con esta captura vemos que se encuentra en ejecución varias aplicaciones, pero llama la atención que el icono del Defender este dando una alerta.



Al igual que el anterior a veces dejamos clicado la barra de iconos ocultos en ejecución. Pues bien, a simple vista vemos el Chrome, Dropbox, el Bluetooth, Eclipse, Java y gráfica Nvidia. Con estos datos, podemos ir filtrando vectores de ataque e ir reduciendo la lista para perfilar el futuro ataque.



Volvamos a la imagen principal. Los dispositivos son portátiles sin cables a la vista, lo que nos indica que se conectan por WI-FI (esto es importante de cara a un ataque WI-FI). Generalmente los router suelen estar instalados en zonas altas y lo más centrado posible del comercio (no queda bien que en una tienda te quedes sin señal). Pero si tenemos dudas, podemos aplicar un poco de ingeniería social argumentando que estas interesado en la compra de un buen router, y entre preguntas de los distintos dispositivos dejas caer la típica de \"La verdad es que necesito uno potente, como el que tenéis aquí\" suele funcionar. Los humanos somos vanidosos por defecto y nada nos gusta más que poder mostrar lo grande que tienes tu router y si previamente nos han regalado el oído, mejor. También podemos preguntar si tienen WI-FI público. Se puede sacar información del router o incluso escalar privilegios si tiene una mala configuración.



Al tener los distintos componentes a la vista podemos ver el ordenador que usan (marca y modelo), la impresora (es otra puerta de ataque, recientemente se puso en conocimiento una vulnerabilidad en la cola de impresión) los teléfonos móviles de los empleados, la chapita con el nombre y número de vendedor (algunas empresas colocan el número de vendedor en la generación de usuario corporativo; otras, las dos primeras letras del nombre y apellidos).



Ahora le toca el turno a la ingeniería social para la obtención de datos. Debemos hablar generando un ambiente distendido, intentando recabar el maximo de información personal del vendedor. ¿Por qué? Si la vendedora Ana lleva un tatuaje o un abalorio con motivos de perros, le podemos preguntar si tiene perro, que raza es, como se llama... Si lleva alianza, intentamos averiguar si esta casada y si llevan muchos años casados, si tienen hijos (en caso afirmativo es muy probable que la contraseña contenga referencia a los mismos)... También podemos montar el teatro que el teléfono es para regalo de cumpleaños y en el momento adecuado preguntarle por su cumpleaños. Saber de donde es nos será de gran ayuda a la hora de la búsqueda en redes sociales, plataformas de empleo..... Todo ello para delimitar el rango del mismo.



¡Casi se me olvida! El tema de libretas abiertas sobre el mostrador y post-it pegados en las pantallas. Eso debería de ser motivo de fusilamiento al amanecer, pero os puedo garantizar que lo he visto en varios negocios, así como las típicas guías de inicio y las operaciones a llevar a cabo. !!!Por favor!!! !!!Se le deberían caer los dedos como castigo!!!



Bien, es hora de algunas recomendaciones:



Disponer los dispositivos de manera que no se puedan ver los teclados y mucho menos el monitor



 Si el monitor debe quedar a la vista, colocarlo en un ángulo que no pueda ser visualizado por los clientes o posibles compradores que merodeen por las estanterías. 



Si se da el caso de tener que mostrar información por el monitor, es recomendable disponer de dos monitores en modo extendido, orientando el secundario para poder ser visto tanto por el vendedor como el cliente (así podremos ejecutar operaciones mientras que al cliente le mostramos la parte de pantalla que queremos y no mostramos información de la barra de tareas )



monitor secundario



No tener espejos o paneles que reflejen la pantalla detrás del operario. 



Colocar el router de manera que sólo sean visibles las antenas.



Capar muy bien la red WI-FI pública.



Cambiar la contraseña que el router trae por defecto. 



La impresora debe estar en un lugar de difícil observación y los materiales de la misma que no estén a la vista (sirve de poco ocultar la impresora si luego se ven repuestos de HP Office Jet Pro, por ejemplo). 



Crear contraseña para la impresión y confirmación de la misma por parte del usuario.



Encender los dispositivos e iniciar sesión antes de abrir el negocio. 



Apagar todos los dispositivos, inclusive el router, al acabar la jornada. 



Evitar dar datos personales y si por no parecer grosero damos algun dato, que no sea cierto (recordar que el malo suele ser el que menos pinta de tiene de serlo). 



No desbloquear teléfonos o tabletas con personas cerca.



Si el negocio es propio, no creéis usuarios como Ana y contraseña 1234, qwerty, tequiero, el nombre del perro, el nombre del hijo,fechas, DNI.....y un largo etc. Crear contraseñas fuertes de combinación alfanumérica y algún símbolo.



¡¡¡Y por el amor a la seguridad informática, nada de post-it en monitores o filo interno de mostradores, las libretas guardadas y las guías de inicio o procedimientos guardadas en el lugar más lúgubre y oscuro del cajón!!!



Creo que esta entrada es interesante porque le damos muy poco valor a la seguridad en nuestros negocios. Son pequeños actos que debemos realizar, pero que nos pueden librar de un buen susto. Hemos podido ver como de una ojeada se recolecta información valiosísima de cara a las siguientes etapas del ataque, como se puede delimitar búsquedas con el simple hecho de tener la barra de tareas o el menú de iconos ocultos a la vista y la importancia de la ingeniería social la cual es un arma poderosa para quien la sabe utilizar.



Espero que os haya gustado leerlo tanto como a mí escribirlo.



Happy Hacking 
