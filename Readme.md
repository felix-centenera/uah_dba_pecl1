

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
Reference: https://dev.to/rainbowhat/postgresql-16-installation-on-ubuntu-2204-51ia
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
```


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
XXXXXXXXX LOG:  escuchando en la direcci√≥n IPv4 ¬´0.0.0.0¬ª, port 5432
XXXXXXXXX LOG:  escuchando en la direcci√≥n IPv6 ¬´::¬ª, port 5432
XXXXXXXXX LOG:  escuchando en el socket Unix ¬´/var/run/postgresql/.s.PGSQL.5432¬ª
XXXXXXXXX LOG:  el sistema de bases de datos fue apagado en 2024-02-02 20:19:24 UTC
XXXXXXXXX LOG:  el sistema de bases de datos est√° listo para aceptar conexiones
XXXXXXXXX [local]LOG:  sentencia: create database testlogging;


XXXXXXXXX [local]LOG:  sentencia: CREATE TABLE ejemplo (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100),
            edad INT,
            email VARCHAR(150)
        );
XXXXXXXXX LOG:  empezando checkpoint: time

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
                                           Tabla ¬´public.camiones¬ª
  Columna   |          Tipo          | Ordenamiento | Nulable  |                 Por omisi√≥n                 
------------+------------------------+--------------+----------+---------------------------------------------
 id_camion  | integer                |              | not null | nextval('camiones_id_camion_seq'::regclass)
 matricula  | character(8)           |              | not null | 
 empresa    | character varying(100) |              |          | 
 ndices:ros | integer                |              |          | 
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