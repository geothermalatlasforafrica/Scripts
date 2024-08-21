Geothermal Atlas for Africa scripts

This repository contains a few handy scripts that aid in updating the website and the data.

- `deploy_data`: Uploads the data with metadata (found [here](https://github.com/geothermalatlasforafrica/Data)) to GeoServer
- `deploy_image_to_acr`: Deploy one or multiple images to Azure Container Registry
- `env_file_to_json`: Convert a `.env` file to `.json` to be used in Azure
- `export_qgis_data_to_directory`: Export a QGIS project's data and styling into a single directory
- `generate_maps_report_document`: Create a single docx report with metadata and map view screenshots by querying GeoServer
- `import_data_directory_into_qgis`: Import a data directory with `.tif` (rasters) and `.zip` (ShapeFiles) into QGIS
