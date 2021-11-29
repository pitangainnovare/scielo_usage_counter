# SciELO Usage Counter


## Installation

__Create a virtual environment and install the application dependencies__
```shell
# Create a virtual environment
virtualenv -p python3 .venv

# Access the virtual environment
source .venv/bin/activated

# Install dependencies
pip install -r requirements.txt

# Install the package
python setup.py install
```

__Run tests__
```
python setup.py test
```


## Usage
_Get the official COUNTER list of robots_
```bash
usage: get_robots [-h] [-u URL] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL da lista de robots
  -o OUTPUT, --output OUTPUT
                        Arquivo de saída
```

_Get the Maxming GeoIP Map_
```bash
usage: get_geomap [-h] [--year YEAR] [--month MONTH] [--url URL] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  --year YEAR           Ano do mapa de geolocalização (yyyy)
  --month MONTH         Mês do mapa de geolocalização (mm)
  --url URL             URL do mapa em formato mmdb.gz
  -o OUTPUT, --output OUTPUT
                        Arquivo do mapa de geolocalizações
```

_Parse a logfile_
```bash
usage: parse [-h] [-c COLLECTION] -f FILE [-o OUTPUT] -m MMDB -r ROBOTS

optional arguments:
  -h, --help            show this help message and exit
  -c COLLECTION, --collection COLLECTION
                        Acrônimo de coleção
  -f FILE, --file FILE  Arquivo de log de acesso
  -o OUTPUT, --output OUTPUT
                        Diretório de saída
  -m MMDB, --mmdb MMDB  Arquivo de mapa de geolocalizações
  -r ROBOTS, --robots ROBOTS
                        Arquivo de robôs
```

_Generate pretables_
```bash
usage: gen_pt [-h] -f FILE [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Arquivo de log pré-processado
  -o OUTPUT, --output OUTPUT
                        Diretório de saída
```

_Initialize database_
```bash
usage: init_db [-h] [-s STR_CONNECTION]

optional arguments:
  -h, --help            show this help message and exit
  -s STR_CONNECTION, --str_connection STR_CONNECTION
                        String de conexão com banco de dados (mysql://user:pass@host:port/database)
```

_Batch script parse logs_
```bash
SciELO Usage COUNTER - Batch script Parse Log
Please, inform:
   1. The directory of logs (parameter -d)
   2. The file MMDB (parameter -m)
   3. The file robots (parameter -r)

For example:

   scripts/batch_parse.sh -d /logs/apache -m /data/map.mmdb -r /data/counter-robots.txt
```

_Batch script generate pretable_
```bash
SciELO Usage COUNTER - Batch script Generate Pretable
Please, inform the directory of logs (parameter -d). For example: 

   scripts/batch_generate_pretable.sh -d /logs_preprocessed
```
## Libraries

__User agent - Robots__
- https://github.com/atmire/COUNTER-Robots
- https://raw.githubusercontent.com/atmire/COUNTER-Robots/master/COUNTER_Robots_list.json

__IP - Geolocation__
- https://github.com/maxmind/GeoIP2-python
- https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
- https://dev.maxmind.com/geoip/importing-databases/postgresql?lang=en

__Device detector__
- https://github.com/thinkwelltwd/device_detector
