import os
import requests
import subprocess
import math
import argparse

def download_osm_data(coordinates, radius_km=5):
    """
    Download OSM data for an area containing all coordinates plus a buffer.

    Args:
        coordinates: List of tuples (lat, lon)
        radius_km: Buffer distance in kilometers around the area

    Returns:
        Path to the downloaded OSM file.
    """
    # Find the min/max coordinates to create a bounding box
    min_lat = min(lat for lat, _ in coordinates)
    max_lat = max(lat for lat, _ in coordinates)
    min_lon = min(lon for _, lon in coordinates)
    max_lon = max(lon for _, lon in coordinates)
    
    # Add the buffer to the bounding box
    # 1 degree latitude ≈ 111 km
    lat_offset = radius_km / 111.0
    
    # 1 degree longitude varies with latitude, use average latitude for calculation
    avg_lat = (min_lat + max_lat) / 2
    lon_offset = radius_km / (111.0 * math.cos(math.radians(avg_lat)))
    
    # Expand the bounding box
    min_lat -= lat_offset
    max_lat += lat_offset
    min_lon -= lon_offset
    max_lon += lon_offset
    
    # Construct Overpass API query
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:xml];
    (
      way["highway"]({min_lat},{min_lon},{max_lat},{max_lon});
      relation["highway"]({min_lat},{min_lon},{max_lat},{max_lon});
    );
    (._;>;);
    out body;
    """
    
    # Download data
    print(f"Downloading area with bounds: {min_lat},{min_lon},{max_lat},{max_lon}")
    response = requests.post(overpass_url, data=overpass_query)
    
    # Save to file
    osm_file = "map_area.osm"
    with open(osm_file, "w", encoding="utf-8") as f:
        f.write(response.text)
    
    return osm_file

def convert_to_sumo_network(osm_file):
    """
    Convert OSM data to a SUMO network.

    Args:
        osm_file: Path to the OSM file.

    Returns:
        Path to the generated SUMO network file.
    """
    net_file = "sumo_network.net.xml"
    
    # Run NETCONVERT to create SUMO network
    subprocess.run([
        "netconvert",
        "--osm-files", osm_file,
        "--output", net_file,
        "--geometry.remove",
        "--roundabouts.guess",
        "--ramps.guess",
        "--junctions.join",
        "--tls.guess-signals",
        "--tls.discard-simple",
        "--tls.join"
    ])
    
    return net_file

def main():
    parser = argparse.ArgumentParser(
        description="Download OSM data from a list of coordinates and convert it to a SUMO network."
    )
    parser.add_argument(
        "-f", "--file", required=True,
        help="Path to the text file with coordinates (lat,lon per line)"
    )
    parser.add_argument(
        "-r", "--radius", type=float, default=5.0,
        help="Buffer radius in kilometers (default: 5 km)"
    )
    args = parser.parse_args()

    input_file = args.file
    buffer_radius = args.radius
    intersection_coordinates = []

    # Read coordinates from the provided file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) != 2:
                    print(f"Skipping invalid line: {line}")
                    continue
                try:
                    lat = float(parts[0].strip())
                    lon = float(parts[1].strip())
                    intersection_coordinates.append((lat, lon))
                except ValueError:
                    print(f"Skipping line with invalid coordinates: {line}")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return

    if not intersection_coordinates:
        print("No valid coordinates found in the file.")
        return

    print("Downloading OSM data...")
    osm_file = download_osm_data(intersection_coordinates, radius_km=buffer_radius)

    print("Converting to SUMO network...")
    net_file = convert_to_sumo_network(osm_file)

    print(f"SUMO network created successfully: {net_file}")

if __name__ == "__main__":
    main()
