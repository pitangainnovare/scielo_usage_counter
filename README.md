# SciELO Usage Counter

The SciELO Usage Counter processes SciELO access logs and generates COUNTER R5.1 compliant usage metrics. It supports Apache NCSA extended log format and BunnyCDN pipe-delimited format, geo-IP resolution, robot detection, and URL translation for articles, books, preprints, and datasets.

## Installation

```bash
git clone https://github.com/scieloorg/scielo_usage_counter.git
cd scielo_usage_counter
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Run tests:

```bash
pytest
```

## Environment Variables

### Download geomap (`dl-geomap`)

| Variable | Type | Default | Description |
|---|---|---|---|
| `GEOIP_LOGGING_LEVEL` | str | `INFO` | Logging level for the geomap downloader. |

### Download robots (`dl-robots`)

| Variable | Type | Default | Description |
|---|---|---|---|
| `COUNTER_ROBOTS_LOGGING_LEVEL` | str | `INFO` | Logging level for the robots downloader. |
| `COUNTER_ROBOTS_MAX_RETRIES` | int | `5` | Maximum retry attempts when fetching the robots list. |
| `COUNTER_ROBOTS_URL` | str | `https://...COUNTER_Robots_list.json` | Default URL for the COUNTER robots list. |
| `COUNTER_ROBOTS_URL_SLEEP_TIME` | int | `30` | Sleep time in seconds between retries. |

### Parse log (`parse-log`)

| Variable | Type | Default | Description |
|---|---|---|---|
| `PARSE_LOG_COLLECTION` | str | `scl` | Default collection acronym. |
| `PARSE_LOG_LOGGING_LEVEL` | str | `INFO` | Logging level for the log parser. |
| `OUTPUT_DIRECTORY` | str | `data` | Default output directory for processed logs. |

## Usage

### Command line

Three entry points are available:

#### `parse-log` — Parse a single access log file

```bash
parse-log -m <mmdb> -r <robots> -f <logfile> [-o <output_dir>] [--sample_size <pct>] [--validate]
```

| Argument | Default | Description |
|---|---|---|
| `-m`, `--mmdb` | *(required)* | Path to the MMDB geolocation database. |
| `-r`, `--robots` | *(required)* | Path to the robots pattern file. |
| `-f`, `--logfile` | — | Path to the access log file to parse. |
| `-o`, `--output_directory` | `data` | Output directory for processed files. |
| `--sample_size` | `0.05` | Fraction of lines to sample for validation (0–1). |
| `--validate` | off | Enable pre-validation with scielo-log-validator. |

**Example:**

```bash
parse-log -m data/map.mmdb -r data/counter-robots.txt \
  -f logs/2025-08-17_scielo-br.log.gz -o output --validate
```

#### `dl-geomap` — Download MaxMind GeoIP database

```bash
dl-geomap --path_output <path> [--year <yyyy>] [--month <mm>] [--url <url>] [--subset city|country]
```

| Argument | Default | Description |
|---|---|---|
| `--path_output` | *(required)* | Output file path for the MMDB database. |
| `--year` | last month | Year of the geolocation map (yyyy). |
| `--month` | last month | Month of the geolocation map (mm). |
| `--url` | — | Direct URL to a mmdb.gz file (overrides year/month). |
| `--subset` | `city` | Database precision: `city` or `country`. |

**Example:**

```bash
dl-geomap --year 2025 --month 04 --path_output data/map.mmdb
```

#### `dl-robots` — Download COUNTER robots list

```bash
dl-robots --path_output <path> [-u <url>]
```

| Argument | Default | Description |
|---|---|---|
| `--path_output` | *(required)* | Output file path for the robots list. |
| `-u`, `--url` | COUNTER-Robots list | URL of the robots JSON list. |

**Example:**

```bash
dl-robots --path_output data/counter-robots.txt
```

### Batch processing

Use the shell helper to parse multiple log files:

```bash
scripts/batch_parse.sh -m <mmdb> -r <robots> -o <output_dir> -f <file_list> [-v]
```

| Flag | Description |
|---|---|
| `-m` | MMDB geolocation file. |
| `-r` | Robots pattern file. |
| `-o` | Output directory. |
| `-f` | File containing a list of log file paths (one per line). |
| `-v` | Enable pre-validation (optional). |

**Example:**

```bash
scripts/batch_parse.sh -m data/map.mmdb -r data/counter-robots.txt \
  -o output -f logs_paths.txt -v
```

### Python library

```python
from scielo_usage_counter import log_handler

lp = log_handler.LogParser(
    mmdb_path='data/map.mmdb',
    robots_path='data/counter-robots.txt',
)

lp.logfile = 'logs/2025-08-17_scielo-br.log.gz'
lp.output = 'output/2025-08-17.tsv'
lp.stats.output = 'output/2025-08-17.summary.tsv'

for record in lp.parse():
    print(record)

lp.stats.save()
```

## Supported log formats

| Format | Description |
|---|---|
| NCSA Extended | Standard Apache combined log format with optional domain prefix and IP list fields. |
| BunnyCDN | Pipe-delimited format with Unix timestamps (7 or 10 digits), country codes, and request IDs. |

## Features

- **COUNTER R5.1 compliant** metrics with unique item and title-level counting
- **Geo-IP resolution** via MaxMind MMDB (city and country)
- **Robot detection** using COUNTER Robots list patterns
- **URL translation** for multiple SciELO platforms:
  - Classic site (`scielo.php`)
  - OPAC site (`/j/acronym/`)
  - OPAC Alpha (`article/`, `/pdf/`)
  - SciELO Books (`/id/<book>`)
  - SciELO Preprints
  - SciELO Data (Dataverse)
- **BunnyCDN** log format detection and parsing
- **Device detection** for client name and version extraction
- **Pre-validation** via scielo-log-validator before parsing

## Libraries

- [COUNTER-Robots](https://github.com/atmire/COUNTER-Robots) — robot user-agent patterns
- [GeoIP2-python](https://github.com/maxmind/GeoIP2-python) — IP geolocation
- [device_detector](https://github.com/thinkwelltwd/device_detector) — client name/version detection
