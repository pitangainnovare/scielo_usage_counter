# SciELO Usage Counter


## Installation

__Create a virtual environment and install the application dependencies__
```shell
# Create a virtual environment
virtualenv -p python3 .venv

# Access the virtual environment
source .venv/bin/activated

# Please ensure that the MySQL developer library is installed on your system. For Ubuntu-based distributions, you can install it using the following command
sudo apt install libmysql++-dev

# Install dependencies
pip install -r requirements.txt

# Install the package
python setup.py install
```

__Run tests__
```
python -m unittest discover
```


## Usage
_Get the official COUNTER list of robots_
```bash
usage: dl-robots [-h] [-u URL] --path_output PATH_OUTPUT

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL da lista de robôs
  --path_output PATH_OUTPUT
                        Arquivo de saída
```

_Get the Maxming GeoIP Map_
```bash
usage: dl-geomap [-h] [--year YEAR] [--month MONTH] [--url URL] --path_output PATH_OUTPUT

options:
  -h, --help            show this help message and exit
  --year YEAR           Ano do mapa de geolocalização (yyyy)
  --month MONTH         Mês do mapa de geolocalização (mm)
  --url URL             URL do mapa em formato mmdb.gz
  --path_output PATH_OUTPUT
                        Caminho do arquivo de mapa de geolocalizações
```

_Parse log file_
```
usage: parse-log [-h] -m MMDB -r ROBOTS [-o OUTPUT_DIRECTORY] [-f LOGFILE]

options:
  -h, --help            show this help message and exit
  -m MMDB, --mmdb MMDB  Arquivo de mapa de geolocalizações
  -r ROBOTS, --robots ROBOTS
                        Arquivo de robôs
  -o OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        Diretório de saída
  -f LOGFILE, --logfile LOGFILE
                        Caminho de arquivo de log de acesso
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
