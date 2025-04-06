# OSM2SUMO - Streamline SUMO Map Creation from coordinates

OSM2SUMO Converter is a Python-based tool that automates downloading OpenStreetMap (OSM) data for a specified geographic area using a list of coordinates and converts it into a SUMO network. This is especially useful for traffic simulation projects where you must generate a SUMO network from real-world map data.

## Features

- **Dynamic Bounding Box:** Automatically calculates the bounding box from a list of coordinates and adds a configurable buffer.
- **Flexible Input:** Reads coordinates from a text file (one coordinate per line, with latitude and longitude separated by a comma).
- **Overpass API Integration:** Downloads OSM data on the fly for the computed area.
- **SUMO Network Conversion:** Uses NETCONVERT (part of the SUMO suite) to generate a SUMO network file.
- **Customizable Buffer:** Set a custom buffer radius via an optional command-line argument.

## Prerequisites

- **Python 3.x:** Make sure you have Python installed.
- **NETCONVERT:** This tool is part of the SUMO suite. [Download SUMO](https://www.eclipse.org/sumo/) and ensure that `netconvert` is in your system PATH.
- **Python Libraries:**
  - `requests`
  - `argparse`

Install the required Python libraries with:

```bash
pip install requests
```

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Harshit2k1/OSM2SUMO.git
   cd OSM2SUMO
   ```

2. **Verify NETCONVERT:**

   Ensure that `netconvert` is installed and available in your system PATH by running:

   ```bash
   netconvert --help
   ```

## Usage

1. **Prepare Your Coordinates File:**

   Create a text file (e.g., `input.txt`) with each line containing a latitude and longitude separated by a comma. For example:

   ```
   43.74179273,-79.22516266622
   43.59438489,-79.53397515
   ```

2. **Run the Script:**

   The script accepts two arguments:
   
   - `-f` or `--file`: The path to the text file containing the coordinates.
   - `-r` or `--radius`: (Optional) The buffer radius in kilometers. Defaults to 5 km if not provided.

   For example, to run the script with a default 5 km buffer:

   ```bash
   python main.py -f input.txt
   ```

   Or with a custom 10 km buffer:

   ```bash
   python main.py -f input.txt -r 10
   ```

3. **Output:**

   The script will:
   - Parse the coordinates from the file.
   - Calculate a bounding box with the specified buffer.
   - Download the corresponding OSM data using the Overpass API.
   - Convert the OSM data to a SUMO network file named `sumo_network.net.xml`.

## Code Overview

- **main.py:**  
  Contains the main script which:
  - Parses the input file for coordinates.
  - Downloads OSM data using the Overpass API.
  - Converts the OSM data to a SUMO network using NETCONVERT.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

## License

This project is licensed under the Apache License. Feel free to modify and improve it!

## Acknowledgements

- [OpenStreetMap](https://www.openstreetmap.org/) for providing the map data.
- [SUMO](https://www.eclipse.org/sumo/) for the simulation tools.
```

This README outlines the purpose, usage, and customization of the program along with clear instructions for both installation and execution. Feel free to modify any sections to best suit your project's needs.
