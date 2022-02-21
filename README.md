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
