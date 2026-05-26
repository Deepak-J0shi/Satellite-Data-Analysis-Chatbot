import ee
import httpx

# Fallback list — agar Nominatim fail ho
FALLBACK_REGIONS = {
    "uttarakhand"      : [77.5, 28.7, 81.1, 31.5],
    "delhi"            : [76.8, 28.4, 77.4, 28.9],
    "amazon"           : [-74.0, -10.0, -49.0, 5.0],
    "california"       : [-124.5, 32.5, -114.1, 42.0],
    "rajasthan"        : [69.5, 23.0, 78.3, 30.2],
    "kerala"           : [74.8, 8.1, 77.4, 12.8],
    "assam"            : [89.7, 24.1, 96.0, 28.2],
    "punjab"           : [73.8, 29.5, 76.9, 32.6],
    "himachal pradesh" : [75.5, 30.4, 79.0, 33.2],
    "west bengal"      : [85.8, 21.5, 89.9, 27.2],
}

# Area limits (km²)
MAX_AREA_PREVIEW = 500_000   # tile preview ke liye
MAX_AREA_EXPORT  = 2_000_000 # full export ke liye

def fetch_from_nominatim(name: str) -> list | None:
    """
    Nominatim (OpenStreetMap) se bounding box fetch karo.
    Returns [west, south, east, north] ya None if not found.
    """
    try:
        url    = "https://nominatim.openstreetmap.org/search"
        params = {
            "q"              : name,
            "format"         : "json",
            "limit"          : 1,
            "polygon_geojson": 0,
        }
        headers = {
            # Nominatim requires a User-Agent
            "User-Agent": "SatelliteChatbot/1.0 (personal learning project)"
        }

        response = httpx.get(url, params=params, headers=headers, timeout=10)
        data     = response.json()

        if not data:
            print(f"      Nominatim: '{name}' nahi mila")
            return None

        result = data[0]
        bbox   = result["boundingbox"]

        # Nominatim format: [south, north, west, east]
        # GEE format:       [west, south, east, north]
        south, north, west, east = (
            float(bbox[0]),
            float(bbox[1]),
            float(bbox[2]),
            float(bbox[3]),
        )

        print(f"      Nominatim found: {result['display_name']}")
        print(f"      BBox: [{west:.2f}, {south:.2f}, {east:.2f}, {north:.2f}]")

        return [west, south, east, north]

    except Exception as e:
        print(f"      Nominatim error: {e}")
        return None


def calculate_area_km2(bbox: list) -> float:
    """Rough area calculation in km²."""
    west, south, east, north = bbox
    width_km  = abs(east - west)  * 111  # 1 degree ≈ 111 km
    height_km = abs(north - south) * 111
    return width_km * height_km


def resolve_region(name: str) -> ee.Geometry:
    """
    Region name → GEE Geometry
    Flow: Nominatim → Fallback list → Error
    """
    key = name.lower().strip()
    print(f"      Resolving region: '{name}'")

    # Step 1 — Nominatim se try karo
    bbox = fetch_from_nominatim(name)

    # Step 2 — Nominatim fail hua toh fallback list
    if not bbox:
        print(f"      Trying fallback list...")
        for known_key, known_bbox in FALLBACK_REGIONS.items():
            if key in known_key or known_key in key:
                print(f"      Fallback match: '{known_key}'")
                bbox = known_bbox
                break

    # Step 3 — Dono fail
    if not bbox:
        raise ValueError(
            f"Region '{name}' resolve nahi hua.\n"
            f"Nominatim pe nahi mila aur fallback list mein bhi nahi.\n"
            f"Try karo: city + country, e.g. 'Shimla, India'"
        )

    # Step 4 — Area check
    area = calculate_area_km2(bbox)
    print(f"      Area: {area:,.0f} km²")

    if area > MAX_AREA_PREVIEW:
        print(f"      Warning: Large area ({area:,.0f} km²) — preview quality reduced")

    return ee.Geometry.Rectangle(bbox)

