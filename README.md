# Traceroute IP Map

A Python tool that traces the network route to a domain and visualizes the path on an interactive map.

## Features

- Executes traceroute to discover IP addresses along the network path
- Geolocates each IP address using ip-api.com (free, no signup required)
- Generates an interactive HTML map with markers for each hop
- Connects route points with lines to visualize the network path

## Requirements

- Python 3.10+
- `traceroute` command available on your system
  - macOS: Pre-installed
  - Linux: `sudo apt install traceroute` or `sudo yum install traceroute`
  - Windows: Use `tracert` (requires code modification) or WSL
- Internet connection (for IP geolocation API)

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

# Show help
python main.py --help
```

The generated HTML file can be opened in any web browser to view the interactive map.

## How It Works

1. Runs `traceroute -n` to the specified domain
2. Extracts and validates IP addresses from each hop (filters private IPs)
3. Looks up geographic coordinates for each IP using ip-api.com
4. Creates a Folium map with markers and route lines
5. Saves the result as an interactive HTML file

## Limitations

- Requires internet access for IP geolocation
- Private/internal IP addresses (10.x.x.x, 172.16-31.x.x, 192.168.x.x) are filtered out
- Traceroute may be blocked by some network configurations or firewalls
- ip-api.com has a rate limit of 45 requests per minute (sufficient for typical traceroutes)

## License

MIT License
