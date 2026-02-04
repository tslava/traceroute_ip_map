# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Traceroute IP Map — a Python CLI tool that traces the network route to a domain, geolocates each hop using MaxMind GeoLite2, and generates an interactive HTML map (Folium/Leaflet).

## Commands

```bash
# Install dependencies
poetry install

# Run the tool
python main.py <domain_or_ip>
python main.py example.com -o custom_output.html
python main.py example.com --db /path/to/GeoLite2-City.mmdb
```

There is no test suite, linter configuration, or CI pipeline.

## Architecture

Single-file application (`main.py`) with these functions:

- `get_ip_list(url)` — runs system `traceroute -n` via subprocess, parses and validates IPv4 addresses, filters all RFC 1918 private IPs via `ipaddress` module, stops after 5 consecutive unreachable hops, has a 120s timeout
- `geolocate_ip(reader, ip_address)` — looks up lat/lng via `geoip2` database reader
- `plot_route(reader, ip_addresses)` — builds a Folium map with markers and a polyline connecting the route
- `is_private_ip(ip_str)` / `is_valid_ipv4(ip_str)` — IP validation helpers using `ipaddress` module
- `main(url, output_path, db_path)` — orchestrates the pipeline and saves the result as a self-contained HTML file

CLI uses `argparse` with a positional domain argument, optional `-o/--output` flag, and `--db` for the GeoLite2 database path.

## Dependencies

- **Poetry** for dependency management (Python ^3.10)
- **geoip2** — official MaxMind client for IP geolocation (requires a GeoLite2-City.mmdb file)
- **folium** — interactive map generation
- System `traceroute` command must be available (pre-installed on macOS; `apt install traceroute` on Linux)

## Key Constraints

- Platform-dependent: uses `traceroute` (not `tracert`); no Windows support without WSL
- Requires a GeoLite2-City.mmdb database file downloaded from MaxMind (free account required)
- Generated `*.html` output files are git-ignored
