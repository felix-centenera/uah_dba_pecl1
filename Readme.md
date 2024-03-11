

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

Crear tabla camiones:
```
pl1=# CREATE TABLE camiones (
    id_camion SERIAL UNIQUE,
    matricula CHAR(8) PRIMARY KEY,
    empresa VARCHAR(100),
    kilometros INT
);
```
Comprobar tabla:
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

Generar los datos:
```
python3 ./generateRandomDat.py
```

```
pl1=# select * from camiones;
 id_camion | matricula | empresa | kilometros 
-----------+-----------+---------+------------
(0 filas)
```

Cargando Datos:
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
----------------------------------------------------------------------------------------------------
FILL-FACTOR: Table FILLFACTOR default value is 100, podemos ver que no hay valor definido que no sea el de por defecto.

SELECT t.relname AS table_name, t.reloptions FROM pg_class JOIN pg_namespace n ON n.oid = t.relnamespace WHERE t.relname = 'camiones' AND n.nspname = 'public';
table_name | reloptions 
------------+------------
 camiones   | 
(1 row)

Por tanto 100%

B = 8.192 bytes
Lcontrol=24
B.util=8192-24= 8168
LR=Lid_camion +  Lmatricula +  Lempresa +  Lkilometros = 4 + 8 + 100 + 4 =116
FR= B.util/LR= 70 reg/bloque
Br=nr/FR= 20000000/70=285715 bloque

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------

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


CREATE TABLE camiones3 (
    id_camion SERIAL,
    matricula CHAR(8),
    empresa VARCHAR(100),
    kilometros INT
) PARTITION BY HASH(kilometros);


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
CREATE TABLE camiones3_p8 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 8);
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

----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------
CHECK PRIMARY KEYS IN PARTITION

```
pl1=# CREATE TABLE camiones3 (
    id_camion SERIAL,
    matricula CHAR(8),
    empresa VARCHAR(100),
    kilometros INT,
    PRIMARY KEY (kilometros)
) PARTITION BY HASH(kilometros);
CREATE TABLE

CREATE TABLE camiones3_p0 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 0);
pl1=# CREATE TABLE camiones3_p0 PARTITION OF camiones3 FOR VALUES WITH (MODULUS 20, REMAINDER 0);
CREATE TABLE
pl1=# 


pl1=# \d camiones3;
                                   Partitioned table "public.camiones3"
   Column   |          Type          | Collation | Nullable |                   Default                    
------------+------------------------+-----------+----------+----------------------------------------------
 id_camion  | integer                |           | not null | nextval('camiones3_id_camion_seq'::regclass)
 matricula  | character(8)           |           |          | 
 empresa    | character varying(100) |           |          | 
 kilometros | integer                |           | not null | 
Partition key: HASH (kilometros)
Indexes:
    "camiones3_pkey" PRIMARY KEY, btree (kilometros)
Number of partitions: 1 (Use \d+ to list them.)


pl1=# \d+
                                                    List of relations
 Schema |          Name           |       Type        |  Owner   | Persistence | Access method |    Size    | Description 
--------+-------------------------+-------------------+----------+-------------+---------------+------------+-------------
 public | camiones                | table             | postgres | permanent   | heap          | 1413 MB    | 
 public | camiones3               | partitioned table | postgres | permanent   |               | 0 bytes    | 
 public | camiones3_id_camion_seq | sequence          | postgres | permanent   |               | 8192 bytes | 
 public | camiones3_p0            | table             | postgres | permanent   | heap          | 0 bytes    | 
 public | camiones_id_camion_seq  | sequence          | postgres | permanent   |               | 8192 bytes | 
(5 rows)


```
----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------



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


Crear un índice de tipo árbol para kilómetros:
```
CREATE INDEX idx_kilometros ON camiones (kilometros);
```

¿Dónde se almacena
físicamente ese índice?
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


¿Qué tamaño tiene? 
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

Podemos confirmar que el sistema Operativo nos indica que el tamaño es de 138MB, como nos decia la función di+
```
du -sh /var/lib/postgresql/16/main/base/16396/17069
139M    /var/lib/postgresql/16/main/base/16396/17069
```

¿Cuántos bloques tiene? 

```
SELECT  relpages FROM   pg_class WHERE  relname = 'idx_kilometros';
 relpages 
----------
    17737
(1 row)
```


¿Cuántos niveles tiene?

 ```
pl1=# SELECT * FROM pgstatindex('idx_kilometros');
 version | tree_level | index_size | root_block_no | internal_pages | leaf_pages | empty_pages | deleted_pages | avg_leaf_density | leaf_fragmentation 
---------+------------+------------+---------------+----------------+------------+-------------+---------------+------------------+--------------------
       4 |          2 |  145301504 |           290 |             64 |      17672 |           0 |             0 |            91.57 |                  0
(1 row)
 ```

El indice que hemos formado es un B+ con 1 nivel raiz +  1 nivel intermedio + un nivel de nodos hojas = 3 niveles


¿Cuántos bloques tiene por nivel?

Número de nodos hoja=  17672
Numero de nodos intermedios + un nodo raiz = 64


Numero de nodos= 64 + 17672= 17736; Que no coincide con el número de bloques que nos indicaba que tiene el arbol 17737, ya que hay un bloque 0 de metadatos.


```
CREATE EXTENSION IF NOT EXISTS pageinspect;
```

¿Cuántas tuplas tiene un bloque de cada nivel?
NIVEL RAIZ: 
-------------

Obtenemos el bloque raiz:290
```
SELECT * FROM bt_metap('idx_kilometros');
 magic  | version | root | level | fastroot | fastlevel | last_cleanup_num_delpages | last_cleanup_num_tuples | allequalimage 
--------+---------+------+-------+----------+-----------+---------------------------+-------------------------+---------------
 340322 |       4 |  290 |     2 |      290 |         2 |                         0 |                      -1 | t
(1 row)
```

Podemos obtener el número de registros que tiene: 63
```
pl1=# SELECT * FROM bt_page_stats('idx_kilometros', 290);
 blkno | type | live_items | dead_items | avg_item_size | page_size | free_size | btpo_prev | btpo_next | btpo_level | btpo_flags 
-------+------+------------+------------+---------------+-----------+-----------+-----------+-----------+------------+------------
   290 | r    |         63 |          0 |            15 |      8192 |      6896 |         0 |         0 |          2 |          2
(1 row)
```

Podemos observas la entradas, si teníamos 64 nodos raiz/intermedio, tiene sentido que tengamos live_items 63 entradas para apuntar a los 63 nodos intermedios no raiz que tenemos en el siguiente nivel.
De lo cuales, podemos observar que la longitud de uno es de 8 bytes, ya que tenemos n punteros a registros y n-1 valores de registro.
Observese, que podemos deducir que el peso del puntero es de 8 bytes por la única entrada que tiene una logitud de 8 bytes.  Si el resto de entradas que tienen puntero a bloque +LongInt=16, podriamos pensar que el tipo int es de 8 bytes, pero esto se debe al byte alignment, ya que el int es 4 bytes, y puntero necesita 8, el sistema nos añade 4 de alineamiento con el fi de mejorar la perfomance en nuestra arquitectura de 64bits.
Observese la columna type, que nos indica con una r que efectivamente estamos analizando el root del indice 


SELECT * FROM bt_page_items('idx_kilometros', 290);
```
 itemoffset |   ctid    | itemlen | nulls | vars |          data           | dead | htid | tids 
------------+-----------+---------+-------+------+-------------------------+------+------+------
          1 | (3,0)     |       8 | f     | f    |                         |      |      | 
          2 | (289,1)   |      16 | f     | f    | 63 1f 00 00 00 00 00 00 |      |      | 
          3 | (575,1)   |      16 | f     | f    | dc 3e 00 00 00 00 00 00 |      |      | 
          4 | (860,1)   |      16 | f     | f    | 35 5e 00 00 00 00 00 00 |      |      | 
          5 | (1145,1)  |      16 | f     | f    | 8d 7d 00 00 00 00 00 00 |      |      | 
          6 | (1430,1)  |      16 | f     | f    | 08 9d 00 00 00 00 00 00 |      |      | 
          7 | (1715,1)  |      16 | f     | f    | 81 bc 00 00 00 00 00 00 |      |      | 
          8 | (2000,1)  |      16 | f     | f    | db db 00 00 00 00 00 00 |      |      | 
          9 | (2285,1)  |      16 | f     | f    | 2f fb 00 00 00 00 00 00 |      |      | 
         10 | (2570,1)  |      16 | f     | f    | 9c 1a 01 00 00 00 00 00 |      |      | 
         11 | (2855,1)  |      16 | f     | f    | f4 39 01 00 00 00 00 00 |      |      | 
         12 | (3140,1)  |      16 | f     | f    | 50 59 01 00 00 00 00 00 |      |      | 
         13 | (3425,1)  |      16 | f     | f    | b1 78 01 00 00 00 00 00 |      |      | 
         14 | (3710,1)  |      16 | f     | f    | 2e 98 01 00 00 00 00 00 |      |      | 
         15 | (3995,1)  |      16 | f     | f    | 93 b7 01 00 00 00 00 00 |      |      | 
         16 | (4280,1)  |      16 | f     | f    | 04 d7 01 00 00 00 00 00 |      |      | 
         17 | (4565,1)  |      16 | f     | f    | 5a f6 01 00 00 00 00 00 |      |      | 
         18 | (4850,1)  |      16 | f     | f    | ca 15 02 00 00 00 00 00 |      |      | 
         19 | (5135,1)  |      16 | f     | f    | 3c 35 02 00 00 00 00 00 |      |      | 
         20 | (5420,1)  |      16 | f     | f    | 95 54 02 00 00 00 00 00 |      |      | 
         21 | (5705,1)  |      16 | f     | f    | f3 73 02 00 00 00 00 00 |      |      | 
         22 | (5990,1)  |      16 | f     | f    | 5c 93 02 00 00 00 00 00 |      |      | 
         23 | (6275,1)  |      16 | f     | f    | c4 b2 02 00 00 00 00 00 |      |      | 
         24 | (6560,1)  |      16 | f     | f    | 24 d2 02 00 00 00 00 00 |      |      | 
         25 | (6845,1)  |      16 | f     | f    | 6a f1 02 00 00 00 00 00 |      |      | 
         26 | (7130,1)  |      16 | f     | f    | d3 10 03 00 00 00 00 00 |      |      | 
         27 | (7415,1)  |      16 | f     | f    | 35 30 03 00 00 00 00 00 |      |      | 
         28 | (7700,1)  |      16 | f     | f    | bd 4f 03 00 00 00 00 00 |      |      | 
         29 | (7985,1)  |      16 | f     | f    | 30 6f 03 00 00 00 00 00 |      |      | 
         30 | (8270,1)  |      16 | f     | f    | b1 8e 03 00 00 00 00 00 |      |      | 
         31 | (8555,1)  |      16 | f     | f    | 1e ae 03 00 00 00 00 00 |      |      | 
         32 | (8840,1)  |      16 | f     | f    | 7c cd 03 00 00 00 00 00 |      |      | 
         33 | (9125,1)  |      16 | f     | f    | d6 ec 03 00 00 00 00 00 |      |      | 
         34 | (9410,1)  |      16 | f     | f    | 3c 0c 04 00 00 00 00 00 |      |      | 
         35 | (9695,1)  |      16 | f     | f    | a2 2b 04 00 00 00 00 00 |      |      | 
         36 | (9980,1)  |      16 | f     | f    | 02 4b 04 00 00 00 00 00 |      |      | 
         37 | (10265,1) |      16 | f     | f    | 55 6a 04 00 00 00 00 00 |      |      | 
         38 | (10550,1) |      16 | f     | f    | bd 89 04 00 00 00 00 00 |      |      | 
         39 | (10835,1) |      16 | f     | f    | 27 a9 04 00 00 00 00 00 |      |      | 
         40 | (11120,1) |      16 | f     | f    | 89 c8 04 00 00 00 00 00 |      |      | 
         41 | (11405,1) |      16 | f     | f    | 02 e8 04 00 00 00 00 00 |      |      | 
         42 | (11690,1) |      16 | f     | f    | 5e 07 05 00 00 00 00 00 |      |      | 
         43 | (11975,1) |      16 | f     | f    | b9 26 05 00 00 00 00 00 |      |      | 
         44 | (12260,1) |      16 | f     | f    | 1b 46 05 00 00 00 00 00 |      |      | 
         45 | (12545,1) |      16 | f     | f    | 7d 65 05 00 00 00 00 00 |      |      | 
         46 | (12830,1) |      16 | f     | f    | e2 84 05 00 00 00 00 00 |      |      | 
         47 | (13115,1) |      16 | f     | f    | 52 a4 05 00 00 00 00 00 |      |      | 
         48 | (13400,1) |      16 | f     | f    | a7 c3 05 00 00 00 00 00 |      |      | 
         49 | (13685,1) |      16 | f     | f    | 0d e3 05 00 00 00 00 00 |      |      | 
         50 | (13970,1) |      16 | f     | f    | 66 02 06 00 00 00 00 00 |      |      | 
         51 | (14255,1) |      16 | f     | f    | a2 21 06 00 00 00 00 00 |      |      | 
         52 | (14540,1) |      16 | f     | f    | fd 40 06 00 00 00 00 00 |      |      | 
         53 | (14825,1) |      16 | f     | f    | 5a 60 06 00 00 00 00 00 |      |      | 
         54 | (15110,1) |      16 | f     | f    | b6 7f 06 00 00 00 00 00 |      |      | 
         55 | (15395,1) |      16 | f     | f    | 0b 9f 06 00 00 00 00 00 |      |      | 
         56 | (15680,1) |      16 | f     | f    | 73 be 06 00 00 00 00 00 |      |      | 
         57 | (15965,1) |      16 | f     | f    | c0 dd 06 00 00 00 00 00 |      |      | 
         58 | (16250,1) |      16 | f     | f    | 2f fd 06 00 00 00 00 00 |      |      | 
         59 | (16535,1) |      16 | f     | f    | 7d 1c 07 00 00 00 00 00 |      |      | 
         60 | (16820,1) |      16 | f     | f    | f8 3b 07 00 00 00 00 00 |      |      | 
         61 | (17105,1) |      16 | f     | f    | 65 5b 07 00 00 00 00 00 |      |      | 
         62 | (17390,1) |      16 | f     | f    | be 7a 07 00 00 00 00 00 |      |      | 
         63 | (17675,1) |      16 | f     | f    | 0a 9a 07 00 00 00 00 00 |      |      |
```

SOLUCIÓN: El nodo raiz, único del nivel raiz tiene 63 registros. Campo live_items 63



NIVEL INTERMEDIO: 
-------------

Podemos preguntar a un bloque de tipo intermedio 

```
SELECT * FROM bt_page_stats('idx_kilometros', 3);
pl1=# SELECT * FROM bt_page_stats('idx_kilometros', 3);
 blkno | type | live_items | dead_items | avg_item_size | page_size | free_size | btpo_prev | btpo_next | btpo_level | btpo_flags 
-------+------+------------+------------+---------------+-----------+-----------+-----------+-----------+------------+------------
     3 | i    |        285 |          0 |            15 |      8192 |      2456 |         0 |       289 |          1 |          0
(1 row)
```

Podemos preguntar o a varios de ellos para tener la certeza de que todos tienen 285 registros.
```
SELECT * FROM bt_multi_page_stats('idx_kilometros', 1, 17736) WHERE type = 'i';
blkno | type | live_items | dead_items | avg_item_size | page_size | free_size | btpo_prev | btpo_next | btpo_level | btpo_flags 
-------+------+------------+------------+---------------+-----------+-----------+-----------+-----------+------------+------------
     3 | i    |        285 |          0 |            15 |      8192 |      2456 |         0 |       289 |          1 |          0
   289 | i    |        285 |          0 |            15 |      8192 |      2456 |         3 |       575 |          1 |          0
   575 | i    |        285 |          0 |            15 |      8192 |      2456 |       289 |       860 |          1 |          0
   860 | i    |        285 |          0 |            15 |      8192 |      2456 |       575 |      1145 |          1 |          0
  1145 | i    |        285 |          0 |            15 |      8192 |      2456 |       860 |      1430 |          1 |          0
  1430 | i    |        285 |          0 |            15 |      8192 |      2456 |      1145 |      1715 |          1 |          0
  1715 | i    |        285 |          0 |            15 |      8192 |      2456 |      1430 |      2000 |          1 |          0
  2000 | i    |        285 |          0 |            15 |      8192 |      2456 |      1715 |      2285 |          1 |          0
  2285 | i    |        285 |          0 |            15 |      8192 |      2456 |      2000 |      2570 |          1 |          0
  2570 | i    |        285 |          0 |            15 |      8192 |      2456 |      2285 |      2855 |          1 |          0
  2855 | i    |        285 |          0 |            15 |      8192 |      2456 |      2570 |      3140 |          1 |          0
  3140 | i    |        285 |          0 |            15 |      8192 |      2456 |      2855 |      3425 |          1 |          0
  3425 | i    |        285 |          0 |            15 |      8192 |      2456 |      3140 |      3710 |          1 |          0
  3710 | i    |        285 |          0 |            15 |      8192 |      2456 |      3425 |      3995 |          1 |          0
  3995 | i    |        285 |          0 |            15 |      8192 |      2456 |      3710 |      4280 |          1 |          0
  4280 | i    |        285 |          0 |            15 |      8192 |      2456 |      3995 |      4565 |          1 |          0
  4565 | i    |        285 |          0 |            15 |      8192 |      2456 |      4280 |      4850 |          1 |          0
  4850 | i    |        285 |          0 |            15 |      8192 |      2456 |      4565 |      5135 |          1 |          0
  5135 | i    |        285 |          0 |            15 |      8192 |      2456 |      4850 |      5420 |          1 |          0
  5420 | i    |        285 |          0 |            15 |      8192 |      2456 |      5135 |      5705 |          1 |          0
  5705 | i    |        285 |          0 |            15 |      8192 |      2456 |      5420 |      5990 |          1 |          0
  5990 | i    |        285 |          0 |            15 |      8192 |      2456 |      5705 |      6275 |          1 |          0
  6275 | i    |        285 |          0 |            15 |      8192 |      2456 |      5990 |      6560 |          1 |          0
  6560 | i    |        285 |          0 |            15 |      8192 |      2456 |      6275 |      6845 |          1 |          0
  6845 | i    |        285 |          0 |            15 |      8192 |      2456 |      6560 |      7130 |          1 |          0
  7130 | i    |        285 |          0 |            15 |      8192 |      2456 |      6845 |      7415 |          1 |          0
  7415 | i    |        285 |          0 |            15 |      8192 |      2456 |      7130 |      7700 |          1 |          0
  7700 | i    |        285 |          0 |            15 |      8192 |      2456 |      7415 |      7985 |          1 |          0
  7985 | i    |        285 |          0 |            15 |      8192 |      2456 |      7700 |      8270 |          1 |          0
  8270 | i    |        285 |          0 |            15 |      8192 |      2456 |      7985 |      8555 |          1 |          0
  8555 | i    |        285 |          0 |            15 |      8192 |      2456 |      8270 |      8840 |          1 |          0
  8840 | i    |        285 |          0 |            15 |      8192 |      2456 |      8555 |      9125 |          1 |          0
  9125 | i    |        285 |          0 |            15 |      8192 |      2456 |      8840 |      9410 |          1 |          0
  9410 | i    |        285 |          0 |            15 |      8192 |      2456 |      9125 |      9695 |          1 |          0
  9695 | i    |        285 |          0 |            15 |      8192 |      2456 |      9410 |      9980 |          1 |          0
  9980 | i    |        285 |          0 |            15 |      8192 |      2456 |      9695 |     10265 |          1 |          0
 10265 | i    |        285 |          0 |            15 |      8192 |      2456 |      9980 |     10550 |          1 |          0
 10550 | i    |        285 |          0 |            15 |      8192 |      2456 |     10265 |     10835 |          1 |          0
 10835 | i    |        285 |          0 |            15 |      8192 |      2456 |     10550 |     11120 |          1 |          0
 11120 | i    |        285 |          0 |            15 |      8192 |      2456 |     10835 |     11405 |          1 |          0
 11405 | i    |        285 |          0 |            15 |      8192 |      2456 |     11120 |     11690 |          1 |          0
 11690 | i    |        285 |          0 |            15 |      8192 |      2456 |     11405 |     11975 |          1 |          0
 11975 | i    |        285 |          0 |            15 |      8192 |      2456 |     11690 |     12260 |          1 |          0
 12260 | i    |        285 |          0 |            15 |      8192 |      2456 |     11975 |     12545 |          1 |          0
 12545 | i    |        285 |          0 |            15 |      8192 |      2456 |     12260 |     12830 |          1 |          0
 12830 | i    |        285 |          0 |            15 |      8192 |      2456 |     12545 |     13115 |          1 |          0
 13115 | i    |        285 |          0 |            15 |      8192 |      2456 |     12830 |     13400 |          1 |          0
 13400 | i    |        285 |          0 |            15 |      8192 |      2456 |     13115 |     13685 |          1 |          0
 13685 | i    |        285 |          0 |            15 |      8192 |      2456 |     13400 |     13970 |          1 |          0
 13970 | i    |        285 |          0 |            15 |      8192 |      2456 |     13685 |     14255 |          1 |          0
 14255 | i    |        285 |          0 |            15 |      8192 |      2456 |     13970 |     14540 |          1 |          0
```
SOLUCIÓN: Los nodos intermedios tienen 285 registros. Campo live_items  285.



NIVEL hoja: 
-------------
Podemos preguntar o a varios bloque de tipo de hoja para saber cuando registros tienen.
SELECT * FROM bt_multi_page_stats('idx_kilometros', 1, 17736) WHERE type = 'l';
```
 blkno | type | live_items | dead_items | avg_item_size | page_size | free_size | btpo_prev | btpo_next | btpo_level | btpo_flags 
-------+------+------------+------------+---------------+-----------+-----------+-----------+-----------+------------+------------
     1 | l    |         30 |          0 |           242 |      8192 |       740 |         0 |         2 |          0 |          1
     2 | l    |         29 |          0 |           255 |      8192 |       632 |         1 |         4 |          0 |          1
     4 | l    |         30 |          0 |           244 |      8192 |       684 |         2 |         5 |          0 |          1
     5 | l    |         30 |          0 |           246 |      8192 |       636 |         4 |         6 |          0 |          1
     6 | l    |         29 |          0 |           256 |      8192 |       608 |         5 |         7 |          0 |          1
     7 | l    |         30 |          0 |           245 |      8192 |       660 |         6 |         8 |          0 |          1
     8 | l    |         28 |          0 |           257 |      8192 |       820 |         7 |         9 |          0 |          1
     9 | l    |         29 |          0 |           251 |      8192 |       728 |         8 |        10 |          0 |          1
    10 | l    |         28 |          0 |           265 |      8192 |       612 |         9 |        11 |          0 |          1
    11 | l    |         30 |          0 |           245 |      8192 |       652 |        10 |        12 |          0 |          1
    12 | l    |         30 |          0 |           248 |      8192 |       572 |        11 |        13 |          0 |          1
    13 | l    |         29 |          0 |           254 |      8192 |       648 |        12 |        14 |          0 |          1
    14 | l    |         27 |          0 |           268 |      8192 |       792 |        13 |        15 |          0 |          1
    15 | l    |         30 |          0 |           247 |      8192 |       612 |        14 |        16 |          0 |          1
    16 | l    |         29 |          0 |           249 |      8192 |       784 |        15 |        17 |          0 |          1
    17 | l    |         31 |          0 |           235 |      8192 |       712 |        16 |        18 |          0 |          1
    18 | l    |         29 |          0 |           252 |      8192 |       696 |        17 |        19 |          0 |          1
    19 | l    |         29 |          0 |           252 |      8192 |       696 |        18 |        20 |          0 |          1
    20 | l    |         28 |          0 |           262 |      8192 |       692 |        19 |        21 |          0 |          1
    21 | l    |         28 |          0 |           258 |      8192 |       804 |        20 |        22 |          0 |          1
    22 | l    |         28 |          0 |           258 |      8192 |       788 |        21 |        23 |          0 |          1
    23 | l    |         30 |          0 |           249 |      8192 |       556 |        22 |        24 |          0 |          1
    24 | l    |         30 |          0 |           245 |      8192 |       676 |        23 |        25 |          0 |          1
    25 | l    |         30 |          0 |           245 |      8192 |       676 |        24 |        26 |          0 |          1
    26 | l    |         28 |          0 |           258 |      8192 |       804 |        25 |        27 |          0 |          1
    27 | l    |         29 |          0 |           252 |      8192 |       720 |        26 |        28 |          0 |          1
    28 | l    |         29 |          0 |           253 |      8192 |       680 |        27 |        29 |          0 |          1
    29 | l    |         29 |          0 |           250 |      8192 |       760 |        28 |        30 |          0 |          1
    30 | l    |         31 |          0 |           237 |      8192 |       648 |        29 |        31 |          0 |          1
    31 | l    |         29 |          0 |           250 |      8192 |       760 |        30 |        32 |          0 |          1
    32 | l    |         29 |          0 |           253 |      8192 |       672 |        31 |        33 |          0 |          1
    33 | l    |         30 |          0 |           245 |      8192 |       652 |        32 |        34 |          0 |          1
    34 | l    |         31 |          0 |           240 |      8192 |       568 |        33 |        35 |          0 |          1
    35 | l    |         30 |          0 |           245 |      8192 |       652 |        34 |        36 |          0 |          1
    36 | l    |         29 |          0 |           258 |      8192 |       544 |        35 |        37 |          0 |          1
    37 | l    |         29 |          0 |           253 |      8192 |       680 |        36 |        38 |          0 |          1
    38 | l    |         30 |          0 |           245 |      8192 |       660 |        37 |        39 |          0 |          1
```

SOLUCIÓN: Los nodos hoja,  tiene unos  30 registros. Campo live_items  30


----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------

Cuestión 12. Determinar el tamaño de bloques que teóricamente tendría de acuerdo
con lo visto en teoría y el número de niveles. Comparar los resultados obtenidos
teóricamente con los resultados obtenidos en la cuestión 11.

RAIZ
SELECT * FROM bt_page_items('idx_kilometros', 290);
PUNTERO A BLOQUE 8bytes

INTERMEDIO
SELECT * FROM bt_page_items('idx_kilometros', 3);
PUNTERO A BLOQUE 8bytes

HOJA
SELECT * FROM bt_page_items('idx_kilometros', 2);
PUNTERO A BLOQUE 16


```
SELECT avg_leaf_density FROM pgstatindex('idx_kilometros');)
 avg_leaf_density 
------------------
            91.57
(1 row)

Butil= 8192 * 91.57/100=7501
Nodo raiz/intermedio: n * LpB + (n-1)*Lkm <=BUtil

(n * 8) + (n-1)*8 <= 7501
8n+8n-8 <= 7501
16n-8 <= 7501
n=469

Nodo hoja: nh*(LpB + Lk) + LpB <= Butil
nh*(8 + Lk) + LpB <= Butil
nh*(8 + 8) + 8 <= 7501
16nh + 8 <= 7501
nh= 468

Nodos hoja= 500001/468=1068
Nodos intermedio= 1068 /469=3
Nodos raiz=1


Numero de registros/cajon= 20000000 / 500001 =40 registros por cajon
LRC=8 
FRC=7501/8=937
BRC= 40/937=1 bloque

Tenemos 500001 cajones de 1 bloque cada uno= 500001 bloques de cajones

Indice ocupa(sin cajones) = 1068 + 3 + 1 = 1072 bloques
Indice ocupa (con cajones ) = 1068 + 3 + 1 + 500001 *1 = 501073 bloques
```
........


Butil= 8192 * 91.57/100=7501
Nodo raiz/intermedio: n * LpB + (n-1)*Lkm <=BUtil
(n * 16) + (n-1)*8 <= 7501
16n + 8n -1 <= 7501
n = 312

Nodo hoja: nh*(LpR + Lk) + LpB <= Butil
nh*(4 + Lk) + LpB <= Butil
nh*(4 + 8) + 8 <= 7501
nh=624

Número de nodos hoja = nR / nh 
 20000000 / 624 = 801
 801/312=2

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------

Cuestión 12. Determinar el tamaño de bloques que teóricamente tendría de acuerdo
con lo visto en teoría y el número de niveles. Comparar los resultados obtenidos
teóricamente con los resultados obtenidos en la cuestión 11.

No ordenado + Valores repetidos:
  Secundario + campo no clave: Cajones de punteros.

APROXIMACIÓN TEÓRICA Lkm=4: 
            Nodo Raíz / Intermedio:
              n*(Lpb)+ (n-1)*(Lkm) <= BUtil
              n*8 + (n-1) *  4  <= BUtil
              8n + 4n -1 <= 8192
              12n -1   <= 8192
              n =  682 punteros a bloque

            Nodo hoja:
              nh(LKm + Lpbloque) + Lpbloque  <= BUtil
              nh(4 + 8 ) + 8 <= 8192
              12nh +8 <= 8192
              nh = 682 valores de campo

            NºNodos hoja:
            nri= Vkm= 500001
            NºNodos hojas= ⌈ 500001 / 682 ⌉ =74 Nodos hojas o bloques

            NºNodos Intermedios:
              NºNodos  Intermedios: ⌈74 / 682⌉ =1

Esto sabemos que es un disparate, el indice no se comporta de esta forma, el BUtil no nos sirve, hay demasiada diferencia con lo realmente utilziado. Veamos un calculo teórico con datos mas aproximados utilizando otro enfoque.

APROXIMACIÓN TEÓRICA Lkm=8 y B usado en bloque raiz :

Sabemos que el bloque raiz tiene 62 entradas de 16 bytes y una de 8 bytes=1000 Bytes 
Y también sabemos que el sistema redondea el int 4 a 8.

            Nodo Raíz / Intermedio:
              n*(Lpb)+ (n-1)*(Lkm) <= Broot
              n*8 + (n-1) *  8  <= 1000
              8n + 8n -8 <= 1000
              16n -8 <= 1000
              n=63 punteros a bloque.  Hasta aquí tiene sentido y cuadra.

CAJONES:

          Bhoja=8192-740=7452 ó 242*30=7260.
          Podemos sacar un promedio de estos dos datos-> (7260+ 7452)/2=7356

nc= 20.000.000/500000= 40 registros por cajon
Lrc= LPReg = 8 byes
Frc=7356/8=919 registros por bloque
brc=40/919=1 bloque 

tenemos 



------------------------
+++++++++++++++++++++++++
            Nodo hoja bloque de tipo hoja:
            blkno | type | live_items | dead_items | avg_item_size | page_size | free_size | btpo_prev | btpo_next | btpo_level | btpo_flags 
            -------+------+------------+------------+---------------+-----------+-----------+-----------+-----------+------------+------------
            1     | l    |         30 |          0 |           242 |      8192 |       740 |         0 |         2 |          0 |          1

            Bhoja=8192-740=7452 ó 242*30=7260.
            Podemos sacar un promedio de estos dos datos-> (7260+ 7452)/2=7356

            nh(LKm + Lpbloque) + Lpbloque  <= Bhoja
            nh(8 + 8) + 8  <= 7356
            nh(16) +8 <= 7356
            nh = 459 valoes de campo km
            
            NºNodos hoja:
            nri= Vkm= 500001
            NºNodos hojas= ⌈ 500000 / 459 ⌉ =109 Nodos hojas o bloques

            Podemos seguir calculando siguienes niveles, pero no tiene sendio, sabemos que hay 17672 nodos hoja. Y es que teóricamente deberiamos estar usando cajones de punteros, donde los nodos hojas solo estuvieran almacenando El valor del campo nh(Lkm + el valor del PBloque)+ LPB.
            Sin embargo, al analizar las entradas de las hojas, vemos que pesan entorno a 242 BYTES,lo cual nos hace pensar que esta apuntando directamente a registros. En ese caso 
            nh(LKm + Lpregistro) + Lpbloque  <= Bhoja




 ```
pl1=# SELECT * FROM pgstatindex('idx_kilometros');
 version | tree_level | index_size | root_block_no | internal_pages | leaf_pages | empty_pages | deleted_pages | avg_leaf_density | leaf_fragmentation 
---------+------------+------------+---------------+----------------+------------+-------------+---------------+------------------+--------------------
       4 |          2 |  145301504 |           290 |             64 |      17672 |           0 |             0 |            91.57 |                  0
(1 row)
 ```

 ```
pl1=# SELECT COUNT (*) FROM bt_multi_page_stats('idx_kilometros', 1, 17736) WHERE type = 'l';
 count 
-------
 17672
(1 row)
 ```

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------



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
create index indice_HASH on camiones using HASH(kilometros);
CREATE INDEX
```

```
SELECT pg_relation_filepath('indice_hash'); 
 pg_relation_filepath 
----------------------
 base/16396/17171
(1 row)
```

```
pl1=# SELECT  relfilenode  FROM   pg_class WHERE  relname = 'indice_hash';
 relfilenode 
-------------
       17171
(1 row)
```

```
root@postgresql01:~# cd /var/lib/postgresql/16/main/base/16396
root@postgresql01:/var/lib/postgresql/16/main/base/16396# ls -lart 17171
-rw------- 1 postgres postgres 632209408 Mar  2 12:05 17171
root@postgresql01:/var/lib/postgresql/16/main/base/16396# 
```

```
pl1=#  SELECT pg_size_pretty(pg_total_relation_size('indice_hash'));
 pg_size_pretty 
----------------
 603 MB
(1 row)
```

```
root@postgresql01:/var/lib/postgresql/16/main/base/16396# du -sh 17171
603M    17171
```

```
pl1=# SELECT relpages FROM pg_class WHERE relname='indice_hash';
 relpages 
----------
    77174
(1 row)
```

Número de cajones:
```
pl1=# SELECT * FROM pgstathashindex('indice_hash');  
 version | bucket_pages | overflow_pages | bitmap_pages | unused_pages | live_items | dead_items |   free_percent    
---------+--------------+----------------+--------------+--------------+------------+------------+-------------------
       4 |        65536 |          11636 |            1 |            0 |   20000000 |          0 | 36.41772476474177
(1 row)
```

Número de tuplas de media:
  Si tenemos 20000000 de registros. 20000000/65536=305 tuplas de media. Usamos 20000000 porque nos esta diciendo que ese es el número de items que hay, pero si nos ceñimos a la teoría, los cajones HASH deberian tener V(Kilometros)/NºCajones, y los cajones de punteros que estuvieran bajo los cajones hash, serían lo que tendrían 20000000/65536=305
  
  V(Kilometros)=500000. 


----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
BLOCK SIZE


```
pl1=# SELECT name, setting, short_desc, extra_desc FROM pg_settings WHERE name like '%block%' or short_desc LIKE '%block%';
       name        | setting |                  short_desc                  |                         extra_desc                         
-------------------+---------+----------------------------------------------+------------------------------------------------------------
 block_size        | 8192    | Shows the size of a disk block.              | 
 recovery_prefetch | try     | Prefetch referenced blocks during recovery.  | Look ahead in the WAL to find references to uncached data.
 wal_block_size    | 8192    | Shows the block size in the write ahead log. | 
(3 rows)

```
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
FILL-FACTOR: Table FILLFACTOR default value is 100

```
SELECT t.relname AS table_name, 
       t.reloptions
FROM pg_class t
JOIN pg_namespace n ON n.oid = t.relnamespace
WHERE t.relname = 'camiones'
  AND n.nspname = 'public';
 table_name | reloptions 
------------+------------
 camiones   | 
(1 row)
```

Por tanto 100%

B = 8.192 bytes
Lcontrol=24
B.util=8192-24= 8168
LR=Lid_camion +  Lmatricula +  Lempresa +  Lkilometros = 4 + 8 + 100 + 4 =116
FR= B.util/LR= 70 reg/bloque
Br=nr/FR= 20000000/70=285715 bloque

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
Cuestión 14. Determinar el tamaño de bloques que teóricamente tendría de acuerdo
con lo visto en teoría y el número de niveles. Comparar los resultados obtenidos
teóricamente con los resultados obtenidos en la cuestión 13.

create index indice_HASH on camiones using HASH(kilometros);
kilometros >> orden? >> No >> Unique value? >> No. Por tanto indice secundario + campo no clave. Cajones de punteros.

Nº de cajones= Depende de la función hash que este utilizando postgresql, como no lo sabemos, vamos a partir los de los cajones que hay. Nº De cajones= 65536
Lcontrol=24
B.util=8192-24= 8168

Nº De cajones= 65536
Nº De registros por Cajón= V(kilometros)/65536= 500000/65536=8 registros por cajón.
Lric=Lkilometro + Lpb= 4 + 8= 12 bytes
frc= ⌊B.util/Lrc⌋= 8168 / 12 = 680 reg/bloque
bc=⌈ 8/680⌉= 1 bloque

Cajones de punteros:
Número de cajones de punteros= V(Camiones)=500000
Número de registros por cajón de punteros =  nr/V(kilometros)= 20000000 /500000 =40 reg/cajón
Lrcp=Lpr= 8 bytes
frcp= ⌊B.util/Lrc⌋ = 8168/ 8 = 1021 reg/bloque
bc=⌈ 40/1021= 1 bloque por cajón de puntero.

El indice debería ocupar= 1 * 500000 + 1 * 65536 = 565536 bloques.

Como podemos ver el calculo teórico no cuadra con el real 77174, esto es debido a que igual que nos pasaba con el arbol B+, el hash no esta utilizando cajones de punteros, el propio hash es el que va a contener las direcciones.



----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------



Cuestión 15. Crear un índice de tipo árbol para el campo matrícula. ¿Dónde se
almacena físicamente ese índice? ¿Qué tamaño tiene? ¿Cuántos bloques tiene?
¿Cuántos niveles tiene? ¿Cuántos bloques tiene por nivel? ¿Cuántas tuplas tiene un
bloque de cada nivel? Indicar el procedimiento seguido e incluir el código SQL
utilizado.


Crear un índice de tipo árbol para kilómetros:
```
CREATE INDEX idx_matricula_b ON camiones (matricula);
```

¿Dónde se almacena
físicamente ese índice?

```
pl1=# SELECT pg_relation_filepath('idx_matricula_b');
 pg_relation_filepath 
----------------------
 base/16396/17172
(1 row)
```

 base/16396/17172

```
 ls -lart  /var/lib/postgresql/16/main/base/16396/17172
-rw------- 1 postgres postgres 630874112 Mar  2 17:21 /var/lib/postgresql/16/main/base/16396/17172
```

¿Qué tamaño tiene? 
602 MB
```
pl1=# \di+ 
                                                           List of relations
 Schema |          Name          |       Type        |  Owner   |    Table     | Persistence | Access method |    Size    | Description 
--------+------------------------+-------------------+----------+--------------+-------------+---------------+------------+-------------
 public | idx_matricula_b        | index             | postgres | camiones     | permanent   | btree         | 602 MB     | 

(8 rows)
```

```
pl1=# SELECT pg_size_pretty( pg_table_size('idx_matricula_b ') );
 pg_size_pretty 
----------------
 602 MB
(1 row)
```


Podemos confirmar que el sistema Operativo nos indica que el tamaño es de 602M, como nos decia la función di+

```
du -sh /var/lib/postgresql/16/main/base/16396/17172
602M    /var/lib/postgresql/16/main/base/16396/17172
```

¿Cuántos bloques tiene? 

```
SELECT  relpages FROM   pg_class WHERE  relname = 'idx_matricula_b';
 relpages 
----------
    77011
(1 row)
```

¿Cuántos niveles tiene?

El indice que hemos formado es un B+ con 1 nivel raiz +  2 nivel intermedio + un nivel de nodos hojas = 4 niveles

```
pl1=# SELECT * FROM pgstatindex('idx_matricula_b');
 version | tree_level | index_size | root_block_no | internal_pages | leaf_pages | empty_pages | deleted_pages | avg_leaf_density | leaf_fragmentation 
---------+------------+------------+---------------+----------------+------------+-------------+---------------+------------------+--------------------
       4 |          3 |  630874112 |         41827 |            381 |      76629 |           0 |             0 |            90.04 |                  0
(1 row)
```

¿Cuántos bloques tiene por nivel?

Número de nodos hoja=  76629
Numero de nodos intermedios + un nodo raiz = 381

Numero de nodos=  76629 +  381 =77010 bloques,  ; Que no coincide con el número de bloques que nos indicaba que tiene el arbol 77011, ya que hay un bloque 0 de metadatos.


¿Cuántas tuplas tiene un bloque de cada nivel?

Obtenemos el bloque raiz:41827

NIVEL RAIZ: 
-------------

```
pl1=# SELECT * FROM bt_metap('idx_matricula_b');
 magic  | version | root  | level | fastroot | fastlevel | last_cleanup_num_delpages | last_cleanup_num_tuples | allequalimage 
--------+---------+-------+-------+----------+-----------+---------------------------+-------------------------+---------------
 340322 |       4 | 41827 |     3 |    41827 |         3 |                         0 |                      -1 | t
(1 row)
```


Podemos obtener el número de registros que tiene: 2
```
pl1=# SELECT * FROM bt_page_stats('idx_matricula_b', 41827);
 blkno | type | live_items | dead_items | avg_item_size | page_size | free_size | btpo_prev | btpo_next | btpo_level | btpo_flags 
-------+------+------------+------------+---------------+-----------+-----------+-----------+-----------+------------+------------
 41827 | r    |          2 |          0 |            16 |      8192 |      8108 |         0 |         0 |          3 |          2
(1 row)
```


Podemos ver esas 2 entradas que tiene.
```
pl1=# SELECT * FROM bt_page_items('idx_matricula_b', 41827);
 itemoffset |   ctid    | itemlen | nulls | vars |                      data                       | dead | htid | tids 
------------+-----------+---------+-------+------+-------------------------------------------------+------+------+------
          1 | (209,0)   |       8 | f     | f    |                                                 |      |      | 
          2 | (41826,1) |      24 | f     | t    | 13 4e 5a 4f 32 37 38 36 20 00 00 00 00 00 00 00 |      |      | 
(2 rows)
```
SOLUCIÓN: El nodo raiz, único del nivel raiz tiene 2 registros. Campo live_items 2

NIVEL INTERMEDIO: 
-------------

Obtenemos los  bloques  de tipo intermedio y vemos los live_items;
```
SELECT * FROM bt_multi_page_stats('idx_matricula_b', 1, 17736) WHERE type = 'i';
blkno | type | live_items | dead_items | avg_item_size | page_size | free_size | btpo_prev | btpo_next | btpo_level | btpo_flags 
-------+------+------------+------------+---------------+-----------+-----------+-----------+-----------+------------+------------
     3 | i    |        204 |          0 |            23 |      8192 |      2452 |         0 |       208 |          1 |          0
   208 | i    |        204 |          0 |            23 |      8192 |      2452 |         3 |       413 |          1 |          0
   209 | i    |        204 |          0 |            23 |      8192 |      2452 |         0 |     41826 |          2 |          0
   413 | i    |        204 |          0 |            23 |      8192 |      2452 |       208 |       617 |          1 |          0
   617 | i    |        204 |          0 |            23 |      8192 |      2452 |       413 |       821 |          1 |          0
   821 | i    |        204 |          0 |            23 |      8192 |      2452 |       617 |      1025 |          1 |          0
  1025 | i    |        204 |          0 |            23 |      8192 |      2452 |       821 |      1229 |          1 |          0
```

Podemos ver mas detalle de uno concreto:
```
 SELECT * FROM bt_page_stats('idx_matricula_b', 3);
 blkno | type | live_items | dead_items | avg_item_size | page_size | free_size | btpo_prev | btpo_next | btpo_level | btpo_flags 
-------+------+------------+------------+---------------+-----------+-----------+-----------+-----------+------------+------------
     3 | i    |        204 |          0 |            23 |      8192 |      2452 |         0 |       208 |          1 |          0
(1 row)
```

SOLUCIÓN: Los nodos intermedios tienen 204 registros. Campo live_items  204.

NIVEL hoja: 
-------------
Podemos preguntar o a varios bloque de tipo de hoja para saber cuando registros tienen.

```
SELECT * FROM bt_multi_page_stats('idx_matricula_b', 1, 17736) WHERE type = 'l';
 blkno | type | live_items | dead_items | avg_item_size | page_size | free_size | btpo_prev | btpo_next | btpo_level | btpo_flags 
-------+------+------------+------------+---------------+-----------+-----------+-----------+-----------+------------+------------
     1 | l    |        262 |          0 |            24 |      8192 |       812 |         0 |         2 |          0 |          1
     2 | l    |        262 |          0 |            24 |      8192 |       812 |         1 |         4 |          0 |          1
     4 | l    |        262 |          0 |            24 |      8192 |       812 |         2 |         5 |          0 |          1
     5 | l    |        262 |          0 |            24 |      8192 |       812 |         4 |         6 |          0 |          1
     6 | l    |        262 |          0 |            24 |      8192 |       812 |         5 |         7 |          0 |          1
     7 | l    |        262 |          0 |            24 |      8192 |       812 |         6 |         8 |          0 |          1
     8 | l    |        262 |          0 |            24 |      8192 |       812 |         7 |         9 |          0 |          1
     9 | l    |        262 |          0 |            24 |      8192 |       812 |         8 |        10 |          0 |          1
    10 | l    |        262 |          0 |            24 |      8192 |       812 |         9 |        11 |          0 |          1
    11 | l    |        262 |          0 |            24 |      8192 |       812 |        10 |        12 |          0 |          1
    12 | l    |        262 |          0 |            24 |      8192 |       812 |        11 |        13 |          0 |          1
    13 | l    |        262 |          0 |            24 |      8192 |       812 |        12 |        14 |          0 |          1
    14 | l    |        262 |          0 |            24 |      8192 |       812 |        13 |        15 |          0 |          1
    15 | l    |        262 |          0 |            24 |      8192 |       812 |        14 |        16 |          0 |          1
    16 | l    |        262 |          0 |            24 |      8192 |       812 |        15 |        17 |          0 |          1
    17 | l    |        262 |          0 |            24 |      8192 |       812 |        16 |        18 |          0 |          1
    18 | l    |        262 |          0 |            24 |      8192 |       812 |        17 |        19 |          0 |          1
    19 | l    |        262 |          0 |            24 |      8192 |       812 |        18 |        20 |          0 |          1
    20 | l    |        262 |          0 |            24 |      8192 |       812 |        19 |        21 |          0 |          1
```

Podemos ver mas detalle de uno concreto:
```
 SELECT * FROM bt_page_stats('idx_matricula_b', 1);
 blkno | type | live_items | dead_items | avg_item_size | page_size | free_size | btpo_prev | btpo_next | btpo_level | btpo_flags 
-------+------+------------+------------+---------------+-----------+-----------+-----------+-----------+------------+------------
     1 | l    |        262 |          0 |            24 |      8192 |       812 |         0 |         2 |          0 |          1
(1 row)
```

SOLUCIÓN: Los nodos hoja tienen 262 registros. Campo live_items  262.

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------


Cuestión 16. Determinar el tamaño de bloques que teóricamente tendría de acuerdo
con lo visto en teoría. Comparar los resultados obtenidos teóricamente con los
resultados obtenidos en la cuestión 15.

Campo matricula.
Orden? -> No -> Unique values -> Sí
Secundario + Campo clave
B+ Siempre denso.

```
pl1=# SELECT avg_leaf_density FROM pgstatindex('idx_matricula_b');)
 avg_leaf_density 
------------------
            90.04
(1 row)
```

Lcontrol=24
B.util=(8192-24) * 90.04/100=7354

Nodo raiz/intermedio: n * LpB + (n-1)*Lkm <=BUtil

(n * 8) + (n-1)*8 <= 7354
8n + 8n -8  <= 7354
n=460

Nodo hoja: nh*(LpB + Lk) + LpB <= Butil
nh*(8 + 8) + 8 <= 7354
16nh + 8 <= 7354
nh=459

Nodos hoja= 20000000/459=43573
Nodos intermedio= 43573 /460=95
Nodos Raiz= 95 /460=1

Tamaño indice= 43573 + 95 + 1 =43669 teóricamente.

Podemos comprobar, que no encaja con la práctica 77010 bloques, la diferencia es mayor, lo que nos demuestra que postgreSQL no esta funcionando como pensabamos teóricamente.

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------


Cuestión 17. Crear un índice de tipo hash para el campo matrícula. ¿Dónde se almacena
físicamente ese índice? ¿Qué tamaño tiene? ¿Cuántos bloques tiene? ¿Cuántos cajones
tiene? ¿Cuántas tuplas tiene de media un cajón? Indicar el procedimiento seguido e
incluir el código SQL utilizado.

```
pl1=# create index indice_hash_matricula on camiones using HASH(matricula);
CREATE INDEX
```


```
pl1=# SELECT pg_relation_filepath('indice_hash_matricula'); 
 pg_relation_filepath 
----------------------
 base/16396/17174
(1 row)
```

```
cd /var/lib/postgresql/16/main/base/16396
root@postgresql01:/var/lib/postgresql/16/main/base/16396# ls -lart 17174
-rw------- 1 postgres postgres 536887296 Mar  2 18:21 17174
```

```
pl1=# SELECT pg_size_pretty(pg_total_relation_size('indice_hash_matricula'));
 pg_size_pretty 
----------------
 512 MB
(1 row)
```

```
root@postgresql01:/var/lib/postgresql/16/main/base/16396# du -sh 17174
513M    17174
```

```
pl1=# SELECT relpages FROM pg_class WHERE relname='indice_hash_matricula';
 relpages 
----------
    65538
(1 row)
```

Número de cajones:

```
SELECT * FROM pgstathashindex('indice_hash_matricula');  
 version | bucket_pages | overflow_pages | bitmap_pages | unused_pages | live_items | dead_items |   free_percent    
---------+--------------+----------------+--------------+--------------+------------+------------+-------------------
       4 |        65536 |              0 |            1 |            0 |   20000000 |          0 | 25.12861107703631
(1 row)
```

Número de tuplas de media:
  Si tenemos 20000000 de registros. 20000000/65536=305 tuplas(registros) de media. 


----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------

Cuestión 18. Determinar el tamaño de bloques que teóricamente tendría de acuerdo
con lo visto en teoría. Comparar los resultados obtenidos teóricamente con los
resultados obtenidos en la cuestión 17.

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
create index indice_hash_matricula on camiones using HASH(matricula);

matricula >> orden >> no >> unique value > sí. Por tanto indice secundario + campo clave.

Nº de cajones= Depende de la función hash que este utilizando postgresql, como no lo sabemos, vamos a partir los de los cajones que hay.
Lcontrol=24
B.util=8192-24= 8168

Nº De cajones= 65536
Nº De registros por Cajón= V(matriculas)/65536= 20000000/65536=305 registros por cajón.
Lric=Lmatricula + Lpr= 8 + 8= 16 bytes
frc= ⌊B.util/Lrc⌋= 8168 / 16 = 510 reg/bloque
bc=⌈ 305/510= 1 bloque /cajón

El indice debería ocupar=  1 * 65536 = 65536 bloques. Como hemos sacado el número de cajones de postgresql, y hemos deducido que para cada cajón necesitamos un bloque, coincide práctica y teoría.



Cuestión 19. ¿Qué conclusiones se puede obtener de la gestión y organización de
PostgreSQL sobre los dos índices árbol y hash que se han creado y han sido analizados?
¿Por qué? Comparar con lo visto en teoría.

Hemos observado que los árboles B+ son altamente eficientes para consultas de rango o claves, mientras que los índices hash son eficientes para buscar un valor específico pero menos eficientes para consultas de rango. En cuanto a las operaciones de inserción y eliminación, los árboles B+ parecen ser más eficientes.

Es importante destacar que al comparar la teoría con la práctica, hemos notado que los árboles B+ no utilizan cajones de punteros como se ha discutido en la teoría, especialmente cuando el campo no clave es secundario. En su lugar, los propios nodos hoja almacenan los registros de los campos, sin depender de otra estructura subyacente de cajones de punteros.

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------


Cuestión 20. Crear un índice primario tipo árbol sobre el campo kilómetros. También
crear un índice hash sobre el campo id_camion y otro sobre kilómetros. ¿Cuál ha sido
el proceso seguido para crear cada tipo de índice? Incluir el código SQL utilizado para
ello.

Podemos crear un indice sobre el campo kilometros de tipo BTree, pero no será primario, puesto que la tabla no esta ordenado por el campo kilómetros.

```
create index idx_kilometros ON camiones (kilometros);
pl1=# create index indice_HASH_idcamion on camiones using HASH(id_camion);
CREATE INDEX
pl1=# create index indice_HASH_kilometro on camiones using HASH(kilometros);
CREATE INDEX
```

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------


Cuestión 21. Para cada una de las consultas que se muestran a continuación, ¿Qué
información se puede obtener de los datos monitorizados por la base de datos al
realizar la consulta? Comentar cómo se ha realizado la resolución de la consulta.
¿Cuántos bloques se han leído de cada estructura? ¿Por qué? Comparar con lo visto en
teoría. Importante, reinicializar los datos recolectados de la actividad de la base de
datos antes de lanzar cada consulta. 


1. Mostrar la información de las tuplas con 50000 km.

```
pl1=# SELECT * FROM pg_stat_reset();
 pg_stat_reset 
---------------
(1 row)
```

```
pl1=# SELECT * FROM pg_statio_user_tables WHERE relname='camiones' ;
 relid | schemaname | relname  | heap_blks_read | heap_blks_hit | idx_blks_read | idx_blks_hit | toast_blks_read | toast_blks_hit | tidx_blks_read | tidx_blks_hit 
-------+------------+----------+----------------+---------------+---------------+--------------+-----------------+----------------+----------------+---------------
 17060 | public     | camiones |              0 |             0 |             0 |            0 |                 |                |                |              
(1 row)
```

```
SELECT * FROM pg_stat_user_indexes;
 relid | indexrelid | schemaname |   relname    |      indexrelname      | idx_scan | last_idx_scan | idx_tup_read | idx_tup_fetch 
-------+------------+------------+--------------+------------------------+----------+---------------+--------------+---------------
 17060 |      17064 | public     | camiones     | camiones_pkey          |        0 |               |            0 |             0
 17060 |      17066 | public     | camiones     | camiones_id_camion_key |        0 |               |            0 |             0
 17060 |      17069 | public     | camiones     | idx_kilometros         |        0 |               |            0 |             0
 17119 |      17123 | public     | camiones3_p0 | camiones3_p0_pkey      |        0 |               |            0 |             0
 17060 |      17170 | public     | camiones     | idx_kilometros1        |        0 |               |            0 |             0
 17060 |      17171 | public     | camiones     | indice_hash            |        0 |               |            0 |             0
 17060 |      17172 | public     | camiones     | idx_matricula_b        |        0 |               |            0 |             0
 17060 |      17174 | public     | camiones     | indice_hash_matricula  |        0 |               |            0 |             0
 17060 |      17175 | public     | camiones     | indice_hash_idcamion   |        0 |               |            0 |             0
 17060 |      17176 | public     | camiones     | indice_hash_kilometro  |        0 |               |            0 |             0
(10 rows)
```

```
SELECT * FROM camiones WHERE kilometros='50000'; 
```
```
 SELECT * FROM pg_statio_user_tables WHERE relname='camiones' ;
 relid | schemaname | relname  | heap_blks_read | heap_blks_hit | idx_blks_read | idx_blks_hit | toast_blks_read | toast_blks_hit | tidx_blks_read | tidx_blks_hit 
-------+------------+----------+----------------+---------------+---------------+--------------+-----------------+----------------+----------------+---------------
 17060 | public     | camiones |              0 |            34 |             0 |            1 |                 |                |                |              
(1 row)
```

```
pl1=# SELECT * FROM pg_stat_user_indexes;
 relid | indexrelid | schemaname |   relname    |      indexrelname      | idx_scan |         last_idx_scan         | idx_tup_read | idx_tup_fetch 
-------+------------+------------+--------------+------------------------+----------+-------------------------------+--------------+---------------
 17060 |      17064 | public     | camiones     | camiones_pkey          |        0 |                               |            0 |             0
 17060 |      17066 | public     | camiones     | camiones_id_camion_key |        0 |                               |            0 |             0
 17060 |      17069 | public     | camiones     | idx_kilometros         |        0 |                               |            0 |             0
 17119 |      17123 | public     | camiones3_p0 | camiones3_p0_pkey      |        0 |                               |            0 |             0
 17060 |      17170 | public     | camiones     | idx_kilometros1        |        0 |                               |            0 |             0
 17060 |      17171 | public     | camiones     | indice_hash            |        0 |                               |            0 |             0
 17060 |      17172 | public     | camiones     | idx_matricula_b        |        0 |                               |            0 |             0
 17060 |      17174 | public     | camiones     | indice_hash_matricula  |        0 |                               |            0 |             0
 17060 |      17175 | public     | camiones     | indice_hash_idcamion   |        0 |                               |            0 |             0
 17060 |      17176 | public     | camiones     | indice_hash_kilometro  |        1 | 2024-03-02 20:13:50.350959+00 |           34 |             0
 ```


Nos dice que no ha tenido que ir a disco para leer los datos, los ha cargado de cache. Ademas nos dice que ha cargado 34 bloques desde cache. Parece que ha usado un indice, un bloque, para leer, también de cache.
Viendo el uso de indices, vemos como ha recogido 34 tuplas. Con un bloque de indice, ha conseguido recuperarnos 34 tuplas, las cuales parecen estar en 34 bloques. Podemos ver que el indice que ha usado es de tipo hash.

 ```
pl1=# SELECT COUNT(*) FROM camiones WHERE kilometros = '50000';
 count 
-------
    34
(1 row)
 ```
 
Si contamos el número de tuplas que se obtienen, cuadra.

Cuando creamos un indice de tipo hash sobre KM, vimos que teóricamente cada cajón hash debería ser de un bloque, y que el cajón de punteros que se debería crear puesto que estamos ante un campo secundario+ campo no clave, también sería de un bloque.
Para leer deberiamos Coster un coste de 2 bloques por indice hash, más los datos obtenidos, puedo que cada cajón de punteros tiene 40 registros(estimación), el coste sería 1 + 1*40= 40 bloques. No muy dispar con lo encontrado.


----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------


2. Mostrar la información de la tupla con id_camion igual a 30000.


```
pl1=# SELECT * FROM pg_stat_reset();
 pg_stat_reset 
---------------
(1 row)
```

```
SELECT * FROM camiones WHERE id_camion='30000'; 
```

```
pl1=#  SELECT * FROM pg_statio_user_tables WHERE relname='camiones' ;
 relid | schemaname | relname  | heap_blks_read | heap_blks_hit | idx_blks_read | idx_blks_hit | toast_blks_read | toast_blks_hit | tidx_blks_read | tidx_blks_hit 
-------+------------+----------+----------------+---------------+---------------+--------------+-----------------+----------------+----------------+---------------
 17060 | public     | camiones |              1 |             0 |             2 |            0 |                 |                |                |              
(1 row)
```

```
pl1=# SELECT * FROM pg_stat_user_indexes;
 relid | indexrelid | schemaname |   relname    |      indexrelname      | idx_scan |         last_idx_scan         | idx_tup_read | idx_tup_fetch 
-------+------------+------------+--------------+------------------------+----------+-------------------------------+--------------+---------------
 17060 |      17064 | public     | camiones     | camiones_pkey          |        0 |                               |            0 |             0
 17060 |      17066 | public     | camiones     | camiones_id_camion_key |        0 |                               |            0 |             0
 17060 |      17069 | public     | camiones     | idx_kilometros         |        0 |                               |            0 |             0
 17119 |      17123 | public     | camiones3_p0 | camiones3_p0_pkey      |        0 |                               |            0 |             0
 17060 |      17170 | public     | camiones     | idx_kilometros1        |        0 |                               |            0 |             0
 17060 |      17171 | public     | camiones     | indice_hash            |        0 |                               |            0 |             0
 17060 |      17172 | public     | camiones     | idx_matricula_b        |        0 |                               |            0 |             0
 17060 |      17174 | public     | camiones     | indice_hash_matricula  |        0 |                               |            0 |             0
 17060 |      17175 | public     | camiones     | indice_hash_idcamion   |        1 | 2024-03-02 20:26:11.947903+00 |            1 |             1
 17060 |      17176 | public     | camiones     | indice_hash_kilometro  |        0 |                               |            0 |             0
(10 rows)
```

Ha tenido que leer en disco un bloque, y leerse de disco dos bloques de indice. Al no usar caches, habrá sido una busqueda mas lenta. Un coste de 3 bloques
Parece que ha utilizado indice indice_hash_idcamion, el cual le ha devuelto una tupla.

id_camion es un campo con orden y valor único, Por tanto en indice hash sobre él sera de tipo primario campo clave. 


```
SELECT * FROM pgstathashindex('indice_hash_idcamion');  
 version | bucket_pages | overflow_pages | bitmap_pages | unused_pages | live_items | dead_items |   free_percent    
---------+--------------+----------------+--------------+--------------+------------+------------+-------------------
       4 |        65536 |              0 |            1 |            0 |   20000000 |          0 | 25.12861107703631
(1 row)
```

Parece que ha creado un indice que hash que necesita 65536 bloques. Puesto que es primario campo clave, cada cajón debería tener 20000000/65536=305 registros por cajón.

Lric=id_camion + Lpr= 4 + 8= 12 bytes
frc= ⌊B.util/Lrc⌋= 8168 / 12 = 680 reg/bloque
bc=⌈ 305/680= 1 bloque /cajón

Teóricamente, deberia haber consumido un bloque de indice, mas un bloque donde esta el dato. Lo cual no cuadra del todo con la práctica, ya que nos dice que para el indice ha necesitado dos bloques. Esto se debe a que cada cajón del hash debe requerir por lo menos dos bloques. 


----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------



3. Contar el número de camiones que tienen más de 400000 km.

```
pl1=# SELECT * FROM pg_stat_reset();
 pg_stat_reset 
---------------
 
(1 row)
```

```
pl1=# SELECT COUNT(*) FROM camiones WHERE kilometros > 400000;
  count  
---------
 4002190
(1 row)

pl1=# 
```

```
pl1=# SELECT * FROM pg_statio_user_tables WHERE relname='camiones' ;
 relid | schemaname | relname  | heap_blks_read | heap_blks_hit | idx_blks_read | idx_blks_hit | toast_blks_read | toast_blks_hit | tidx_blks_read | tidx_blks_hit 
-------+------------+----------+----------------+---------------+---------------+--------------+-----------------+----------------+----------------+---------------
 17060 | public     | camiones |              0 |        597542 |             0 |         3539 |                 |                |                |              
(1 row)
```

COSTE TOTAL= 597542 + 3539=601081 bloques

```
pl1=# SELECT * FROM pg_stat_user_indexes;
 relid | indexrelid | schemaname |   relname    |      indexrelname      | idx_scan |        last_idx_scan         | idx_tup_read | idx_tup_fetch 
-------+------------+------------+--------------+------------------------+----------+------------------------------+--------------+---------------
 17060 |      17064 | public     | camiones     | camiones_pkey          |        0 |                              |            0 |             0
 17060 |      17066 | public     | camiones     | camiones_id_camion_key |        0 |                              |            0 |             0
 17060 |      17069 | public     | camiones     | idx_kilometros         |        0 |                              |            0 |             0
 17119 |      17123 | public     | camiones3_p0 | camiones3_p0_pkey      |        0 |                              |            0 |             0
 17060 |      17170 | public     | camiones     | idx_kilometros1        |        3 | 2024-03-02 20:47:32.95768+00 |      4002190 |             0
 17060 |      17171 | public     | camiones     | indice_hash            |        0 |                              |            0 |             0
 17060 |      17172 | public     | camiones     | idx_matricula_b        |        0 |                              |            0 |             0
 17060 |      17174 | public     | camiones     | indice_hash_matricula  |        0 |                              |            0 |             0
 17060 |      17175 | public     | camiones     | indice_hash_idcamion   |        0 |                              |            0 |             0
 17060 |      17176 | public     | camiones     | indice_hash_kilometro  |        0 |                              |            0 |             0
(10 rows)
```


Para esta consulta ha leido 597542 bloques de cache de datos, y 3539 bloques de cache de indices.
Vemos que el indice utilizado ha sido idx_kilometros1.
public | idx_kilometros1        | index             | postgres | camiones     | permanent   | btree         | 139 MB     | 


Para cada busqueda  1 bloque raiz + 1 bloque intermedio  + 1  bloque hoja + n bloque dato. Como hemos visto, aunque debería haber teóricamente un cajón de punteros, los nodos hojas están ya guardando todas las direcciones. Si es como creemos, tendra ordenados los datos en el arbol, hay 4002190 registros que cumplen esa condición, si cada nodo hoja tenía unos 30 = 133407 , debería haber necesitado 133407 bloques, pero parece que solo ha necesitado 3539. Lo cual nos hace suponer que hay una estragia distinta y que no podemos comparar con la teoría.


----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------


4. Mostrar el número de camiones de cada empresa.

```
SELECT * FROM pg_stat_reset();
```

```
SELECT empresa, COUNT(*) AS cantidad_de_camiones FROM camiones GROUP BY empresa;
```

```
pl1=# SELECT * FROM pg_statio_user_tables WHERE relname='camiones' ;
 relid | schemaname | relname  | heap_blks_read | heap_blks_hit | idx_blks_read | idx_blks_hit | toast_blks_read | toast_blks_hit | tidx_blks_read | tidx_blks_hit 
-------+------------+----------+----------------+---------------+---------------+--------------+-----------------+----------------+----------------+---------------
 17060 | public     | camiones |         180621 |           131 |             0 |            0 |                 |                |                |              
(1 row)
```

```
pl1=# SELECT * FROM pg_stat_user_indexes;
 relid | indexrelid | schemaname |   relname    |      indexrelname      | idx_scan | last_idx_scan | idx_tup_read | idx_tup_fetch 
-------+------------+------------+--------------+------------------------+----------+---------------+--------------+---------------
 17060 |      17064 | public     | camiones     | camiones_pkey          |        0 |               |            0 |             0
 17060 |      17066 | public     | camiones     | camiones_id_camion_key |        0 |               |            0 |             0
 17060 |      17069 | public     | camiones     | idx_kilometros         |        0 |               |            0 |             0
 17119 |      17123 | public     | camiones3_p0 | camiones3_p0_pkey      |        0 |               |            0 |             0
 17060 |      17170 | public     | camiones     | idx_kilometros1        |        0 |               |            0 |             0
 17060 |      17171 | public     | camiones     | indice_hash            |        0 |               |            0 |             0
 17060 |      17172 | public     | camiones     | idx_matricula_b        |        0 |               |            0 |             0
 17060 |      17174 | public     | camiones     | indice_hash_matricula  |        0 |               |            0 |             0
 17060 |      17175 | public     | camiones     | indice_hash_idcamion   |        0 |               |            0 |             0
 17060 |      17176 | public     | camiones     | indice_hash_kilometro  |        0 |               |            0 |             0
(10 rows)
```

Ha leido 180621 bloques de disco, 131 bloques de cache. Podemos ver que no ha utilizado ningún indice. 
180621+131=180752

 ```
SELECT  relpages FROM   pg_class WHERE  relname = 'camiones';
 relpages 
----------
   180752
(1 row)
 ```
Lo que comprobamos es que se ha leido todos los bloques, lo cual tiene sentido para este tipo de busqueda.


----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------


5. Insertar un nuevo camión en la tabla camiones con 30000 km.

 ```
pl1=# SELECT * FROM camiones ORDER BY id_camion DESC LIMIT 1;
 id_camion | matricula |      empresa      | kilometros 
-----------+-----------+-------------------+------------
  20000000 | RJZ5230   | Anpulo Food, Inc. |     294952
 ```

  ```
SELECT * FROM pg_stat_reset();
 ```
 ``` 
pl1=# INSERT INTO camiones (id_camion, matricula, empresa, kilometros) VALUES (20000002, 'UAH6109', 'UAHTransporte', 30000);
INSERT 0 1
 ```

 ```
pl1=# SELECT * FROM pg_statio_user_tables WHERE relname='camiones' ;
 relid | schemaname | relname  | heap_blks_read | heap_blks_hit | idx_blks_read | idx_blks_hit | toast_blks_read | toast_blks_hit | tidx_blks_read | tidx_blks_hit 
-------+------------+----------+----------------+---------------+---------------+--------------+-----------------+----------------+----------------+---------------
 17060 | public     | camiones |              1 |             3 |             6 |           17 |                 |                |                |              
(1 row)
 ```

 ```
pl1=# SELECT * FROM pg_stat_user_indexes;
 relid | indexrelid | schemaname |   relname    |      indexrelname      | idx_scan | last_idx_scan | idx_tup_read | idx_tup_fetch 
-------+------------+------------+--------------+------------------------+----------+---------------+--------------+---------------
 17060 |      17064 | public     | camiones     | camiones_pkey          |        0 |               |            0 |             0
 17060 |      17066 | public     | camiones     | camiones_id_camion_key |        0 |               |            0 |             0
 17060 |      17069 | public     | camiones     | idx_kilometros         |        0 |               |            0 |             0
 17119 |      17123 | public     | camiones3_p0 | camiones3_p0_pkey      |        0 |               |            0 |             0
 17060 |      17170 | public     | camiones     | idx_kilometros1        |        0 |               |            0 |             0
 17060 |      17171 | public     | camiones     | indice_hash            |        0 |               |            0 |             0
 17060 |      17172 | public     | camiones     | idx_matricula_b        |        0 |               |            0 |             0
 17060 |      17174 | public     | camiones     | indice_hash_matricula  |        0 |               |            0 |             0
 17060 |      17175 | public     | camiones     | indice_hash_idcamion   |        0 |               |            0 |             0
 17060 |      17176 | public     | camiones     | indice_hash_kilometro  |        0 |               |            0 |             0
(10 rows)
 ```

Ha utilizado un bloque de disco de datos, 3 bloques de cache para datos, 6 bloques de disco de indices, y 17 bloques de cache de indices.
Como vemos, aunque ha usado los bloques de indices, para actualizar, no los ha utilziado para leer. 


----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
6. Actualizar los kilómetros del camión insertado anteriormente para cambiar de
30000 a 20000 km.

 ```
pl1=# SELECT * FROM pg_stat_reset();
 pg_stat_reset 
---------------
(1 row)
 ```

 ```
pl1=# UPDATE camiones SET kilometros = 20000 WHERE matricula = 'UAH6109';
UPDATE 1
```

```
pl1=# SELECT * FROM pg_statio_user_tables WHERE relname='camiones' ;
 relid | schemaname | relname  | heap_blks_read | heap_blks_hit | idx_blks_read | idx_blks_hit | toast_blks_read | toast_blks_hit | tidx_blks_read | tidx_blks_hit 
-------+------------+----------+----------------+---------------+---------------+--------------+-----------------+----------------+----------------+---------------
 17060 | public     | camiones |              1 |             8 |             5 |           19 |                 |                |                |              
(1 row)

```

```
pl1=# SELECT * FROM pg_stat_user_indexes;
 relid | indexrelid | schemaname |   relname    |      indexrelname      | idx_scan |         last_idx_scan         | idx_tup_read | idx_tup_fetch 
-------+------------+------------+--------------+------------------------+----------+-------------------------------+--------------+---------------
 17060 |      17064 | public     | camiones     | camiones_pkey          |        0 |                               |            0 |             0
 17060 |      17066 | public     | camiones     | camiones_id_camion_key |        0 |                               |            0 |             0
 17060 |      17069 | public     | camiones     | idx_kilometros         |        0 |                               |            0 |             0
 17119 |      17123 | public     | camiones3_p0 | camiones3_p0_pkey      |        0 |                               |            0 |             0
 17060 |      17170 | public     | camiones     | idx_kilometros1        |        0 |                               |            0 |             0
 17060 |      17171 | public     | camiones     | indice_hash            |        0 |                               |            0 |             0
 17060 |      17172 | public     | camiones     | idx_matricula_b        |        0 |                               |            0 |             0
 17060 |      17174 | public     | camiones     | indice_hash_matricula  |        1 | 2024-03-02 22:49:40.857114+00 |            1 |             1
 17060 |      17175 | public     | camiones     | indice_hash_idcamion   |        0 |                               |            0 |             0
 17060 |      17176 | public     | camiones     | indice_hash_kilometro  |        0 |                               |            0 |             0
(10 rows)
```

Ha utilizado 1 bloque de disco de datos, 8 bloques de disco de cache, 5 bloques de disco de indices, un bloque de cache de indices.
Lo importente es que al ser un update, vemos como si ha utilizado el indice, tiene sentido, utiliza el indice para buscar el elemento, para después cambiarlo.

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------


7. Mostrar los datos de los camiones que tienen un id_camion entre 80000 y
100000.

 ```
pl1=# SELECT * FROM pg_stat_reset();
 pg_stat_reset 
---------------
(1 row)
 ```

 ```
SELECT * FROM camiones WHERE id_camion BETWEEN 80000 AND 100000;
 ```

```
pl1=# SELECT * FROM pg_statio_user_tables WHERE relname='camiones' ;
 relid | schemaname | relname  | heap_blks_read | heap_blks_hit | idx_blks_read | idx_blks_hit | toast_blks_read | toast_blks_hit | tidx_blks_read | tidx_blks_hit 
-------+------------+----------+----------------+---------------+---------------+--------------+-----------------+----------------+----------------+---------------
 17060 | public     | camiones |              0 |           185 |             0 |           64 |                 |                |                |              
(1 row)
 ```


 ```
pl1=# SELECT * FROM pg_stat_user_indexes;
 relid | indexrelid | schemaname |   relname    |      indexrelname      | idx_scan |         last_idx_scan         | idx_tup_read | idx_tup_fetch 
-------+------------+------------+--------------+------------------------+----------+-------------------------------+--------------+---------------
 17060 |      17064 | public     | camiones     | camiones_pkey          |        0 |                               |            0 |             0
 17060 |      17066 | public     | camiones     | camiones_id_camion_key |        3 | 2024-03-02 22:54:23.424588+00 |        20003 |         20001
 17060 |      17069 | public     | camiones     | idx_kilometros         |        0 |                               |            0 |             0
 17119 |      17123 | public     | camiones3_p0 | camiones3_p0_pkey      |        0 |                               |            0 |             0
 17060 |      17170 | public     | camiones     | idx_kilometros1        |        0 |                               |            0 |             0
 17060 |      17171 | public     | camiones     | indice_hash            |        0 |                               |            0 |             0
 17060 |      17172 | public     | camiones     | idx_matricula_b        |        0 |                               |            0 |             0
 17060 |      17174 | public     | camiones     | indice_hash_matricula  |        0 |                               |            0 |             0
 17060 |      17175 | public     | camiones     | indice_hash_idcamion   |        0 |                               |            0 |             0
 17060 |      17176 | public     | camiones     | indice_hash_kilometro  |        0 |                               |            0 |             0
(10 rows)
 ```

Ha utizado 185 bloques de cache de datos, y 64 bloque de cache de indice.

```
public | camiones_id_camion_key | index             | postgres | camiones     | permanent   | btree         | 428 MB     | 
 ```
Es un indice B+, y puesto que es un indice primario + campo clave, al estar ordenado, el arbol debería encontrar el primer elemento, e ir obteniendo el resto sin tener que seguir buscando.

 ```
pl1=# SELECT * FROM pgstatindex('camiones_id_camion_key');
 version | tree_level | index_size | root_block_no | internal_pages | leaf_pages | empty_pages | deleted_pages | avg_leaf_density | leaf_fragmentation 
---------+------------+------------+---------------+----------------+------------+-------------+---------------+------------------+--------------------
       4 |          2 |  449241088 |           412 |            193 |      54645 |           0 |             0 |            90.09 |                  0
(1 row)
 ```

Número de nodos hoja=  54645


nrc=nr/FR=20000000/
B = 8.192 bytes
Lcontrol=24
B.util=8192-24= 8168
LR=Lid_camion +  Lmatricula +  Lempresa +  Lkilometros = 4 + 8 + 100 + 4 =116
FR= B.util/LR= 70 reg/bloque
Br=nr/FR= 20000000/70=285715 bloque
ncr=nr/Vid_camion=20000000/20000000=1;

Coste= 1 raiz + 1 intermedio + 1 hoja + nrc/FR= 1 raiz + 1 intermedio + 1 hoja + nv * nrc/FR= 1 raiz + 1 intermedio + 1 hoja + 1* 20000/70 = 286  bloques.
Con la teoría no nos cuadra que tenga que consumir 64 bloques del indice, al tratarse de un B+ sobre un campo ordenado, debería bajar por el arbol para caer en el primer registro y recorrer de forma secuencial limitada los registros.  La diferencia es de 185 a 286 bloques teóricos.


----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------

Cuestión 22. Borrar los índices creados en la cuestión 20. Crear un índice multiclave
tipo árbol sobre los campos empresa y kilómetros. Incluir el código SQL utilizado para
ello.

 ```
pl1=# \di+
                                                           List of relations
 Schema |          Name          |       Type        |  Owner   |    Table     | Persistence | Access method |    Size    | Description 
--------+------------------------+-------------------+----------+--------------+-------------+---------------+------------+-------------
 public | camiones3_p0_pkey      | index             | postgres | camiones3_p0 | permanent   | btree         | 8192 bytes | 
 public | camiones3_pkey         | partitioned index | postgres | camiones3    | permanent   | btree         | 0 bytes    | 
 public | camiones_id_camion_key | index             | postgres | camiones     | permanent   | btree         | 428 MB     | 
 public | camiones_pkey          | index             | postgres | camiones     | permanent   | btree         | 773 MB     | 
 public | idx_kilometros         | index             | postgres | camiones     | permanent   | btree         | 139 MB     | 
 public | idx_kilometros1        | index             | postgres | camiones     | permanent   | btree         | 139 MB     | 
 public | idx_matricula_b        | index             | postgres | camiones     | permanent   | btree         | 602 MB     | 
 public | indice_hash            | index             | postgres | camiones     | permanent   | hash          | 603 MB     | 
 public | indice_hash_idcamion   | index             | postgres | camiones     | permanent   | hash          | 512 MB     | 
 public | indice_hash_kilometro  | index             | postgres | camiones     | permanent   | hash          | 603 MB     | 
 public | indice_hash_matricula  | index             | postgres | camiones     | permanent   | hash          | 512 MB     | 
(11 rows)
 ```

 ```
pl1=# DROP INDEX idx_kilometros;
DROP INDEX
pl1=# DROP INDEX indice_HASH_idcamion;
DROP INDEX
pl1=# DROP INDEX indice_HASH_kilometro;
DROP INDEX
 ```

```
 pl1=# \di+
                                                           List of relations
 Schema |          Name          |       Type        |  Owner   |    Table     | Persistence | Access method |    Size    | Description 
--------+------------------------+-------------------+----------+--------------+-------------+---------------+------------+-------------
 public | camiones3_p0_pkey      | index             | postgres | camiones3_p0 | permanent   | btree         | 8192 bytes | 
 public | camiones3_pkey         | partitioned index | postgres | camiones3    | permanent   | btree         | 0 bytes    | 
 public | camiones_id_camion_key | index             | postgres | camiones     | permanent   | btree         | 428 MB     | 
 public | camiones_pkey          | index             | postgres | camiones     | permanent   | btree         | 773 MB     | 
 public | idx_kilometros1        | index             | postgres | camiones     | permanent   | btree         | 139 MB     | 
 public | idx_matricula_b        | index             | postgres | camiones     | permanent   | btree         | 602 MB     | 
 public | indice_hash            | index             | postgres | camiones     | permanent   | hash          | 603 MB     | 
 public | indice_hash_matricula  | index             | postgres | camiones     | permanent   | hash          | 512 MB     | 
(8 rows)

```

```
pl1=# CREATE INDEX  indice_empresa_km_btree ON camiones (empresa, kilometros);
CREATE INDEX
```

```
CREATE INDEX indice_empresa_km_hash on camiones using HASH(empresa, kilometros);
ERROR:  access method "hash" does not support multicolumn indexes
```
No es posible hash multicolum. Hacemos uno para cada campo.

```
pl1=# CREATE INDEX indice_empresa_hash on camiones using HASH(empresa);
CREATE INDEX
pl1=# CREATE INDEX indice_km_hash on camiones using HASH(kilometros);
CREATE INDEX
```

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
Cuestión 23. Para cada una de las consultas que se muestran a continuación, ¿Qué
información se puede obtener de los datos monitorizados por la base de datos al
realizar la consulta? Comentar cómo se ha realizado la resolución de la consulta.
¿Cuántos bloques se han leído de cada estructura? ¿Por qué? Importante, reinicializar
los datos recolectados de la actividad de la base de datos antes de lanzar cada consulta


1. Mostrar el número de camiones que tiene la empresa UPS.

```
SELECT * FROM pg_stat_reset();
```

```
pl1=# select COUNT(*) from camiones where empresa='UPS';
 count 
-------
  2020
(1 row)
```

```
SELECT * FROM pg_statio_user_tables WHERE relname='camiones' ;
```

```
pl1=# SELECT * FROM pg_statio_user_tables WHERE relname='camiones' ;
 relid | schemaname | relname  | heap_blks_read | heap_blks_hit | idx_blks_read | idx_blks_hit | toast_blks_read | toast_blks_hit | tidx_blks_read | tidx_blks_hit 
-------+------------+----------+----------------+---------------+---------------+--------------+-----------------+----------------+----------------+---------------
 17060 | public     | camiones |              0 |          1682 |             0 |            9 |                 |                |                |              
(1 row)
```

```
pl1=# SELECT * FROM pg_stat_user_indexes;
 relid | indexrelid | schemaname |   relname    |      indexrelname       | idx_scan |         last_idx_scan         | idx_tup_read | idx_tup_fetch 
-------+------------+------------+--------------+-------------------------+----------+-------------------------------+--------------+---------------
 17060 |      17064 | public     | camiones     | camiones_pkey           |        0 |                               |            0 |             0
 17060 |      17066 | public     | camiones     | camiones_id_camion_key  |        0 |                               |            0 |             0
 17119 |      17123 | public     | camiones3_p0 | camiones3_p0_pkey       |        0 |                               |            0 |             0
 17060 |      17170 | public     | camiones     | idx_kilometros1         |        0 |                               |            0 |             0
 17060 |      17171 | public     | camiones     | indice_hash             |        0 |                               |            0 |             0
 17060 |      17172 | public     | camiones     | idx_matricula_b         |        0 |                               |            0 |             0
 17060 |      17174 | public     | camiones     | indice_hash_matricula   |        0 |                               |            0 |             0
 17060 |      17178 | public     | camiones     | indice_empresa_km_btree |        1 | 2024-03-03 00:03:41.801977+00 |         2020 |             0
 17060 |      17179 | public     | camiones     | indice_empresa_hash     |        0 |                               |            0 |             0
 17060 |      17180 | public     | camiones     | indice_km_hash          |        0 |                               |            0 |             0
(10 rows)
```

Se leen 1682 bloque de cache de datos, y 9 bloques de cache de indice. Vemos que se han devuelto 2020 resultados, observerse que indice es justo el número de tuplas que nos ha devuelto.
El indice utilizado es el indice_empresa_km_btree. Ha utilizado este indice que indexa dos valores, puesto que tiene la empresa, lo puede utilizar.

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------

2. Mostrar la información de los camiones que son de la empresa UPS o que tienen
90000 km.

```
SELECT * FROM pg_stat_reset();
```

```
SELECT * FROM camiones WHERE empresa = 'UPS' OR kilometros = 90000;
```

```
pl1=# SELECT * FROM pg_statio_user_tables WHERE relname='camiones' ;
 relid | schemaname | relname  | heap_blks_read | heap_blks_hit | idx_blks_read | idx_blks_hit | toast_blks_read | toast_blks_hit | tidx_blks_read | tidx_blks_hit 
-------+------------+----------+----------------+---------------+---------------+--------------+-----------------+----------------+----------------+---------------
 17060 | public     | camiones |             40 |          2003 |             1 |            6 |                 |                |                |              
(1 row)
```

```
pl1=# SELECT * FROM pg_stat_user_indexes;
 relid | indexrelid | schemaname |   relname    |      indexrelname       | idx_scan |         last_idx_scan         | idx_tup_read | idx_tup_fetch 
-------+------------+------------+--------------+-------------------------+----------+-------------------------------+--------------+---------------
 17060 |      17064 | public     | camiones     | camiones_pkey           |        0 |                               |            0 |             0
 17060 |      17066 | public     | camiones     | camiones_id_camion_key  |        0 |                               |            0 |             0
 17119 |      17123 | public     | camiones3_p0 | camiones3_p0_pkey       |        0 |                               |            0 |             0
 17060 |      17170 | public     | camiones     | idx_kilometros1         |        0 |                               |            0 |             0
 17060 |      17171 | public     | camiones     | indice_hash             |        0 |                               |            0 |             0
 17060 |      17172 | public     | camiones     | idx_matricula_b         |        0 |                               |            0 |             0
 17060 |      17174 | public     | camiones     | indice_hash_matricula   |        0 |                               |            0 |             0
 17060 |      17178 | public     | camiones     | indice_empresa_km_btree |        0 |                               |            0 |             0
 17060 |      17179 | public     | camiones     | indice_empresa_hash     |        1 | 2024-03-03 00:09:01.105427+00 |         2020 |             0
 17060 |      17180 | public     | camiones     | indice_km_hash          |        1 | 2024-03-03 00:09:01.105427+00 |           40 |             0
(10 rows)
```

Se leen 40 bloques de disco de datos, 2003 bloques de cache de datos, 1 bloque de disco de indices, 6 bloques de  cache de indices 
Al ser un OR, siempre tenemos la opción de secuencia sobre toda la tabla, o la suma de dos busquedas. En este caso podemos ver que ha usado los dos indices hash que hay, uno para empresa y el otro para KM.
Ha considerado que la suma de las dos busquedas era más rápida que leerse toda la tabla.

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------

3. Mostrar la información de los camiones de la empresa UPS que tienen 60000 km.


```
SELECT * FROM pg_stat_reset();
```

```
SELECT * FROM camiones WHERE empresa = 'UPS' AND kilometros = 60000;
```

```
pl1=# SELECT * FROM pg_statio_user_tables WHERE relname='camiones' ;
 relid | schemaname | relname  | heap_blks_read | heap_blks_hit | idx_blks_read | idx_blks_hit | toast_blks_read | toast_blks_hit | tidx_blks_read | tidx_blks_hit 
-------+------------+----------+----------------+---------------+---------------+--------------+-----------------+----------------+----------------+---------------
 17060 | public     | camiones |              0 |             0 |             0 |            4 |                 |                |                |              
(1 row)
```

```
pl1=# SELECT * FROM pg_stat_user_indexes;
 relid | indexrelid | schemaname |   relname    |      indexrelname       | idx_scan |         last_idx_scan         | idx_tup_read | idx_tup_fetch 
-------+------------+------------+--------------+-------------------------+----------+-------------------------------+--------------+---------------
 17060 |      17064 | public     | camiones     | camiones_pkey           |        0 |                               |            0 |             0
 17060 |      17066 | public     | camiones     | camiones_id_camion_key  |        0 |                               |            0 |             0
 17119 |      17123 | public     | camiones3_p0 | camiones3_p0_pkey       |        0 |                               |            0 |             0
 17060 |      17170 | public     | camiones     | idx_kilometros1         |        0 |                               |            0 |             0
 17060 |      17171 | public     | camiones     | indice_hash             |        0 |                               |            0 |             0
 17060 |      17172 | public     | camiones     | idx_matricula_b         |        0 |                               |            0 |             0
 17060 |      17174 | public     | camiones     | indice_hash_matricula   |        0 |                               |            0 |             0
 17060 |      17178 | public     | camiones     | indice_empresa_km_btree |        1 | 2024-03-03 00:14:23.266243+00 |            0 |             0
 17060 |      17179 | public     | camiones     | indice_empresa_hash     |        0 |                               |            0 |             0
 17060 |      17180 | public     | camiones     | indice_km_hash          |        0 |                               |            0 |             0
(10 rows)
```

Se ha utilizado 4 bloques de cache de indice.
Al tener un indce multiclave, indice_empresa_km_btreem, lo único que ha sido buscar en indice la combinación de ambas claves, al no encontrarla en el arbol, no necesita ir a datos, y la busqueda tiene un coste ridículo.

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------


Cuestión 24. Crear la tabla camiones3 particionada por rangos de 50.000 en 50.000 km hasta un máximo de 500000 km. Para cada una de las consultas que se muestran
a continuación, ¿Qué información se puede obtener de los datos monitorizados por la
base de datos al realizar la consulta? Comentar cómo se ha realizado la resolución de
la consulta. ¿Cuántos bloques se han leído de cada estructura? ¿Por qué? Comparar
con la teoría. Importante, reinicializar los datos recolectados de la actividad de la base
de datos antes de lanzar cada consulta.

```
CREATE TABLE camiones3 (id_camion SERIAL , matricula CHAR(8), empresa VARCHAR(100), kilometros INT) PARTITION BY RANGE (kilometros);
```

```
CREATE TABLE camiones3_p0 PARTITION OF camiones3 FOR VALUES FROM (0) TO (50000);
CREATE TABLE camiones3_p1 PARTITION OF camiones3 FOR VALUES FROM (50000)  TO (100000);
CREATE TABLE camiones3_p2 PARTITION OF camiones3 FOR VALUES FROM (100000) TO (150000);
CREATE TABLE camiones3_p3 PARTITION OF camiones3 FOR VALUES FROM (150000) TO (200000);
CREATE TABLE camiones3_p4 PARTITION OF camiones3 FOR VALUES FROM (200000) TO (250000);
CREATE TABLE camiones3_p5 PARTITION OF camiones3 FOR VALUES FROM (250000) TO (300000);
CREATE TABLE camiones3_p6 PARTITION OF camiones3 FOR VALUES FROM (300000) TO (350000);
CREATE TABLE camiones3_p7 PARTITION OF camiones3 FOR VALUES FROM (350000) TO (400000);
CREATE TABLE camiones3_p8 PARTITION OF camiones3 FOR VALUES FROM (400000) TO (450000);
CREATE TABLE camiones3_p9 PARTITION OF camiones3 FOR VALUES FROM (450000) TO (500001);
```

```
pl1=# \copy camiones3(id_camion,matricula,empresa,kilometros) FROM '/tmp/0000.dat' DELIMITER ';' CSV
COPY 20000000
```
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------



1. Mostrar el número de camiones con más de 600000 km.

```
SELECT * FROM pg_stat_reset();
```
```
pl1=# SELECT COUNT(*) FROM camiones3 WHERE kilometros > 600000;
 count 
-------
     0
(1 row)
```

```
SELECT * FROM pg_statio_user_tables WHERE relname='camiones3_p0' or relname='camiones3_p1'
or relname='camiones3_p2' or relname='camiones3_p3' or relname='camiones3_p4' or relname='camiones3_p5' 
or relname='camiones3_p6' or relname='camiones3_p7' or relname='camiones3_p8' or relname='camiones3_p9'; 

 relid | schemaname |   relname    | heap_blks_read | heap_blks_hit | idx_blks_read | idx_blks_hit | toast_blks_read | toast_blks_hit | tidx_blks_read | tidx_blks_hit 
-------+------------+--------------+----------------+---------------+---------------+--------------+-----------------+----------------+----------------+---------------
 17378 | public     | camiones3_p0 |              0 |             0 |               |              |                 |                |                |              
 17382 | public     | camiones3_p1 |              0 |             0 |               |              |                 |                |                |              
 17386 | public     | camiones3_p2 |              0 |             0 |               |              |                 |                |                |              
 17390 | public     | camiones3_p3 |              0 |             0 |               |              |                 |                |                |              
 17394 | public     | camiones3_p4 |              0 |             0 |               |              |                 |                |                |              
 17398 | public     | camiones3_p5 |              0 |             0 |               |              |                 |                |                |              
 17402 | public     | camiones3_p6 |              0 |             0 |               |              |                 |                |                |              
 17406 | public     | camiones3_p7 |              0 |             0 |               |              |                 |                |                |              
 17410 | public     | camiones3_p8 |              0 |             0 |               |              |                 |                |                |              
 17414 | public     | camiones3_p9 |              0 |             0 |               |              |                 |                |                |              
(10 rows)
```
No hay resultados, curiosamente, no necesita buscar para devolver la falta de valores. Es probable, como en indice ya esta generado con margenes, utilice esta información para devolvernos la consulta.


----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------


2. Mostrar los camiones que tienen entre 30000 y 80000 km.

```
SELECT * FROM pg_stat_reset();
```

```
SELECT * FROM camiones3 WHERE kilometros BETWEEN 30000 AND 80000;
```

```
pl1=# SELECT * FROM pg_statio_user_tables WHERE relname='camiones3_p0' or relname='camiones3_p1'
or relname='camiones3_p2' or relname='camiones3_p3' or relname='camiones3_p4' or relname='camiones3_p5' 
or relname='camiones3_p6' or relname='camiones3_p7' or relname='camiones3_p8' or relname='camiones3_p9'; 
 relid | schemaname |   relname    | heap_blks_read | heap_blks_hit | idx_blks_read | idx_blks_hit | toast_blks_read | toast_blks_hit | tidx_blks_read | tidx_blks_hit 
-------+------------+--------------+----------------+---------------+---------------+--------------+-----------------+----------------+----------------+---------------
 17378 | public     | camiones3_p0 |          16308 |          1804 |               |              |                 |                |                |              
 17382 | public     | camiones3_p1 |          16195 |          1917 |               |              |                 |                |                |              
 17386 | public     | camiones3_p2 |              0 |             0 |               |              |                 |                |                |              
 17390 | public     | camiones3_p3 |              0 |             0 |               |              |                 |                |                |              
 17394 | public     | camiones3_p4 |              0 |             0 |               |              |                 |                |                |              
 17398 | public     | camiones3_p5 |              0 |             0 |               |              |                 |                |                |              
 17402 | public     | camiones3_p6 |              0 |             0 |               |              |                 |                |                |              
 17406 | public     | camiones3_p7 |              0 |             0 |               |              |                 |                |                |              
 17410 | public     | camiones3_p8 |              0 |             0 |               |              |                 |                |                |              
 17414 | public     | camiones3_p9 |              0 |             0 |               |              |                 |                |                |              
(10 rows)
```
Podemos comprobar como hace uso de las particiones, recuperando de cada partición los datos que corresponden a dicha partición. En esta busqueda, el acceso ha sido ha disco, mayoritariamente, 16308 y 16195 bloques para cada rango, y parte en disco que tenemos cacheado. 
Como no hay indices, no obtenemos bloques de indice.



----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------


3.Mostrar los camiones con 400000 km.
```
SELECT * FROM pg_stat_reset();
```

```
SELECT * FROM camiones3 WHERE kilometros = 400000;
```

```
SELECT * FROM pg_statio_user_tables WHERE relname='camiones3_p0' or relname='camiones3_p1'
or relname='camiones3_p2' or relname='camiones3_p3' or relname='camiones3_p4' or relname='camiones3_p5' 
or relname='camiones3_p6' or relname='camiones3_p7' or relname='camiones3_p8' or relname='camiones3_p9'; 

 relid | schemaname |   relname    | heap_blks_read | heap_blks_hit | idx_blks_read | idx_blks_hit | toast_blks_read | toast_blks_hit | tidx_blks_read | tidx_blks_hit 
-------+------------+--------------+----------------+---------------+---------------+--------------+-----------------+----------------+----------------+---------------
 17378 | public     | camiones3_p0 |              0 |             0 |               |              |                 |                |                |              
 17382 | public     | camiones3_p1 |              0 |             0 |               |              |                 |                |                |              
 17386 | public     | camiones3_p2 |              0 |             0 |               |              |                 |                |                |              
 17390 | public     | camiones3_p3 |              0 |             0 |               |              |                 |                |                |              
 17394 | public     | camiones3_p4 |              0 |             0 |               |              |                 |                |                |              
 17398 | public     | camiones3_p5 |              0 |             0 |               |              |                 |                |                |              
 17402 | public     | camiones3_p6 |              0 |             0 |               |              |                 |                |                |              
 17406 | public     | camiones3_p7 |              0 |             0 |               |              |                 |                |                |              
 17410 | public     | camiones3_p8 |          16590 |          1522 |               |              |                 |                |                |              
 17414 | public     | camiones3_p9 |              0 |             0 |               |              |                 |                |                |              
(10 rows)
```
Utiliza el rango que le corresponde, leyendo 16590 bloques de datos en disco, 1522 bloques de datos en cache.

16590+1522=18112 bloque


3A.PRIMA para comparar rangos Mostrar los camiones con 400000 km.


```
SELECT * FROM pg_stat_reset();
```

```
SELECT * FROM camiones3 WHERE kilometros >= 400000;
```

pl1=# SELECT * FROM pg_statio_user_tables WHERE relname='camiones3_p0' or relname='camiones3_p1'
or relname='camiones3_p2' or relname='camiones3_p3' or relname='camiones3_p4' or relname='camiones3_p5' 
or relname='camiones3_p6' or relname='camiones3_p7' or relname='camiones3_p8' or relname='camiones3_p9'; 
 relid | schemaname |   relname    | heap_blks_read | heap_blks_hit | idx_blks_read | idx_blks_hit | toast_blks_read | toast_blks_hit | tidx_blks_read | tidx_blks_hit 
-------+------------+--------------+----------------+---------------+---------------+--------------+-----------------+----------------+----------------+---------------
 17378 | public     | camiones3_p0 |              0 |             0 |               |              |                 |                |                |              
 17382 | public     | camiones3_p1 |              0 |             0 |               |              |                 |                |                |              
 17386 | public     | camiones3_p2 |              0 |             0 |               |              |                 |                |                |              
 17390 | public     | camiones3_p3 |              0 |             0 |               |              |                 |                |                |              
 17394 | public     | camiones3_p4 |              0 |             0 |               |              |                 |                |                |              
 17398 | public     | camiones3_p5 |              0 |             0 |               |              |                 |                |                |              
 17402 | public     | camiones3_p6 |              0 |             0 |               |              |                 |                |                |              
 17406 | public     | camiones3_p7 |              0 |             0 |               |              |                 |                |                |              
 17410 | public     | camiones3_p8 |          16622 |          1490 |               |              |                 |                |                |              
 17414 | public     | camiones3_p9 |          16566 |          1546 |               |              |                 |                |                |              
(10 rows)

Al igual que nos ocurre antes, vemos como accede a la partición definida:
  16622 bloques de disco para datos y 1490 bloque de cache para datos.
  16566 bloques de disco para datos y 1546 bloque de cache para datos.



3B.PRIMA para comparar valor concreto Mostrar los camiones con 400000 km en camiones.


pl1=# SELECT * FROM pg_statio_user_tables WHERE relname='camiones' ;
 relid | schemaname | relname  | heap_blks_read | heap_blks_hit | idx_blks_read | idx_blks_hit | toast_blks_read | toast_blks_hit | tidx_blks_read | tidx_blks_hit 
-------+------------+----------+----------------+---------------+---------------+--------------+-----------------+----------------+----------------+---------------
 17060 | public     | camiones |             41 |             0 |             2 |            0 |                 |                |                |              
(1 row)


pl1=# SELECT * FROM pg_stat_user_indexes;
 relid | indexrelid | schemaname | relname  |      indexrelname       | idx_scan |         last_idx_scan         | idx_tup_read | idx_tup_fetch 
-------+------------+------------+----------+-------------------------+----------+-------------------------------+--------------+---------------
 17060 |      17064 | public     | camiones | camiones_pkey           |        0 |                               |            0 |             0
 17060 |      17066 | public     | camiones | camiones_id_camion_key  |        0 |                               |            0 |             0
 17060 |      17170 | public     | camiones | idx_kilometros1         |        0 |                               |            0 |             0
 17060 |      17171 | public     | camiones | indice_hash             |        0 |                               |            0 |             0
 17060 |      17172 | public     | camiones | idx_matricula_b         |        0 |                               |            0 |             0
 17060 |      17174 | public     | camiones | indice_hash_matricula   |        0 |                               |            0 |             0
 17060 |      17178 | public     | camiones | indice_empresa_km_btree |        0 |                               |            0 |             0
 17060 |      17179 | public     | camiones | indice_empresa_hash     |        0 |                               |            0 |             0
 17060 |      17180 | public     | camiones | indice_km_hash          |        1 | 2024-03-03 01:19:34.954683+00 |           41 |             0
(9 rows)

Ha usado 41 bloque de disco de disco de datos y 2 bloques de disco de indice.
Coste de 41+2=43 bloques


----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------



Cuestión 25. A la vista de los resultados obtenidos de este apartado, comentar las
conclusiones que se pueden obtener del acceso de PostgreSQL a los datos almacenados
en disco.


VALOR CONCRETO:
Comparemos la busqueda kilometros = 400000;
  SELECT * FROM camiones3WHERE kilometros = 400000;
  SELECT * FROM camiones3 WHERE kilometros = 400000;
  Sobre camiones3 ha utilizado el particionado en disco COSTE TOTAL=16590+1522=18112 bloque
  Sobre camiones ha utilizado Coste de 41+2=43 bloques


RANGOS:
Comparemos la busqueda kilometros >= 400000;
  SELECT COUNT(*) FROM camiones WHERE kilometros > 400000;
  SELECT * FROM camiones3 WHERE kilometros >= 400000;
  Sobre camiones ha utilizado el indice Btree COSTE TOTAL= 597542 + 3539=601081 bloques
  Sobre camiones3 ha utilizado el particionado en disco COSTE TOTAL= 16622 + 1490 + 16566 + 1546 =  34883bloques

Para rangos parece mucho mas interesante usar rangos, pero cuando buscamos sobre un valor concreto, el uso de indice mejora muchismo el coste.