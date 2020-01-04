# Dist2

### Consideraciones generales:

Para cada una de las actividades existe un archivo "docker-compose.yml", por lo que dependiendo de la actividad que se quiera ejecutar, basta con meterse dentro de la carpeta *"Act1"* o *"Act2"* y ejecutar los comandos "docker-compose build" y "docker-compose up".

(Tal y como está la tarea funciona, dado que no se debiesen cambiar los input de esta tarea no deberían haber problemas, y si llegasen a ocurrir se hablará en alguna instancia futura)
(Solo se ha probado la tarea en w10)

## Actividad 1 (Act1)

Para detener la ejecución se debe hacerlo forzándola presionando la combinación CTRL+C en la terminal donde se está ejecutando. **NOTA:** Ya que para realizar la simulación entre los dos clientes y el servidor se utilizó una función que usaba un ***random*** es necesario esperar a que terminen (esperar a ver *c1 exited with code 0* o *c2 exited...*) para poder forzar la detención "correctamente" (aun así mientras se simula se puede agregar un tercer cliente desde afuera). 

Para la primera actividad existen dos tipos de aplicaciones ("servidor" y "cliente") que se encuentran en los directorios "Server" y "Client" respectivamente. Dentro de cada una de estos directorios, existen los archivos "Dockerfile", y el código python de las aplicaciones correspondientes. 

Ya que además era necesario utilizar el protocolo RPC, se utiliza un archivo .proto que genera los archivos *Act1_pb2.py* y *Act1_pb2_grpc.py* y por comodidad se dejaron en la carpeta raíz de esta actividad. Para generar estos archivos es necesario tener instaladas las librerías grpc y grpc-tools.

### Servidor

Dentro de la carpeta Server solo existe un archivo .py que es el que básicamente contiene todo el código de este, por otro lado notar que además este depende de los 2 archivos **Act_pb2**. 
Para que funciones correctamente es necesario que exista previamente el archivo *log.txt*. En él se encontrá el "log" de los mensajes recibidos por el servidor.

**Cuando el servidor parta se mostrará por pantalla su IP, esta será la que se deberá usar para conectarse a él manualmente cuando se quiera agregar un tercer o cuarto cliente.**

### Cliente

Dentro de la carpeta Client existen dos archivos para el *Cliente*: **Client.py** es el archivo que se utiliza para realizar la simulación de la interacción con el servidor; por otro lado está **ClientOut.py** que es el que se deberá ejecutar si es que se quisiera agregar un tercer cliente al servidor. Por último se creó una carpeta *act1* que contiene una copia de los archivos **Act_pb2** necesarios para que el cliente que se conecte desde afuera se pueda ejecutar.

**Para conectar un tercer cliente** se debe ejecutar la línea `python .\Client\ClientOut.py` desde la raíz de la actividad 1 (*\act1*), además es necesario introducir la IP mostrada por el servidor al inicio de su ejecución cuando sea solicitado por el cliente, de esta manera ya podrá realizar cualquiera de las funciones mostradas en el menú. 

#### Ejemplo del menú

 | What would you like to do?
 | 1 - Write and Send a Message
 | 2 - View received messages
 | 3 - View sent messages
 | 4 - View the full list of Clients of the server
 | 0 - Logout
 | Your choice: 3

 ## Actividad 2 (Act2)

 Será subida pronto...

 ## Integrantes:

- Sebastián Alvarado A. 201673580-1
- Felipe González G. 201673616-6