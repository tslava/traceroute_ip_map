# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Traceroute IP Map — a Python CLI tool that traces the network route to a domain, geolocates each hop using ip-api.com, and generates an interactive HTML map (Folium/Leaflet).

## Commands

```bash
# Install dependencies
poetry install

# Run the tool
python main.py <domain_or_ip>
python main.py example.com -o custom_output.html
```

There is no test suite, linter configuration, or CI pipeline.

## Architecture

Single-file application (`main.py`) with these functions:

- `get_ip_list(url)` — runs system `traceroute -n` via subprocess, parses and validates IPv4 addresses, filters all RFC 1918 private IPs via `ipaddress` module, stops after 5 consecutive unreachable hops, has a 120s timeout
- `geolocate_ip(ip_address)` — looks up lat/lng via ip-api.com (free API, no key required)
- `plot_route(ip_addresses)` — builds a Folium map with markers and a polyline connecting the route
- `is_private_ip(ip_str)` / `is_valid_ipv4(ip_str)` — IP validation helpers using `ipaddress` module
- `main(url, output_path)` — orchestrates the pipeline and saves the result as a self-contained HTML file

CLI uses `argparse` with a positional domain argument and optional `-o/--output` flag.

## Dependencies

- **Poetry** for dependency management (Python ^3.10)
- **folium** — interactive map generation
- System `traceroute` command must be available (pre-installed on macOS; `apt install traceroute` on Linux)
- Requires internet access for ip-api.com geolocation

## Key Constraints

- Platform-dependent: uses `traceroute` (not `tracert`); no Windows support without WSL
- ip-api.com rate limit: 45 requests/minute (sufficient for typical traceroutes)
- Generated `*.html` output files are git-ignored
