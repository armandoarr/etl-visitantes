# ETL Visitantes

para construir la base de datos mysql y correr el procesamiento de datos ejecutar

```
$ docker-compose up --build mysql-local procesador
```

Para levantar la BD y ejecutar el proceso manualmente ejecutar

```
$ docker-compose up --build mysql-local
```
exportar las variables de ambiente

```
MYSQL_ROOT_PASSWORD=password
MYSQL_DB=mydb
MYSQL_USER=root
MYSQL_HOST=mysql-local:3306
```

y ejecutar el script

```
$ python file_processor.py
```

El proceso se realiza en 3 etapas:

En la primera se descargan los archivos y se verifica que tengan el formato adecuado.

En la segunda etapa se extrae la información de los archivos y se clasifican los registros en válidos e inválidos según los criterios establecidos (fechas, email).

Finalmente, en la última etapa se hacen las inserciones correspondientes en base de datos y se crean los respaldos en el archivo zip. También se eliminan los archivos cargados.

Los registros de la bitácora se encuentran en la carpeta logs.


La idea es que el proceso se ejecute diariamente por medio de un cronjob o similar, y la persona a cargo de la ejecución sólo consulte los logs para
asegurarse de que todo salió bien, en caso de errores, conocer las variables de ambiente pueden ser útiles para hacer debug, acceder a la BD y saber en que parte del
código se ejecuta cada etapa.

Para liberar este proceso en producción, un primer paso sería eliminar todos los elementos hardcodeados (rutas, contraseñas, etcétera) y cargarlas como
variables de ambiente donde sea que se vaya a ejecutar este proceso.

Finalmente, considerando incluir tecnologías de Big Data, el flujo no debería cambiar mucho. Quizá utilizar alguna herramienta como spark o algo
diseñado para manejar grandes cantidades de datos, en lugar de python puro y duro. Lo que habría que considerar es en que momento hacer ese cambio
y como realizar y administrar las particiones de los datos.
