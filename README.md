# Traceroute IP Map

A Python tool that traces the network route to a domain and visualizes the path on an interactive map.

## Features

- Executes traceroute to discover IP addresses along the network path
- Geolocates each IP address using the MaxMind GeoLite2 database
- Generates an interactive HTML map with markers for each hop
- Connects route points with lines to visualize the network path

## Requirements

- Python 3.10+
- `traceroute` command available on your system
  - macOS: Pre-installed
  - Linux: `sudo apt install traceroute` or `sudo yum install traceroute`
  - Windows: Use `tracert` (requires code modification) or WSL
- GeoLite2 City database file (see below)

## GeoLite2 Database Setup

This tool requires a GeoLite2-City.mmdb database file for IP geolocation:

1. Create a free account at [MaxMind](https://www.maxmind.com/en/geolite2/signup)
2. Download the GeoLite2 City database (`.mmdb` format) from [the download page](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)
3. Place `GeoLite2-City.mmdb` in the project directory, or pass its path with `--db`

## Installation

```bash
# Clone the repository
git clone https://github.com/tslava/traceroute_ip_map.git
cd traceroute_ip_map

# Install dependencies using Poetry
poetry install
```

## Usage

```bash
# Basic usage
python main.py example.com

# Specify output file
python main.py example.com -o my_route_map.html

# Use a custom database path
python main.py example.com --db /path/to/GeoLite2-City.mmdb

# Show help
python main.py --help
```

The generated HTML file can be opened in any web browser to view the interactive map.

## How It Works

1. Runs `traceroute -n` to the specified domain
2. Extracts and validates IP addresses from each hop (filters private IPs)
3. Looks up geographic coordinates for each IP using GeoLite2
4. Creates a Folium map with markers and route lines
5. Saves the result as an interactive HTML file

## Limitations

- Some IPs might not geolocate accurately depending on database freshness
- Private/internal IP addresses (10.x.x.x, 172.16-31.x.x, 192.168.x.x) are filtered out
- Traceroute may be blocked by some network configurations or firewalls

## License

MIT License
