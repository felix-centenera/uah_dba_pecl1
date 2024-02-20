

* Preparar Sistema

lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 22.04.3 LTS
Release:        22.04
Codename:       jammy

sudo apt update
sudo apt install gnupg2 wget vim


* Instalar  POSTGRESQL 16.1

```
References: 
https://dev.to/rainbowhat/postgresql-16-installation-on-ubuntu-2204-51ia
https://dba.stackexchange.com/questions/83984/connect-to-postgresql-server-fatal-no-pg-hba-conf-entry-for-host

TIP: ES posible que necesuite permitir conexión md5
```

```
sudo sed -i '/^host/s/ident/md5/' /etc/postgresql/16/main/pg_hba.conf
sudo sed -i '/^local/s/peer/trust/' /etc/postgresql/16/main/pg_hba.conf
echo "host all all 0.0.0.0/0 md5" | sudo tee -a /etc/postgresql/16/main/pg_hba.conf
```

```
apt-get update
```

```
apt install gnupg2 wget vim
```

```
sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
```

```
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg 
```

```
apt update
```

```
apt install postgresql-16 postgresql-contrib-16
```

```
systemctl start postgresql
```

```
systemctl enable postgresql
```

```
vi /etc/postgresql/16/main/postgresql.conf

 listen_addresses = '*'
```

```
systemctl restart postgresql
```

```
sudo ufw allow 5432/tcp
```

```
sudo -u postgres psql
```

```
 ALTER USER postgres PASSWORD 'VeryStronGPassWord@1137';
 ALTER USER postgres PASSWORD 'uah';
```

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------



Cuestión 0. Configurar el fichero de Error Reporting and Logging de PostgreSQL para
que aparezcan recogidas las sentencias SQL DDL (Lenguaje de Definición de Datos) +
DML (Lenguaje de Manipulación de Datos) generadas en dicho fichero. No se pide
activar todas las sentencias. No activar la duración de la consulta. También se debe de
configurar el log para que en el comienzo de la línea de registro de la información del
log (“line prefix”) aparezcan vuestros DNI’s y el nombre del host con su puerto. ¿Cómo
se ha realizado la configuración?


Activar la recogida de logs:
```
vi /etc/postgresql/16/main/postgresql.conf
logging_collector = on
```

Activar la recogida de  de sentencias DDL y DML:
```
vi /etc/postgresql/16/main/postgresql.conf
log_statement = 'mod'
```

Activar line prefix para aparación de DNI:
```
vi /etc/postgresql/16/main/postgresql.conf
log_line_prefix = 'XXXXXX %r'
```

```
systemctl restart postgresql
```

```
systemctl status postgresql
```

Comprobar la activación de registros y campos:

```
tail -f  /var/lib/postgresql/16/main/log/postgresql-2024-02-02_201924.log
```

```
postgres=# create database testlogging;
CREATE DATABASE
postgres=# \c testlogging;
Ahora est√° conectado a la base de datos ¬´testlogging¬ª con el usuario ¬´postgres¬ª.
testlogging=# CREATE TABLE ejemplo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    edad INT,
    email VARCHAR(150)
);
CREATE TABLE
```

```
47224020Y LOG:  starting PostgreSQL 16.2 (Ubuntu 16.2-1.pgdg22.04+1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0, 64-bit
47224020Y LOG:  listening on IPv4 address "0.0.0.0", port 5432
47224020Y LOG:  listening on IPv6 address "::", port 5432
47224020Y LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
47224020Y LOG:  database system was shut down at 2024-02-09 18:18:06 UTC
47224020Y LOG:  database system is ready to accept connections
47224020Y [local]LOG:  statement: create database testlogging;
47224020Y [local]ERROR:  syntax error at or near "c" at character 1
47224020Y [local]STATEMENT:  c testlogging;
47224020Y [local]LOG:  statement: CREATE TABLE ejemplo (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100),
            edad INT,
            email VARCHAR(150)
        );


```

Cuestión 1. Crear una nueva Base de Datos que se llame PL1. Después crear una tabla
camiones con los siguientes campos:
- id_camion: que debe ser el identificador del camión comenzando por 1.
- Matricula: guarda la matrícula española del camión y no se debe repetir.
- Empresa: guarda la empresa de transportes a la que pertenece el camión.
- Kilómetros: guarda los kilómetros que tiene actualmente el camión.
Crear un programa que permita generar 20 millones de registros en un fichero de texto
que pueda ser cargado en la tabla (preferiblemente en Python) con las siguientes
propiedades para los siguientes campos, cuyos valores se deben generar
aleatoriamente.
- Empresa: deben ser valores aleatorios generados de 10000 empresas
disponibles. Una de ellas debe ser UPS.
- Kilómetros: deben ser valores aleatorios generados entre 0 y 500000 km.
Cargar los datos en la tabla y localizar los ficheros relacionados con la tabla. ¿cómo se
localizan? ¿Cuánto ocupan? ¿por qué?


Crear la base de datos PL1:
```
create database PL1;
\c pl1
```

Crear tabla camiones
```
pl1=# CREATE TABLE camiones (
    id_camion SERIAL UNIQUE,
    matricula CHAR(8) PRIMARY KEY,
    empresa VARCHAR(100),
    kilometros INT
);
```



```
pl1=# \dt
         Listado de relaciones
 Esquema |  Nombre  | Tipo  |  Due√±o   
---------+----------+-------+----------
 public  | camiones | tabla | postgres
(1 fila)


pl1=# \d camiones;
                                         Table "public.camiones"
   Column   |          Type          | Collation | Nullable |                   Default                   
------------+------------------------+-----------+----------+---------------------------------------------
 id_camion  | integer                |           | not null | nextval('camiones_id_camion_seq'::regclass)
 matricula  | character(8)           |           | not null | 
 empresa    | character varying(100) |           |          | 
 kilometros | integer                |           |          | 
Indexes:
    "camiones_pkey" PRIMARY KEY, btree (matricula)
    "camiones_id_camion_key" UNIQUE CONSTRAINT, btree (id_camion)
```


```
python3 ./generateRandomDat.py
```

```
pl1=# select * from camiones;
 id_camion | matricula | empresa | kilometros 
-----------+-----------+---------+------------
(0 filas)
```



```
sftp> cd /tmp/
sftp> put 0000.dat
Uploading 0000.dat to /tmp/0000.dat
  100% 943515KB  29484KB/s 00:00:32 
 0000.dat: 1146210490 bytes transferred in 37 seconds (30252 KB/s)
sftp> ls 
0000.dat 

```

```
\copy camiones(id_camion,matricula,empresa,kilometros) FROM '/tmp/0000.dat' DELIMITER ';' CSV
COPY 20000000
```

```
pl1=# SELECT COUNT(*) FROM camiones;
  count   
----------
 20000000
 ```

 ```
 pl1=# select * from camiones LIMIT 20;
 id_camion | matricula |                    empresa                     | kilometros 
-----------+-----------+------------------------------------------------+------------
         1 | JPV6108   | Bats Global Markets, Inc.                      |     173326
         2 | QNA0265   | Itrackr Systems Inc                            |     172546
         3 | VZU4299   | Bonanza Creek Energy, Inc.                     |     106332
         4 | ODA7913   | Bluefire Renewables, Inc.                      |     149317
         5 | JJN8731   | PAN American Goldfields LTD                    |     339413
         6 | CGL0600   | Capital Auto Receivables Asset Trust 2014-3    |     443945
         7 | VNV7626   | Baeta Corp                                     |     445705
         8 | BOO9470   | Gopro, Inc.                                    |     266671
         9 | JRB6039   | Assurance Group Inc.                           |     152561
        10 | GMV9007   | BJS Wholesale Club Inc                         |     433822
        11 | PWE0035   | Parallax Health Sciences, Inc.                 |     137053
        12 | RSU1355   | Frank'S International N.V.                     |     267760
        13 | KWN9954   | Oracle Corp                                    |     464221
        14 | KZM7632   | Dynamic Ventures Corp.                         |     236130
        15 | ASN3844   | Dolphin Digital Media Inc                      |     241064
        16 | DXD2907   | Westmont Resources Inc.                        |      30359
        17 | ZUC1227   | Strats SM Trust FOR IBM Corp SEC Series 2004-7 |     181713
        18 | EGB3244   | Nilam Resources Inc.                           |      28289
        19 | IQR4555   | Timberline Resources Corp                      |     222396
        20 | DPW1547   | Weyerhaeuser CO                                |     223663
(20 filas)
 ```


```
pl1=# select COUNT(*) from camiones where empresa='UPS';
 count 
-------
  2020
(1 row)
 ```



 ```
  vi /etc/postgresql/16/main/postgresql.conf

#------------------------------------------------------------------------------
# FILE LOCATIONS
#------------------------------------------------------------------------------

# The default values of these variables are driven from the -D command-line
# option or PGDATA environment variable, represented here as ConfigDir.

data_directory = '/var/lib/postgresql/16/main'          # use data in another directory
                                        # (change requires restart)
hba_file = '/etc/postgresql/16/main/pg_hba.conf'        # host-based authentication file
                                        # (change requires restart)
ident_file = '/etc/postgresql/16/main/pg_ident.conf'    # ident configuration file
                                        # (change requires restart)

# If external_pid_file is not explicitly set, no extra PID file is written.
external_pid_file = '/var/run/postgresql/16-main.pid'                   # write an extra PID file
                                        # (change requires restart)
#------------------------------------------------------------------------------
 ```

 ```
show data_directory;
       data_directory        
-----------------------------
 /var/lib/postgresql/16/main
(1 fila)
 ```

 ```
 SELECT oid from pg_database WHERE datname='pl1';
  oid  
-------
 16396
(1 fila)
 ```

  ```
 cd /var/lib/postgresql/16/main/base/16396

 ls
112        13391      2601_fsm  2612      2658  2690      2838_fsm  3394_vm   3598      4144  4174
113        13392      2601_vm   2612_fsm  2659  2691      2838_vm   3395      3599      4145  5002
1247       13392_fsm  2602      2612_vm   2660  2692      2839      3429      3600      4146  548
1247_fsm   13392_vm   2602_fsm  2613      2661  2693      2840      3430      3600_fsm  4147  549
1247_vm    13395      2602_vm   2615      2662  2696      2840_fsm  3431      3600_vm   4148  6102
1249       13396      2603      2615_fsm  2663  2699      2840_vm   3433      3601      4149  6104
1249_fsm   1417       2603_fsm  2615_vm   2664  2701      2841      3439      3601_fsm  4150  6106
1249_vm    1418       2603_vm   2616      2665  2702      2995      3440      3601_vm   4151  6110
1255       16471      2604      2616_fsm  2666  2703      2996      3455      3602      4152  6111
1255_fsm   16472      2605      2616_vm   2667  2704      3079      3456      3602_fsm  4153  6112
1255_vm    16472.1    2605_fsm  2617      2668  2753      3079_fsm  3456_fsm  3602_vm   4154  6113
1259       16472_fsm  2605_vm   2617_fsm  2669  2753_fsm  3079_vm   3456_vm   3603      4155  6116
1259_fsm   16472_vm   2606      2617_vm   2670  2753_vm   3080      3466      3603_fsm  4156  6117
1259_vm    16476      2606_fsm  2618      2673  2754      3081      3467      3603_vm   4157  6175
13377      16478      2606_vm   2618_fsm  2674  2755      3085      3468      3604      4158  6176
13377_fsm  174        2607      2618_vm   2675  2756      3118      3501      3605      4159  6228
13377_vm   175        2607_fsm  2619      2678  2757      3119      3502      3606      4160  6229
13380      2187       2607_vm   2619_fsm  2679  2830      3164      3503      3607      4163  6237
13381      2224       2608      2619_vm   2680  2831      3256      3534      3608      4164  6238
13382      2228       2608_fsm  2620      2681  2832      3257      3541      3609      4165  6239
13382_fsm  2328       2608_vm   2650      2682  2833      3258      3541_fsm  3712      4166  826
13382_vm   2336       2609      2651      2683  2834      3350      3541_vm   3764      4167  827
13385      2337       2609_fsm  2652      2684  2835      3351      3542      3764_fsm  4168  828
13386      2579       2609_vm   2653      2685  2836      3379      3574      3764_vm   4169  pg_filenode.map
13387      2600       2610      2654      2686  2836_fsm  3380      3575      3766      4170  pg_internal.init
13387_fsm  2600_fsm   2610_fsm  2655      2687  2836_vm   3381      3576      3767      4171  PG_VERSION
13387_vm   2600_vm    2610_vm   2656      2688  2837      3394      3596      3997      4172
13390      2601       2611      2657      2689  2838      3394_fsm  3597      4143      4173
 ```

 ```
SELECT pg_relation_filepath('camiones'); 
 pg_relation_filepath 
----------------------
 base/16396/16398
(1 row)
 ```

 ```
pl1=# SELECT  relfilenode  FROM   pg_class WHERE  relname = 'camiones';
 relfilenode 
-------------
       16398
(1 row)
 ```
 ```
cd /var/lib/postgresql/16/main/base/16396
du -sh 16398
1.1G    16398
 ```

```
 SELECT pg_size_pretty(pg_total_relation_size('camiones'));
 pg_size_pretty 
----------------
 2614 MB
(1 row)
 ```

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------


 Cuestión 2. Calcular teóricamente el tamaño en bloques que ocupa la relación
camiones tal y como se realiza en clase de teoría. ¿Concuerda con el tamaño en
bloques que nos proporciona PostgreSQL? ¿Cuál es el factor de bloque medio real de
la tabla camiones? ¿Por qué? Realizar una consulta SQL que obtenga ese valor y
comparar con el factor de bloque teórico.


 ```
SELECT  relpages FROM   pg_class WHERE  relname = 'camiones';
 relpages 
----------
   180752
(1 row)
 ```

 ```
SELECT COUNT(*) FROM camiones; 
  count   
----------
 20000000
(1 row)
 ```

 ```
SHOW block_size;
 block_size 
------------
 8192
(1 row)
 ```


 ```
 CREATE TABLE camiones1 (
    id_camion SERIAL UNIQUE,
    matricula CHAR(8) PRIMARY KEY,
    empresa CHAR(100),
    kilometros INT
);
 ```

 ``` 
\copy camiones1(id_camion,matricula,empresa,kilometros) FROM '/tmp/0000.dat' DELIMITER ';' CSV
 ```

 ```
SELECT oid::regclass AS tbl, relpages FROM   pg_class WHERE  relname = 'camiones1'; 
 ```

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------


Cuestión 3. Realizar una consulta que muestre la matrícula de los camiones que tengan
200000 km. ¿Cuántas tuplas se obtienen y cuántos bloques se leen por Postgres? ¿Por
qué? Comparar con los resultados obtenidos al aplicar el método visto en teoría.

 ```
select  COUNT(*) from camiones where kilometros=20000 ;
 count 
-------
    37
(1 row)

EXPLAIN select  COUNT(*) from camiones where kilometros=20000 ;

EXPLAIN select  COUNT(*) from camiones where kilometros=20000 ;
                                       QUERY PLAN                                        
-----------------------------------------------------------------------------------------
 Finalize Aggregate  (cost=285933.64..285933.65 rows=1 width=8)
   ->  Gather  (cost=285933.42..285933.63 rows=2 width=8)
         Workers Planned: 2
         ->  Partial Aggregate  (cost=284933.42..284933.43 rows=1 width=8)
               ->  Parallel Seq Scan on camiones  (cost=0.00..284933.38 rows=18 width=0)
                     Filter: (kilometros = 20000)
 JIT:
   Functions: 6
   Options: Inlining false, Optimization false, Expressions true, Deforming true
(9 rows)
 ```


 ```
SELECT * FROM pg_statio_all_tables WHERE relname='camiones'; 
``` 

si nos vamos a la columna heap_blks_read y heap_blks_hit podemos saber que en total ha leido 81730 + 480 = 82018 bloques. Por lo que el gdb ha realizado un lectura secuencial de la tabla.


----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------



Cuestión 4. Crear una tabla camiones2 cuyas tuplas estén ordenadas físicamente por
el campo km de menor a mayor y que tenga la misma información. Cargar el mismo
fichero de datos creado en la cuestión1. Indicar el proceso de generación de dicha tabla
ordenada. ¿Cuántos bloques ocupa la tabla ahora? ¿Hay algún cambio? ¿Por qué?


 ```
CREATE TABLE camiones2 (
    id_camion SERIAL UNIQUE,
    matricula CHAR(8) PRIMARY KEY,
    empresa VARCHAR(100),
    kilometros INT
);
 ```

 ```
INSERT INTO camiones2 select * from camiones ORDER BY(kilometros);
INSERT 0 20000000
 ```


```
pl1=# SELECT COUNT(*) FROM camiones2; 
  count   
----------
 20000000
(1 row)

```

El número de bloques es muy similar:
```
SELECT  relpages FROM   pg_class WHERE  relname = 'camiones';
 relpages 
----------
   180752
(1 row)
 ```

 ```
 SELECT  relpages FROM   pg_class WHERE  relname = 'camiones2';
 relpages 
----------
   180626
(1 row)
 ```

El tamaño la tabla camiones2 es mayor.
 ```
pl1=# SELECT pg_size_pretty(pg_total_relation_size('camiones'));
 pg_size_pretty 
----------------
 2614 MB
(1 row)
 ```

 ```
pl1=# SELECT pg_size_pretty(pg_total_relation_size('camiones2'));
 pg_size_pretty 
----------------
 2756 MB
(1 row)
 ```




Realmente la diferencia la tenemos no la tenemos en la tabla en sí.

 ```
pl1=#  SELECT pg_size_pretty( pg_table_size('camiones') );
 pg_size_pretty 
----------------
 1413 MB
(1 row)
 ```

  
```
pl1=#  SELECT pg_size_pretty( pg_table_size('camiones2') );
 pg_size_pretty 
----------------
 1412 MB
(1 row)
 ```


 ```
 \dt+
                                      List of relations
 Schema |   Name    | Type  |  Owner   | Persistence | Access method |  Size   | Description 
--------+-----------+-------+----------+-------------+---------------+---------+-------------
 public | camiones  | table | postgres | permanent   | heap          | 1413 MB | 
 public | camiones2 | table | postgres | permanent   | heap          | 1412 MB | 
 ```


La diferencia la tenemos en los indices.
 ```
\di+ 
                                                  List of relations
 Schema |          Name           | Type  |  Owner   |   Table   | Persistence | Access method |  Size  | Description 
--------+-------------------------+-------+----------+-----------+-------------+---------------+--------+-------------
 public | camiones2_id_camion_key | index | postgres | camiones2 | permanent   | btree         | 572 MB | 
 public | camiones2_pkey          | index | postgres | camiones2 | permanent   | btree         | 772 MB | 
 public | camiones_id_camion_key  | index | postgres | camiones  | permanent   | btree         | 428 MB | 
 public | camiones_pkey           | index | postgres | camiones  | permanent   | btree         | 773 MB | 
 ```


Index para camiones1= 428 + 773= 1201
Index para camiones2= 572 + 772=1314

Ha crecido el indice de tipo camiones_id_camion_key. Y tiene sentido, ya que antes al estar ordenado el indice
El indice pasa de ser primario a secundario y campo no clave, ya que los valores van a estar repetidos y además desordenados, esto  conlleva el uso de mas cajones y punteros, incrementando el peso.



 ```

SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'camiones';


SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'camiones2';


SELECT indexname, pg_size_pretty(pg_indexes_size('camiones_pkey')) AS index_size
FROM pg_indexes
WHERE indexname = 'camiones_pkey';

SELECT indexname, pg_size_pretty(pg_indexes_size('camiones_id_camion_key')) AS index_size
FROM pg_indexes
WHERE indexname = 'camiones_id_camion_key';



SELECT indexname, pg_size_pretty(pg_indexes_size('camiones2_pkey')) AS index_size
FROM pg_indexes
WHERE indexname = 'camiones2_pkey';

SELECT indexname, pg_size_pretty(pg_indexes_size('camiones2_id_camion_key')) AS index_size
FROM pg_indexes
WHERE indexname = 'camiones2_id_camion_key';
 ```


 SELECT pg_size_pretty( pg_table_size('camiones') );

 SELECT relpages FROM pg_class WHERE relname = 'camiones'

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------

Cuestión 5. Repetir la cuestión 3 sobre la tabla camiones2 y comparar los resultados
obtenidos indicando las conclusiones obtenidas.

  Cuestión 3. Realizar una consulta que muestre la matrícula de los camiones que tengan
  200000 km. ¿Cuántas tuplas se obtienen y cuántos bloques se leen por Postgres? ¿Por
  qué? Comparar con los resultados obtenidos al aplicar el método visto en teoría.


 ```
select  COUNT(*) from camiones2 where kilometros=20000 ;
 count 
-------
    37
(1 row)
 ```


 ```
 pl1=# explain (analyse, buffers) select  COUNT(*) from camiones2 where kilometros=20000 ;
                                                               QUERY PLAN                                                                
-----------------------------------------------------------------------------------------------------------------------------------------
 Finalize Aggregate  (cost=285794.54..285794.55 rows=1 width=8) (actual time=481.682..485.669 rows=1 loops=1)
   Buffers: shared hit=698 read=179928
   ->  Gather  (cost=285794.32..285794.53 rows=2 width=8) (actual time=481.517..485.650 rows=3 loops=1)
         Workers Planned: 2
         Workers Launched: 2
         Buffers: shared hit=698 read=179928
         ->  Partial Aggregate  (cost=284794.32..284794.33 rows=1 width=8) (actual time=468.517..468.519 rows=1 loops=3)
               Buffers: shared hit=698 read=179928
               ->  Parallel Seq Scan on camiones2  (cost=0.00..284794.10 rows=88 width=0) (actual time=321.732..468.481 rows=12 loops=3)
                     Filter: (kilometros = 20000)
                     Rows Removed by Filter: 6666654
                     Buffers: shared hit=698 read=179928
 Planning Time: 0.053 ms
 JIT:
   Functions: 14
   Options: Inlining false, Optimization false, Expressions true, Deforming true
   Timing: Generation 0.908 ms, Inlining 0.000 ms, Optimization 0.480 ms, Emission 10.232 ms, Total 11.621 ms
 Execution Time: 485.979 ms
(18 rows)
 ```
 hit=698 + read=179928= 180626



 ```
 SELECT  relpages FROM   pg_class WHERE  relname = 'camiones2';
 relpages 
----------
   180626
(1 row)
 ```

Es decir, recorreremos todos los bloques, esta realizando una busqueda secuencial. Aunque el campo este ordenado, no parece que las estádisticas le indiquen que es mejor cualquier otro algorítmo de busqueda. Necesitariamos crear un indice por el campo kilometros con el fin de utilizar busquedas no secuenciales.



Cuestión 6. Borrar 2000000 tuplas de la tabla camiones de manera aleatoria usando
el valor del campo id_camion. ¿Qué es lo que ocurre físicamente en la base de datos?
¿Se observa algún cambio en el tamaño de la tabla y estructuras asociadas a ella? ¿Por
qué? Adjuntar el código de borrado.


 ```
pl1=#  SELECT pg_size_pretty( pg_table_size('camiones') );
 pg_size_pretty 
----------------
 1413 MB
(1 row)
 ```

 ```
pl1=# SELECT COUNT(*) FROM camiones; 
  count   
----------
 20000000
(1 row)
```

```
pl1=#  \dt+
                                      List of relations
 Schema |   Name    | Type  |  Owner   | Persistence | Access method |  Size   | Description 
--------+-----------+-------+----------+-------------+---------------+---------+-------------
 public | camiones  | table | postgres | permanent   | heap          | 1413 MB | 
 ```


 ```
 \di+ 
                                                  List of relations
 Schema |          Name           | Type  |  Owner   |   Table   | Persistence | Access method |  Size  | Description 
--------+-------------------------+-------+----------+-----------+-------------+---------------+--------+-------------
 public | camiones_id_camion_key  | index | postgres | camiones  | permanent   | btree         | 428 MB | 
 public | camiones_pkey           | index | postgres | camiones  | permanent   | btree         | 773 MB | 
 ```


```
DELETE FROM camiones WHERE id_camion IN(SELECT id_camion FROM camiones ORDER BY random() LIMIT 2000000);
 ```

```
pl1=# SELECT pg_size_pretty( pg_table_size('camiones') );
 pg_size_pretty 
----------------
 1413 MB
(1 row)
```

```
 SELECT COUNT(*) FROM camiones; 
  count   
----------
 18000000
(1 row)
```

```
pl1=# \dt+
                                      List of relations
 Schema |   Name    | Type  |  Owner   | Persistence | Access method |  Size   | Description 
--------+-----------+-------+----------+-------------+---------------+---------+-------------
 public | camiones  | table | postgres | permanent   | heap          | 1413 MB | 
 ```

```
 pl1=#  \di+ 
                                                  List of relations
 Schema |          Name           | Type  |  Owner   |   Table   | Persistence | Access method |  Size  | Description 
--------+-------------------------+-------+----------+-----------+-------------+---------------+--------+-------------
 public | camiones_id_camion_key  | index | postgres | camiones  | permanent   | btree         | 428 MB | 
 public | camiones_pkey           | index | postgres | camiones  | permanent   | btree         | 773 MB | 
 ```

 Observamos que no aparecen esas filas, pero el espacio de ocupado es el mismo, esto se debe a que los punteros que apuntaban a la información estan en NULL; pero la información sigue estando en el disco. Observerse que permance el mismo espacio ocupado para tabla e indices asociados.

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------



Cuestión 7. En la situación anterior, ¿Qué operaciones se pueden aplicar a la base de
datos PL1 para optimizar el rendimiento de esta? Aplicarlas de tal manera que se
recupere el mayor espacio posible. Comentar cuál es el resultado final y qué es lo que
ocurre físicamente.

Como mencionabamos en el apartado anterior, cuando se borrar los datos  Postgresql solo nos marca las filas como espacio libre, si quieremos eliminar los datos realmente, debemos hacer uso del proceso VACUUM.

```
VACUUM camiones;
```

```
pl1=#  SELECT COUNT(*) FROM camiones; 
  count   
----------
 18000000
(1 row)
```
```
SELECT pg_size_pretty( pg_table_size('camiones') );
 pg_size_pretty 
----------------
 1412 MB
(1 row)
```

```
pl1=# \dt+
                                      List of relations
 Schema |   Name    | Type  |  Owner   | Persistence | Access method |  Size   | Description 
--------+-----------+-------+----------+-------------+---------------+---------+-------------
 public | camiones  | table | postgres | permanent   | heap          | 1412 MB | 
```

```
pl1=# \di+
                                                  List of relations
 Schema |          Name           | Type  |  Owner   |   Table   | Persistence | Access method |  Size  | Description 
--------+-------------------------+-------+----------+-----------+-------------+---------------+--------+-------------
 public | camiones_id_camion_key  | index | postgres | camiones  | permanent   | btree         | 428 MB | 
 public | camiones_pkey           | index | postgres | camiones  | permanent   | btree         | 773 MB | 
```


```
pl1=# VACUUM FULL;
VACUUM
```

Realizamos un VACUUM FULL para generar un proceso de limpieza mas profundo, con el que vemos que se libera bastante mas espacio.

```
pl1=# SELECT pg_size_pretty( pg_table_size('camiones') );
 pg_size_pretty 
----------------
 1271 MB
(1 row)
```

```
pl1=# \dt+
                                      List of relations
 Schema |   Name    | Type  |  Owner   | Persistence | Access method |  Size   | Description 
--------+-----------+-------+----------+-------------+---------------+---------+-------------
 public | camiones  | table | postgres | permanent   | heap          | 1271 MB | 
```

```
pl1=# \di+
                                                  List of relations
 Schema |          Name           | Type  |  Owner   |   Table   | Persistence | Access method |  Size  | Description 
--------+-------------------------+-------+----------+-----------+-------------+---------------+--------+-------------
 public | camiones_id_camion_key  | index | postgres | camiones  | permanent   | btree         | 386 MB | 
 public | camiones_pkey           | index | postgres | camiones  | permanent   | btree         | 541 MB | 
```


----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------


Cuestión 8. Crear una nueva tabla denominada camiones3 con los mismos campos
que la cuestión 1 y que esté particionada por el campo kilómetros con la función hash
kilómetros mod 20. Insertar los datos del fichero de datos generado en la cuestión
1. Explicar el proceso seguido y comentar qué es lo que ha ocurrido físicamente en la
base de datos. ¿Cuándo será útil el particionamiento? ¿Cuántos bloques ocupa cada
una de las particiones? ¿Por qué? Comparar con el número bloques que se obtendría
teóricamente utilizando el procedimiento visto en teoría.


Crear tabla camiones3


```
CREATE TABLE camiones3 (
    id_camion SERIAL,
    matricula CHAR(8),
    empresa VARCHAR(100),
    kilometros INT,
    PRIMARY KEY (id_camion, matricula, kilometros)
) PARTITION BY HASH(kilometros);
```


```
\d camiones3;
                                   Partitioned table "public.camiones3"
   Column   |          Type          | Collation | Nullable |                   Default                    
------------+------------------------+-----------+----------+----------------------------------------------
 id_camion  | integer                |           | not null | nextval('camiones3_id_camion_seq'::regclass)
 matricula  | character(8)           |           | not null | 
 empresa    | character varying(100) |           |          | 
 kilometros | integer                |           | not null | 
Partition key: HASH (kilometros)
Indexes:
    "camiones3_pkey" PRIMARY KEY, btree (id_camion, matricula, kilometros)
Number of partitions: 0
```


```
CREATE TABLE camiones3_p0 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 0);
CREATE TABLE camiones3_p1 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 1);
CREATE TABLE camiones3_p2 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 2);
CREATE TABLE camiones3_p3 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 3);
CREATE TABLE camiones3_p4 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 4);
CREATE TABLE camiones3_p5 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 5);
CREATE TABLE camiones3_p6 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 6);
CREATE TABLE camiones3_p7 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 7);
CREATE TABLE camiones3_p9 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 9);
CREATE TABLE camiones3_p10 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 10);
CREATE TABLE camiones3_p11 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 11);
CREATE TABLE camiones3_p12 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 12);
CREATE TABLE camiones3_p13 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 13);
CREATE TABLE camiones3_p14 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 14);
CREATE TABLE camiones3_p15 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 15);
CREATE TABLE camiones3_p16 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 16);
CREATE TABLE camiones3_p17 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 17);
CREATE TABLE camiones3_p18 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 18);
CREATE TABLE camiones3_p19 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 19);
```

```
 \d+ camiones3;
                                                              Partitioned table "public.camiones3"
   Column   |          Type          | Collation | Nullable |                   Default                    | Storage  | Compression | Stats target | Description 
------------+------------------------+-----------+----------+----------------------------------------------+----------+-------------+--------------+-------------
 id_camion  | integer                |           | not null | nextval('camiones3_id_camion_seq'::regclass) | plain    |             |              | 
 matricula  | character(8)           |           | not null |                                              | extended |             |              | 
 empresa    | character varying(100) |           |          |                                              | extended |             |              | 
 kilometros | integer                |           | not null |                                              | plain    |             |              | 
Partition key: HASH (kilometros)
Indexes:
    "camiones3_pkey" PRIMARY KEY, btree (id_camion, matricula, kilometros)
Partitions: camiones3_p0 FOR VALUES WITH (modulus 20, remainder 0),
            camiones3_p1 FOR VALUES WITH (modulus 20, remainder 1),
            camiones3_p10 FOR VALUES WITH (modulus 20, remainder 10),
            camiones3_p11 FOR VALUES WITH (modulus 20, remainder 11),
            camiones3_p12 FOR VALUES WITH (modulus 20, remainder 12),
            camiones3_p13 FOR VALUES WITH (modulus 20, remainder 13),
            camiones3_p14 FOR VALUES WITH (modulus 20, remainder 14),
            camiones3_p15 FOR VALUES WITH (modulus 20, remainder 15),
            camiones3_p16 FOR VALUES WITH (modulus 20, remainder 16),
            camiones3_p17 FOR VALUES WITH (modulus 20, remainder 17),
            camiones3_p18 FOR VALUES WITH (modulus 20, remainder 18),
            camiones3_p19 FOR VALUES WITH (modulus 20, remainder 19),
            camiones3_p2 FOR VALUES WITH (modulus 20, remainder 2),
            camiones3_p3 FOR VALUES WITH (modulus 20, remainder 3),
            camiones3_p4 FOR VALUES WITH (modulus 20, remainder 4),
            camiones3_p5 FOR VALUES WITH (modulus 20, remainder 5),
            camiones3_p6 FOR VALUES WITH (modulus 20, remainder 6),
            camiones3_p7 FOR VALUES WITH (modulus 20, remainder 7),
            camiones3_p8 FOR VALUES WITH (modulus 20, remainder 8),
            camiones3_p9 FOR VALUES WITH (modulus 20, remainder 9)
```

```
pl1=# \copy camiones3(id_camion,matricula,empresa,kilometros) FROM '/tmp/0000.dat' DELIMITER ';' CSV
COPY 20000000
```

```
pl1=# SELECT COUNT(*) FROM camiones3; 
  count   
----------
 20000000
(1 row)
```


Vemos lo que ocupan por bloque
```
SELECT  relname, relpages FROM   pg_class WHERE  relname = 'camiones3_p0' or  relname = 'camiones3_p1' 
or relname = 'camiones3_p2'
or relname = 'camiones3_p3'
or relname = 'camiones3_p4'
or relname = 'camiones3_p5'
or relname = 'camiones3_p6'
or relname = 'camiones3_p7'
or relname = 'camiones3_p8'
or relname = 'camiones3_p9'
or relname = 'camiones3_p10'
or relname = 'camiones3_p11'
or relname = 'camiones3_p12'
or relname = 'camiones3_p13'
or relname = 'camiones3_p14'
or relname = 'camiones3_p15'
or relname = 'camiones3_p16'
or relname = 'camiones3_p17'
or relname = 'camiones3_p18'
or relname = 'camiones3_p19';

  relname    | relpages 
---------------+----------
 camiones3_p0  |     9024
 camiones3_p1  |     9088
 camiones3_p2  |     9024
 camiones3_p3  |     9088
 camiones3_p4  |     9088
 camiones3_p5  |     9024
 camiones3_p6  |     9088
 camiones3_p7  |     9024
 camiones3_p8  |     9088
 camiones3_p9  |     9216
 camiones3_p10 |     9024
 camiones3_p11 |     9152
 camiones3_p12 |     9024
 camiones3_p13 |     9088
 camiones3_p14 |     9088
 camiones3_p15 |     8960
 camiones3_p16 |     9088
 camiones3_p17 |     9088
 camiones3_p18 |     9024
 camiones3_p19 |     9088
(20 rows)
 ```

 ```
pl1=# SELECT  SUM(relpages) AS total_relpages FROM   pg_class WHERE  relname = 'camiones3_p0' or  relname = 'camiones3_p1' 
or relname = 'camiones3_p2'
or relname = 'camiones3_p3'
or relname = 'camiones3_p4'
or relname = 'camiones3_p5'
or relname = 'camiones3_p6'
or relname = 'camiones3_p7'
or relname = 'camiones3_p8'
or relname = 'camiones3_p9'
or relname = 'camiones3_p10'
or relname = 'camiones3_p11'
or relname = 'camiones3_p12'
or relname = 'camiones3_p13'
or relname = 'camiones3_p14'
or relname = 'camiones3_p15'
or relname = 'camiones3_p16'
or relname = 'camiones3_p17'
or relname = 'camiones3_p18'
or relname = 'camiones3_p19';
 total_relpages 
----------------
         181376
(1 row)
 ```

Si lo calculamos de forma teórica.

 La función hash mod 20 nos crea 20 particiones. N=20
 La media de registros que tendrá cada partición es de = nr/N= 20000000/20=1000000 registros por partición.
 
 VARCHAR 100 estimamos que ocupa la mitado 50bytes.

 LR= 4+8+50+4=66byes
 fr=⌊B.util/LR⌋=8192/66=125 registros por bloque

br=⌈1000000/125⌉=80000 bloques cada partoción
Como tenemos 20 particiones. Ocupara 20 * 80000= 160000 bloques

Hay que tener en cuenta que nuestro VARCHAR(100) del nombre de empresa hace que sea dínamica la ocupación del campo, de ahí las posibles variaciones.


Utilizar particiones es útil cuando manejanmos grandes cantidades de datos. Al implementarlo mejoramos el rendimiento de las consultas, al estar ordenados los datos por conjuntos, accedemos a la parte que nos interesa. Distribuir la carga de datos entre particiones también mejora el rendimiento al no sobre cargar discos, lo cual esta relacionado con la escalabilidad, podemos distribuir los datos entre distintos discos permitiendonos escalar la capacidad de la base de datos de manera más uniforme y permitir una distribución de carga más equitativa en el sistema.


----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------


Cuestión 9. Repetir la cuestión 3 sobre la tabla camiones3 y comparar los resultados
obtenidos con lo visto anteriormente en las tablas camiones y camiones2
obteniendo conclusiones sobre el método de partición.


Cuestión 3. Realizar una consulta que muestre la matrícula de los camiones que tengan
200000 km. ¿Cuántas tuplas se obtienen y cuántos bloques se leen por Postgres? ¿Por
qué? Comparar con los resultados obtenidos al aplicar el método visto en teoría.

 ```
pl1=# select  COUNT(*) from camiones3 where kilometros=20000 ;
 count 
-------
    37
(1 row)
 ```

```
explain (analyse, buffers) select  COUNT(*) from camiones3 where kilometros=20000 ;
                                                                    QUERY PLAN                                                                     
---------------------------------------------------------------------------------------------------------------------------------------------------
 Finalize Aggregate  (cost=15214.94..15214.95 rows=1 width=8) (actual time=37.334..40.973 rows=1 loops=1)
   Buffers: shared hit=360 read=8664
   ->  Gather  (cost=15214.72..15214.93 rows=2 width=8) (actual time=37.252..40.967 rows=3 loops=1)
         Workers Planned: 2
         Workers Launched: 2
         Buffers: shared hit=360 read=8664
         ->  Partial Aggregate  (cost=14214.72..14214.73 rows=1 width=8) (actual time=26.247..26.247 rows=1 loops=3)
               Buffers: shared hit=360 read=8664
               ->  Parallel Seq Scan on camiones3_p10 camiones3  (cost=0.00..14214.68 rows=17 width=0) (actual time=2.699..26.236 rows=12 loops=3)
                     Filter: (kilometros = 20000)
                     Rows Removed by Filter: 332191
                     Buffers: shared hit=360 read=8664
 Planning Time: 0.114 ms
 Execution Time: 40.998 ms
(14 rows)
```

HIT=360 + read=8664 = 9024 bloques.


```
 SELECT  SUM(relpages) AS total_relpages FROM   pg_class WHERE  relname = 'camiones3_p0' or  relname = 'camiones3_p1' 
or relname = 'camiones3_p2'
or relname = 'camiones3_p3'
or relname = 'camiones3_p4'
or relname = 'camiones3_p5'
or relname = 'camiones3_p6'
or relname = 'camiones3_p7'
or relname = 'camiones3_p8'
or relname = 'camiones3_p9'
or relname = 'camiones3_p10'
or relname = 'camiones3_p11'
or relname = 'camiones3_p12'
or relname = 'camiones3_p13'
or relname = 'camiones3_p14'
or relname = 'camiones3_p15'
or relname = 'camiones3_p16'
or relname = 'camiones3_p17'
or relname = 'camiones3_p18'
or relname = 'camiones3_p19';
 total_relpages 
----------------
         181376
(1 row)
```

Camiones 3 ocupa 181376 bloques, como podemos ver,  para la consulta solicitada se leen 9024 bloques, lo cual nos indica que ya no estamos realizando una consulta secuencial. 9024 es el número de bloques que tiene cada partición, con esto queda demostrado que solo estamos recuperando una partición para realizar la consulta. Para las otras tablas camiones, recuperabamos todos los bloques, realizando una consulta secuencial.



Indexación de PostgreSQL
PostgreSQL soporta indexación definida por el usuario para ayudar a acelerar ciertas
consultas. Entre otros tipos de índices soporta árboles y hash. En este apartado se va a
trabajar sobre ambos tipos de índices, pudiendo observar cómo se organizan
internamente y su funcionamiento.


----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------

Cuestión 10. Borrar todas las tablas camiones, camiones2 y camiones3. Crear una
nueva tabla que se llama camiones como en la cuestión 1 y que tenga cargados todos
los datos del fichero de texto generado.


Borrar las tablas:
```
pl1=# drop table camiones2;
DROP TABLE
pl1=# drop table camiones3;
DROP TABLE
pl1=# drop table camiones;
DROP TABLE
pl1=# 
```

```
pl1=# \d
Did not find any relations.
```

Crear tabla camiones
```
pl1=# CREATE TABLE camiones (
    id_camion SERIAL UNIQUE,
    matricula CHAR(8) PRIMARY KEY,
    empresa VARCHAR(100),
    kilometros INT
);
```

```
\copy camiones(id_camion,matricula,empresa,kilometros) FROM '/tmp/0000.dat' DELIMITER ';' CSV
COPY 20000000
```

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------


Cuestión 11. Crear un índice de tipo árbol para kilómetros. ¿Dónde se almacena
físicamente ese índice? ¿Qué tamaño tiene? ¿Cuántos bloques tiene? ¿Cuántos niveles
tiene? ¿Cuántos bloques tiene por nivel? ¿Cuántas tuplas tiene un bloque de cada nivel?
Indicar el procedimiento seguido e incluir el código SQL utilizado.

```
CREATE INDEX idx_kilometros ON camiones (kilometros);
```

```
pl1=# \di+ 
                                                 List of relations
 Schema |          Name          | Type  |  Owner   |  Table   | Persistence | Access method |  Size  | Description 
--------+------------------------+-------+----------+----------+-------------+---------------+--------+-------------
 public | camiones_id_camion_key | index | postgres | camiones | permanent   | btree         | 428 MB | 
 public | camiones_pkey          | index | postgres | camiones | permanent   | btree         | 773 MB | 
 public | idx_kilometros         | index | postgres | camiones | permanent   | btree         | 139 MB | 
 ```

```
SELECT pg_size_pretty( pg_table_size('idx_kilometros ') );
 pg_size_pretty 
----------------
 139 MB
(1 row)

```

```
SELECT  relpages FROM   pg_class WHERE  relname = 'idx_kilometros';
 relpages 
----------
    17737
(1 row)
```

```
SELECT pg_relation_filepath('idx_kilometros');
 pg_relation_filepath 
----------------------
 base/16396/17069
(1 row)
```

```
ls -lart  /var/lib/postgresql/16/main/base/16396/17069
-rw------- 1 postgres postgres 145301504 Feb 13 19:47 /var/lib/postgresql/16/main/base/16396/17069
```


Podemos confirmar que el sistema Operativo nos indica que el tamaño es de 138MB, como nos decia la función di+
```
du -sh /var/lib/postgresql/16/main/base/16396/17069
139M    /var/lib/postgresql/16/main/base/16396/17069
```


SELECT * FROM pgstatindex("camiones_pkey"); 


SELECT * FROM pgstatindex('idx_kilometros');


SELECT bt_index_levels('idx_kilometros') AS index_levels;


SELECT * FROM pgstatindex('idx_kilometros');

Por otro lado para ver el numero de niveles y tuplas por nivel usamos el comando 
SELECT * FROM pgstatindex('order_tree') y este nos muestra que tenemos un arbol de 2 +1 = 3 niveles y 50 bloques por cada nivel interno (internal_pages) y 13662 bloques hoja(leaf_pages).
 
 
Cada nivel tendra el numero de bloques * numero de registros teoricos que son 47 registros.
Asi el primer nivel tendra 47 registros, el segundo 50 * 47 = 2350 registros y el tercer nivel 
 13662 * 47 = 642114 registros

Instalamos la extensión pgstattuple
 ```
pl1=# create extension pgstattuple;
CREATE EXTENSION
```



 ```
pl1=# SELECT * FROM pgstatindex('idx_kilometros');
 version | tree_level | index_size | root_block_no | internal_pages | leaf_pages | empty_pages | deleted_pages | avg_leaf_density | leaf_fragmentation 
---------+------------+------------+---------------+----------------+------------+-------------+---------------+------------------+--------------------
       4 |          2 |  145301504 |           290 |             64 |      17672 |           0 |             0 |            91.57 |                  0
(1 row)
 ```

El indice que hemos formado es un B+ con 2 niveles de hojas, donde el tamaño del indice es 138,6MB,que tiene un bloque raíz en la página 290 (Root Block No), donde hay 64 páginas internas que no son ni hojas, no raíz y el árbol tien 17672 páginas, siendo estas las que contienen las claves del indice y los punteros a las filas de las tablas correspondientes. No hay páginas vacías, ni páginas eliminadas en el indice, tiene una densidad de 91,57% lo que indica que caben más datos en la página  y con una fragmentación de las páginas en las hojas del 0%, esto indica que las páginas estan contiguas.

Este indice esta biene structurado y ocupa un tamaño considerable, lo que tiene 2 niveles y muchas hojas, que hace que el indice sea óptimo, al haber una alta densidad en las páginas hace que haya un alto rendimiento en las consultas. Ademas al no haber páginas vacías y una alta fragmentación son indicativos de una alto mantenimiento del indice.



----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------




Cuestión 12. Determinar el tamaño de bloques que teóricamente tendría de acuerdo
con lo visto en teoría y el número de niveles. Comparar los resultados obtenidos
teóricamente con los resultados obtenidos en la cuestión 11.


¡HACER LA COMPARACIÓN!

```
Secundario + no clave  Cajones de Punteros
Nri = V(Kilometros)  500.001 reg
Lpbloque = 8 bytes
Lp(kilómetros) = 4 bytes
Ya que el tamaño de puntero a bloque en un sistema de 64 bits son 8 bytes.
Nodo Raíz / Intermedio:
n * Lpbloque + (n-1)* L(Kilometros) <= Butil
n*8 + (n-1)4 <= 146336106,6 bytes
12n – 4 <= 146336106,6 bytes
n <= 146336106,6 + 4 /12 =
n <= 12194675,22 punteros a bloque
Nodo Hoja:
Nh * (L(kilómetros) + Lbloque) + Lpbloque <= Butil
nh * (8+4) + 8 <= 146336106,6 bytes
20nh <= 146336106,6 bytes
nh <= 146336106,6 / 20 
nh <= 7316805,33 valores de campo

Nodos Hoja Raíz: 500.001reg / 7316805,33 = 1 (redondear por arriba)
Número de Bloques = 1bloque es 1 nivel
Cajones a Punteros  Número de Cajones = 500.001 registros / cajón
Nc = 20.000.000 / 500.001 reg =40 reg
Los cajones llevan pRegistro  Lrc = LPreg = 6 bytes
Frc = 500.001 reg / 7 = 71.428 reg / bloq
Brc = 40 / 71428 reg/bloq = 1 bloq
```

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Cuestión 13. Crear un índice de tipo hash para el campo kilómetros. Dónde se
almacena físicamente ese índice? ¿Qué tamaño tiene? ¿Cuántos bloques tiene?
¿Cuántos cajones tiene? ¿Cuántas tuplas tiene de media un cajón? Indicar el
procedimiento seguido e incluir el código SQL utilizado.

```
create index indice_HASH from camiones using HASH(kilometros);

```


Con esto generamos un indice de tipo HASH y comprobamos que es HASH, ya que es access method indica HASH, en cuanto al tamaño del indice también lo podemos observar en la tabla y en este caso es de 603 MB.

```
\di+
```
                                                List of relations
 Schema |          Name          | Type  | Owner |  Table   | Persistence | Access method |  Size  | Description 
--------+------------------------+-------+-------+----------+-------------+---------------+--------+-------------
 public | camiones_id_camion_key | index | hol   | camiones | permanent   | btree         | 428 MB | 
 public | camiones_pkey          | index | hol   | camiones | permanent   | btree         | 783 MB | 
 public | idx_kilometros         | index | hol   | camiones | permanent   | btree         | 139 MB | 
 public | indice_hash            | index | hol   | camiones | permanent   | hash          | 603 MB |

 Para saber ¿donde se almacena físicamente el indice?, me sirve del comando pg_class y mediante la columna relfilenode, que me dice el nodo en el que se almacena el indice que es el "16457", y con esto podemos saber el lugar físico en el que se almacena el indice mediante pg_relation_filepath, esto nos muestra que se situa en físicamente en el "base/16401/16457", esto indica que se situa en el directorio 'base' que es donde se almacena los datos de la base de datos, '16401' es el OID del espacio de tablas al que pertenece la relación y el '16457', es el identificador de nodo de archivo de la relación, de aquí también podemos obtener el numero de cajones del indice

(FELIX PRUEBALO TU A VER SI TE ESCUPE LO MISMO: "16457"	"indice_hash"	"2200"	0	0	"10"	"405"	"16457"	0	77198	2e+07	0	0	false	false	"p"	"i"	1	0	false	false	false	false	false	true	"n"	false	0	"0"	"0", ya que hya un apartado que dice file partition y en los apartado anteriores hay que hacer una partición y yo no la tengo hecha.)
```
 select * from pg_class where relname ilike 'indice_hash';
```
>"16457"	"indice_hash"	"2200"	0	0	"10"	"405"	"16457"	0	77198	2e+07	0	0	false	false	"p"	"i"	1	0	false	false	false	false	false	true	"n"	false	0	"0"	"0"

```
select pg_relation_filepath(16457);select pg_relation_filepath(16457);
```
>"base/16401/16457"

Para saber cuantos bloques tiene el indice diviendo el tamaño de archivo entre el tamaño de bloque. El tamaño de archivo lo podemos obtener pg_relation_size y el numero de nodo del indice, que lo sabemos del comando anterior y obtenemos el tamaño de archivo del indice que ocupa 632406016 bytes y con el tamaño de bloque de Postgres SQL obtenido con show block_size, que es de 8192 bytes / bloque, de la división de 632406016 bytes / 8192 bytes / bloque = 77198 bloques.

```
select pg_relation_size(16457);

```
>632406016 bytes

```
show block_size;



```
>  block_size 
------------
 8192

El indice hash alberga 65530 bloques de cajones del indice hash y 11660 bloques de cajones de overflow, este número alto de páginas de desbordamiento, indican que el indice hash esta experimentando una alta carga de datos, que afecta al rendimiento debido a un mayor tiempo de acceso a las páginas de desbordamiento. El numero de páginas de cubos es demasiado bajo con el número total de elementos activos (live_items = 20.000.000), esto podría sugerir una alta frágmentación y por ello reducir el rendimiento de las consultas de un indice hash y secundo mi tesis de que este indice hash reduce el rendimiento de las consultas ya que postgres no lo utiliza para buscar y utiliza el btree.
Con los datos obtenidos anteriormente calculamos el número medio de tuplas por cajón que resulta de la división de los live_items / bucket_pages --> 20.000.000/65536 = 304,63 número medio de tuplas por cajón.

```
select * from pgstathashindex('indice_hash');
```
<img width="851" alt="Captura de pantalla 2024-02-20 a las 19 39 21" src="https://github.com/HugoOvide/BBDA-11--...../assets/159030158/f475298a-59c1-47a9-ae22-ab1a199a83be">

```
select * from pg_stat_user_indexes;
```
<img width="848" alt="Captura de pantalla 2024-02-20 a las 19 42 20" src="https://github.com/HugoOvide/BBDA-11--...../assets/159030158/ab63f206-f5e3-4b42-9539-42dbef06f1e8">


