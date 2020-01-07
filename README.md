# Dist2

### Consideraciones generales:

Para cada una de las actividades existe un archivo "docker-compose.yml", por lo que dependiendo de la actividad que se quiera ejecutar, basta con meterse dentro de la carpeta *"Act1"* o *"Act2"* y ejecutar los comandos "docker-compose build" y "docker-compose up".

Para ambas actividades existen dos tipos de aplicaciones ("servidor" y "cliente") que se encuentran en los directorios "Server" y "Client" respectivamente. Dentro de cada una de estos directorios, existen los archivos "Dockerfile", y el código python de las aplicaciones correspondientes.

Dado que se utiliza el caracter ';' como separador, se asume que ningún mensaje o nombre de cliente/usuario tendrá ese caracter ya que inducirá a errores.

Para detener la ejecución se debe hacerlo forzándola presionando la combinación CTRL+C en la terminal donde se está ejecutando. **NOTA:** Ya que para realizar la simulación entre los dos clientes y el servidor se utilizó una función que usaba un ***random*** es necesario esperar a que terminen (esperar a ver *c1 exited with code 0* o *c2 exited...*) para poder forzar la detención "correctamente" (aun así mientras se simula se puede agregar un tercer cliente desde afuera). 

(Tal y como está la tarea funciona, dado que no se debiesen cambiar los input de esta tarea no deberían haber problemas, y si llegasen a ocurrir se hablará en alguna instancia futura)
(Solo se ha probado la tarea en w10)

## Actividad 1 (Act1)

Para la primera actividad era necesario utilizar el protocolo RPC con gRPC, es por ello que se utiliza un archivo .proto que genera los archivos *Act1_pb2.py* y *Act1_pb2_grpc.py* y por comodidad se dejaron en la carpeta raíz de esta actividad. Para generar estos archivos es necesario tener instaladas las librerías grpc y grpc-tools.

### Servidor

Dentro de la carpeta Server solo existe un archivo .py que es el que básicamente contiene todo el código de este, por otro lado notar que además este depende de los 2 archivos **Act_pb2**. 
Para que funciones correctamente es necesario que exista previamente el archivo *log.txt*. En él se encontrá el "log" de los mensajes recibidos por el servidor.

**Cuando el servidor parta se mostrará por pantalla su IP, esta será la que se deberá usar para conectarse a él manualmente cuando se quiera agregar un tercer o cuarto cliente.**

### Cliente

Dentro de la carpeta Client existen dos archivos para el *Cliente*: **Client.py** es el archivo que se utiliza para realizar la simulación de la interacción con el servidor; por otro lado está **ClientOut.py** que es el que se deberá ejecutar si es que se quisiera agregar un tercer cliente al servidor. Por último se creó una carpeta *act1* que contiene una copia de los archivos **Act_pb2** necesarios para que el cliente que se conecte desde afuera se pueda ejecutar.

Al iniciar **ClientOut.py** se harán una serie de preguntas que le permitirá poder acceder e interactuar con el servidor y otros usuarios a través de él. El login es simplemente colocar el nombre de usuario, esto significa que cualquiera que coloque su nombre creará un nuevo usuario o accederá a una cuenta creada.

**Para conectar un tercer cliente** se debe ejecutar la línea `python .\Client\ClientOut.py` desde la raíz de la actividad 1 (*\act1*), además es necesario introducir la IP mostrada por el servidor al inicio de su ejecución cuando sea solicitado por el cliente, de esta manera ya podrá realizar cualquiera de las funciones mostradas en el menú. 

## Actividad 2 (Act2) 

Ya que para esta actividad era necesario utilizar el protocolo RPC con RabbitMQ, fue necesaria la "instalación" de la imagen de rabbit para docker (revisar el archivo .yml). Es por esto que además es necesaria la instalación de **pika** llevada a cabo mediante los archivos *dockerfile*.

**Nota:** Dado que el container de rabbit suele demorarse, se dejó una línea `time.sleep(n)` (con n cantidad de segundos) al inicio de los archivos *Client.py* y *Server.py* para que el container pueda cargar sus archivos con tranquilidad al inicio y no provoque ningún error prematuro al hacer docker-compose up.

### Servidor

Dentro de la carpeta Server solo existe un archivo .py que es el que básicamente contiene todo el código de este.
Para que funciones correctamente es necesario que exista previamente el archivo *log.txt*. En él se encontrá el "log" de los mensajes recibidos por el servidor.

### Cliente

Dentro de la carpeta Client existen dos archivos para el *Cliente*: **Client.py** es el archivo que se utiliza para realizar la simulación de la interacción con el servidor; por otro lado está **ClientOut.py** que es el que se deberá ejecutar si es que se quisiera agregar un tercer cliente al servidor.

Al iniciar **ClientOut.py** se harán una serie de preguntas que le permitirá poder acceder e interactuar con el servidor y otros usuarios a través de él. El login es simplemente colocar el nombre de usuario, esto significa que cualquiera que coloque su nombre creará un nuevo usuario o accederá a una cuenta creada.

**Para conectar un tercer cliente** se debe ejecutar la línea `python .\Client\ClientOut.py` desde la raíz de la actividad 1 (*\act2*), además es necesario introducir la IP mostrada por el servidor de la imagen de rabbit cuando realiza alguna conexión con un cliente, de esta manera ya podrá realizar cualquiera de las funciones mostradas en el menú.

#### Obención de la IP
una vez ejecutado el container de rabbit este será capaz de aceptar conexiones, al hacerlo imprime algunas líneas que son del estilo:

```rabbit_1     | 2020-01-07 04:46:27.371 [info] <0.613.0> accepting AMQP connection <0.613.0> (172.31.52.178:53888 -> 172.31.60.146:5672)```

De estas líneas lo que nos interesa es lo quee está después de la flecha, la ip número ***172.31.60.146*** es la que se necesitaría introducir en esta ocasión para poder conectarnos a rabbit desde una terminal externa a docker (la ip para ClientOut).

**Nota:** el número de ip puede variar entre ejecución y ejecución por lo que es aconsejable que se obtenga la ip de la línea de conexión cada vez que se quiera conectar un nuevo cliente desde afuera.

> Otra manera de obtener la ip es mirando al rededor de la línea `218` del json que caracteriza al **container** de rabbit, allí la ip se denota como `"IPAddress": "172.31.60.146"`. Recordar que la ip cambia entre ejecuciones de docker-compose run, así que se debe revisar esta línea una vez haya inicializado por completo rabbit.

## Ejemplo del menú

 | What would you like to do?

 | 1 - Write and Send a Message

 | 2 - View received messages

 | 3 - View sent messages

 | 4 - View the full list of Clients of the server

 | 0 - Logout

 | Your choice: 3

 ## Integrantes:

- Sebastián Alvarado A. 201673580-1
- Felipe González G. 201673616-6

*La demora con los plazos se debió a problemas e inconvenientes personales, por favor contactar a Sebastián con el correo sebastian.alvaradoa@sansano.usm.cl para discutir al respecto de la evaluación.*