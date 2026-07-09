import json


def geolocate_ip(ip_address: str) -> str:
    """Locates an IP address to identify its geographical location, ISP, and metadata."""
    if not ip_address:
        return "[ip_geolocator] Error: Parameter 'ip_address' is required."

    ip_clean = ip_address.strip()

    # Static mock registration for standard demonstration vectors
    ip_database = {
        "8.8.8.8": {
            "country": "United States",
            "country_code": "US",
            "region": "California",
            "city": "Mountain View",
            "zip_code": "94043",
            "latitude": 37.4223,
            "longitude": -122.0847,
            "isp": "Google LLC",
            "asn": "AS15169",
        },
        "1.1.1.1": {
            "country": "Australia",
            "country_code": "AU",
            "region": "Queensland",
            "city": "Research",
            "zip_code": "4000",
            "latitude": -27.4698,
            "longitude": 153.0251,
            "isp": "Cloudflare, Inc.",
            "asn": "AS13335",
        },
    }

    if ip_clean in ip_database:
        geo_data = ip_database[ip_clean]
    else:
        # Fallback profile generating a mock response tracking block for unknown IPs
        geo_data = {
            "country": "Unknown / Private Network",
            "country_code": "XX",
            "region": "Unknown Region",
            "city": "Unknown City",
            "zip_code": "00000",
            "latitude": 0.0,
            "longitude": 0.0,
            "isp": "Local Loopback / Unassigned Provider",
            "asn": "AS00000",
        }

    report = {
        "query_ip": ip_clean,
        "geographical_location": {
            "country": geo_data["country"],
            "country_code": geo_data["country_code"],
            "region": geo_data["region"],
            "city": geo_data["city"],
            "postal_code": geo_data["zip_code"],
            "coordinates": {"lat": geo_data["latitude"], "lon": geo_data["longitude"]},
        },
        "network_provider_details": {
            "isp_name": geo_data["isp"],
            "autonomous_system_number": geo_data["asn"],
        },
    }

    return f"[ip_geolocator] Geolocation resolution complete: {json.dumps(report, ensure_ascii=False)}"


SKILLS = [
    {
        "name": "ip_geolocator",
        "description": "Locates IP addresses to identify their geographical location, ISP provider, and network routing markers.",
        "trigger_phrases": [
            "geolocate ip",
            "locate ip address",
            "find ip location",
            "lookup ip details",
            "track ip isp",
            "ip geolocator",
            "where is this ip from",
        ],
        "func": geolocate_ip,
    },
]