---
layout: post
title: "HTB: Pilgrimage"
date: 2024-03-28
categories: [HTB]
tags: [htb, linux, easy, imagemagick, cve]
difficulty: Easy
excerpt: "Walkthrough de HTB Pilgrimage: explotación de ImageMagick y análisis de binarios para privesc."
---


Recolección de información:



Comencemos escaneando la máquina objetivo, antes de filtrar por puertos lanzamos un mapeo general con el siguiente comando \"nmap -Pn -p- &lt;IP.OBJETIVO&gt;\". Luego enviamos la ejecución de scripts (-sV) y servicios (-sV) sobre los puertos descubiertos. Con ello tardaremos menos en su ejecución. En este caso encontramos el puerto 22 y 80 abiertos con un dominio.







Añadimos el nombre del dominio a nuestro archivo /etc/hosts para poder resolver la dirección DNS.







Continuamos con nuestro mapeo haciendo uso del script \"vuln\" (--script vuln) para poder averiguar qué tipos de vulnerabilidades encuentra nmap recogiendo la información desde la base de datos de vulners. 







Vemos enumerados posibles objetivos, pero sin duda lo que nos llama la atención es la existencia de un repositorio .git.















Pasamos a la búsqueda de archivos ocultos usando la herramienta gobuster en modo genérico pero ante la falta de resultados, usamos la herramienta ffuz con el filtro de búsqueda por tipo de archivos.







Podemos ver la aparición de nuevos archivos.











Continuamos con nuestra recolección, ahora desde el punto de vista web, recordemos que toda información es valor!! más adelante filtraremos todo.







Vemos una página en la cual existe un cajón para envío de ficheros, y dos páginas, una de Login y otra de Registro.







Probemos a registrarnos. De maravilla, a veces el envió de paquetes debe ser desde un usuario logueado.











Aparece una nueva pestaña de nombre Dashboard.







No debemos dejar de examinar el código fuente de cada página, en ellas se encuentran alojadas información más que útil. En este caso nos indica que tipo de archivos pueden ser cargados (.PNG y .JPEG)







Veamos si se produce la carga de nuestro archivo correctamente.















Análisis de vulnerabilidades:



Bién!! de momento la cosa no pinta mal. Podremos cargar una revshell dentro de la imagen para que  cuando sea cargada nos la devuelva?







Usamos exiftool para agregar el código a los metadatos...







Cargamos y cruzamos dedos...















Nada! es una pena pero había que intentarlo.







Recordamos la existencia del repositorio git, allí seguro que encontramos información de interés así que creamos un directorio y hacemos uso de la herramienta git_dumper para la descarga de dicho repositorio.







El uso de esta herramienta se encuentra en su página de github, aunque básicamente el uso es el siguiente:



python3 git_dumper.py &lt;URL ARCHIVO A DESCARGAR&gt;&lt;RUTA DESTINO EN LOCAL&gt;







Leamos qué cosas interesantes encontramos en el directorio recién descargado. Tenemos un archivo de nombre magick.







Se trata de un binario ejecutable, así que lo lanzamos.











QUE ES MAGICK?



\"ImageMagick® es un paquete de software gratuito de código abierto que se utiliza para editar y manipular imágenes digitales. Se puede utilizar para crear, editar, componer o convertir imágenes de mapas de bits y admite una amplia gama de formatos de archivo, incluidos JPEG, PNG, GIF, TIFF y PDF.  Está escrito en C y se puede utilizar en una variedad de sistemas operativos, incluidos Linux, Windows y macOS.



Características y capacidades



Una de las características clave de ImageMagick es su compatibilidad con secuencias de comandos y automatización. Esto permite a los usuarios crear procesos complejos de manipulación de imágenes que se pueden ejecutar automáticamente, sin necesidad de intervención manual. Esto puede resultar especialmente útil para tareas que requieren el procesamiento de una gran cantidad de imágenes o para tareas que deben realizarse de forma regular.



Éstos son sólo algunos ejemplos de lo que ImageMagick puede hacer por usted:




Animación crea una secuencia de animación GIF a partir de un grupo de imágenes.



Filtro de suavizado no lineal, de desenfoque bilateral, que preserva los bordes y reduce el ruido.



Gestión del color Gestión precisa del color con perfiles de color o en lugar de compresión o expansión gamma integrada según lo exija el espacio de color.



El umbral de color obliga a todos los píxeles de la gama de colores a ser blancos, de lo contrario negros.



El procesamiento de la línea de comandos utiliza ImageMagick desde la línea de comandos.



Diseño de texto complejo, soporte y configuración de texto bidireccional.



El compuesto superpone una imagen sobre otra.



El etiquetado de componentes conectados etiqueta de forma única las regiones conectadas en una imagen.



Polígono convexo del área más pequeña del casco convexo que contiene los objetos de primer plano de la imagen. Además, también se generan el cuadro delimitador mínimo y el ángulo sin rotación.



Decorar añade un borde o marco a una imagen.



Delinear imagen presenta detección de bordes astuta y líneas ásperas.



La transformada discreta de Fourier implementa la DFT directa e inversa.



La caché de píxeles distribuida descarga el almacenamiento de píxeles intermedio a uno o más servidores remotos.



Dibujar y agregar formas o texto a una imagen.



Cifrar o descifrar una imagen convierte imágenes ordinarias en galimatías ininteligibles y viceversa.



La conversión de formato convierte una imagen de un formato a otro (por ejemplo, PNG a JPEG).



La distorsión generalizada de píxeles corrige o induce distorsiones de la imagen, incluida la perspectiva.



Procesamiento distribuido heterogéneo: ciertos algoritmos están habilitados para OpenCL para aprovechar las aceleraciones que ofrece la ejecución conjunta en plataformas heterogéneas que constan de CPU, GPU y otros procesadores.



Las imágenes de alto rango dinámico representan con precisión la amplia gama de niveles de intensidad que se encuentran en escenas reales, desde la luz solar directa más brillante hasta las sombras más oscuras y profundas.



La ecualización de histograma utiliza la ecualización de histograma adaptativa para mejorar el contraste de las imágenes.



Métodos y herramientas seguros de caché de imágenes para almacenar en caché imágenes, secuencias de imágenes, videos, audio o metadatos en una carpeta local.



La calculadora de imágenes aplica una expresión matemática a una imagen, secuencia de imágenes o canales de imágenes.



Los degradados de imagen crean una combinación gradual de dos colores cuya forma es horizontal, vertical, circular o elíptica.



La identificación de imágenes describe el formato y los atributos de una imagen.



ImageMagick en el iPhone convierte, edita o compone imágenes en tu dispositivo iOS, como iPhone o iPad.



Las imágenes grandes admiten lectura, procesamiento o escritura de tamaños de imágenes de mega, giga o terapíxeles.



El montaje yuxtapone miniaturas de imágenes en un lienzo de imágenes.



La morfología de las formas extrae características, describe formas y reconoce patrones en imágenes.



Soporte de imágenes en movimiento para leer y escribir los formatos de imágenes comunes utilizados en el trabajo cinematográfico digital.



Las imágenes multiespectrales admiten imágenes multiespectrales de hasta 32 bandas, 22 de ellas metacanales.



Filtro Kuwahara de reducción de ruido y color, cambio medio.



El hash perceptivo asigna imágenes visualmente idénticas al mismo hash o a uno similar, útil en la recuperación, autenticación, indexación o detección de copias de imágenes, así como en la creación de marcas de agua digitales.



Los efectos especiales desenfocan, enfocan, ajustan o tiñen una imagen.



Texto y comentarios insertan texto descriptivo o artístico en una imagen.



Soporte de ejecución de subprocesos ImageMagick es seguro para subprocesos y la mayoría de los algoritmos internos se ejecutan en paralelo para aprovechar las aceleraciones que ofrecen los chips de procesador multinúcleo.



Transforme, cambie el tamaño, gire, enderece, recorte, voltee o recorte una imagen.



La transparencia hace que partes de una imagen sean invisibles.



Los píxeles virtuales admiten un acceso conveniente a los píxeles fuera de los límites de la imagen.




Ya sabemos que tipo de archivo es magick y para que se usa, en este caso, como conversor y renderizador de imágenes introducidas en el cajón de la página. Podemos ver en el archivo index.php el comando de ejecución donde se pide que convierta y renderice al 50% la imagen cargada y lo envíe bajo otro nombre pero con la misma extensión al directorio shrunk.







Comprobemos la versión y veamos si existe algún exploit disponible sobre esta herramienta.







Explotacion:



Basta con googlear el nombre de la aplicación junto con su versión para encontrar la solución a nuestra búsqueda.







CVE-2022-44268 : 



\"ImageMagick 7.1.0-49 es vulnerable a la divulgación de información. Cuando analiza una imagen PNG (por ejemplo, para cambiar su tamaño), la imagen resultante podría haber incrustado el contenido de una forma arbitraria. archivo (si el binario magick tiene permisos para leerlo).\"



Por lo tanto el ataque será un LFI (Local File Inclusion).  Descargamos el exploit y configuramos.







Importante ejecutar la opción de instalar los requisitos.







El uso es muy sencillo como podemos ver. En primer lugar ejecutamos python3 EXPLOIT.py --image &lt;elegimos una imagen a tratar&gt; --file-to-read &lt;archivo que queremos leer&gt; --output &lt;imagen tratada&gt;







La imagen tratada la cargamos vía web y nos devolverá una URL.







Podemos ver los metadatos con exiftool para comprobar que el archivo se manipuló como queríamos. Seguidamente ejecutamos python3 EXPLOIT.py --url &lt;URL devuelta en la web&gt; para leer su contenido.



Sin problemas!! tenemos el archivo a la vista y encontramos dos usuarios con permisos de ejecución de bash,  root y emily.







Bien, ahora tenemos que encontrar un archivo susceptible. Puesto que los intentos de lectura de archivos con permisos de root no esta disponibles. Volvemos al directorio git descargado y comprobamos el index.php. Encontramos la variable \"db\" es la creación de una instancia PDO donde se encuentra el path de origen de la base de datos o user/pass si lo hubiera.







Volvemos a lanzar el exploit, solo que solicitamos la lectura del archivo /var/db/pilgrimage.







Cargamos el archivo y nos devuelve una nueva URL.







Aquí el exploit CVE-2022-44268 de kljunowsky nos deja de funcionar puesto que no puede decodificar el archivo cifrado, pero no pasa nada, recuperamos el archivo mediante curl y lo guardamos con otro nombre mas facil....como pilgrimage, por ejemplo.







Usamos la herramienta identify para que nos muestre todo el contenido del archivo pilgrimage.







Copiamos todo el contenido del texto cifrado en hexadecimal y lo pegamos en un TXT.











Googleamos en busca de un decoder en kali y como vemos, la búsqueda es bien corta.







Decodificamos según opciones y encontramos el user/pass de emily indexado en la base de datos \"db\".







Creamos otro TXT para guardar las credenciales de emily y procedemos a autenticarnos en ssh.







Buscamos la flag de usuario con find....y... La tenemos!!







Escalada de privilegios:



Lo primero que solemos hacer es comprobar si podemos ejecutar algún archivo con sudo....pero no es el caso. Pasamos largo rato buscando archivos o indicios que nos ayuden a escalar de manera manual, pero sabeis? existe una manera más rápida, Linpeas és la solución.







QUE ES LINPEAS?



\"Es una&nbsp;herramienta de enumeración y recopilación de información en entornos Linux para el análisis de un equipo Linux accedido en un ciberataque. Se utiliza principalmente para la evaluación de seguridad y la búsqueda de posibles vulnerabilidades en sistemas basados en Linux\".



Para ahorrarnos problemas con la elección del binário correcto solicitamos información del equipo. 







Seleccionamos el binário acorde a nuestras necesidades, lo copiamos en el directorio que elijamos, y levantamos el servidor local.











Nos desplazamos al directorio /tmp y mediante curl enviamos el binário al equipo víctima. Le damos permisos de ejecución..... 







Y lanzamos.







De entre toda la información recogida la existencia de dos binários en bash es lo que más nos llama la atención.







De los dos, el más interesante es malwarescan.sh. Si leemos el código vemos que la segunda variable establece la ejecución de la primera variable mediante el binário /usr/local/bin/binwalk ....bien vayamos a ver de qué se trata.







Leemos el código de binwalk, esta vez se trata de un script escrito en python, pero ante la falta de información en su código optamos por su ejecución.







QUE ES BINWALK?



\"&nbsp;Es una&nbsp;herramienta rápida y fácil de usar para: analizar en busca de código malicioso, realizar ingeniería inversa y extraer imágenes de firmware\".







Tiene toda su lógica puesto que estamos tratando imágenes. Ahora busquemos el exploit apropiado.







CVE-2022-4510



\"Al crear un archivo de sistema de archivos PFS malicioso, un atacante puede hacer que el extractor PFS de binwalk extraiga archivos en ubicaciones arbitrarias cuando binwalk se ejecuta en modo de extracción (opción -e). La ejecución remota de código(RCE remote code execution) se puede lograr creando un sistema de archivos PFS que, tras la extracción, extraiga un módulo binwalk malicioso en la carpeta .config.\"



Descargamos el exploit desde su github, colocamos en su dirección la imagen que queremos que use y lanzamos el exploit. Como resultado obtenemos una nueva imagen .PNG. 







Ponemos nuestro Lístener a la escucha !!ATENCION!! el lístener debe estar a la escucha antes de la subida de la imágen!! puesto que la revshell se ejecuta con la carga de dicha imagen y no con la posterior ejecución del archivo desde el directorio en el que será almacenado.











Aquí tenemos nuestra shell!!! Solo nos resta expandir una shell interactiva. Revisamos en Linpeas la información del software, y vemos que podemos usar python.











Ahora solo nos resta buscar la flag de root, volvemos a usar find......NUESTRA!!!







Happy Hacking!!



Referencias:



https://github.com/vulnersCom/nmap-vulners.git



https://github.com/kljunowsky/CVE-2022-44268?tab=readme-ov-file



https://linux.die.net/man/1/identify



https://www.kali.org/tools/hurl/



https://github.com/carlospolop/PEASS-ng



https://github.com/adhikara13/CVE-2022-4510-WalkingPath



https://book.hacktricks.xyz/generic-methodologies-and-resources/shells/full-ttys
','Pilgrimage','