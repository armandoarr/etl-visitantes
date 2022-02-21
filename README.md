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

MYSQL_ROOT_PASSWORD=password
MYSQL_DB=mydb
MYSQL_USER=root
MYSQL_HOST=mysql-local:3306

y ejecutar el script

```
$ python file_processor.py
```


