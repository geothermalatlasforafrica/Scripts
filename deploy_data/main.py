import os
from os import path
from pathlib import Path

import pandas as pd
import validators
from typing import List

from scripts.deploy_data import secrets
from scripts.deploy_data.api_service import ApiService
from scripts.deploy_data.geoserver_service import GeoserverService
from scripts.deploy_data.layer import Layer


def run() -> None:
    """
    Deploy the data to the API and GeoServer.
    This function requires a file to exist in the same directory as this script named "secrets.py"
    The file should contain the following lines:
    geoserver_username = "my_secret_username"
    geoserver_password = "my_secret_password"
    api_token = "my_secret_api_token"
    """
    geoserver_url = os.getenv("GEOSERVER_URL")  # This environment variable is set in the Dockerfile(.prod)
    api_url = os.getenv("API_URL")  # This environment variable is set in the Dockerfile(.prod)
    data_path = path.join("..", "..", "data", "gaa")  # The data folder is located in the root of the repository
    metadata_filename = "gaa_metadata_restructured.xlsx"  # geoelec_metadata.xlsx or gaa_metadata.xlsx
    workspace = "gaa-dev"  # geoelec-dev or gaa-dev
    layers = get_layers(metadata_filename, workspace)

    validate_all_files_exist(data_path, layers, metadata_filename)

    # Setup connection to the API and perform database migrations
    api_service = ApiService(api_url, secrets.api_token)
    api_service.check_status()
    api_service.migrate_database()

    workspace_layers = [layer for layer in layers if layer.workspace == workspace]
    raster_layers = [layer for layer in workspace_layers if layer.type.lower() == "raster"]
    vector_layers = [layer for layer in workspace_layers if layer.type.lower() == "vector"]

    # Update layer metadata in database
    api_service.delete_layers(workspace)  # First, remove all layers of the workspace
    api_service.add_layers(workspace_layers)  # Then, add the layers of the workspace

    # Updating layers in GeoServer
    geoserver_service = GeoserverService(geoserver_url, secrets.geoserver_username, secrets.geoserver_password)
    geoserver_service.check_status()

    geoserver_service.create_workspace(workspace)
    geoserver_service.create_raster_layers(data_path, raster_layers, workspace)
    geoserver_service.create_vector_layers(data_path, vector_layers, workspace)


def validate_all_files_exist(data_path: str, layers: List[Layer], metadata_filename: str):
    """
    Check if all files in the metadata file exist in the data_path.
    If not, throw an exception.
    """
    files_in_path = [path.basename(filename) for filename in os.listdir(data_path)]
    for layer in layers:
        if not path.isfile(path.join(data_path, layer.filename)) or layer.filename not in files_in_path:
            raise FileNotFoundError(f"{metadata_filename} contains the file '{layer.filename}' that cannot be "
                                    f"found in {data_path}.")


def get_layers(metadata_filename: str, workspace: str) -> List[Layer]:
    """Get a list of layer objects by parsing the metadata Excel file."""
    if not metadata_filename.endswith(".xlsx"):
        raise ValueError(f"File type {metadata_filename} not supported. Use .xlsx instead.")

    return parse_metadata_excel(metadata_filename, workspace)


def parse_metadata_excel(metadata_filename: str, workspace: str) -> List[Layer]:
    """Parse the metadata Excel file and return a list of layer objects."""
    layers = []
    df = pd.read_excel(metadata_filename, engine="openpyxl")
    df.fillna("", inplace=True)  # Replace all nan values with an empty string

    if not df["filename"].is_unique:
        raise ValueError("Layer filenames are not unique")

    for index, row in df.iterrows():
        # Validate
        source_url = row["source"]
        if not validators.url(source_url) and source_url != "":
            raise ValueError(f"{row['source']} is not a valid url")

        filename: str = row["filename"]
        name = Path(filename).stem
        layer = Layer(name=name,
                      full_name=row["full_name"],
                      filename=row["filename"],
                      type=row["type"],
                      url=row["source"],
                      unit=row["unit"],
                      workspace=workspace,
                      layer_group=row["layer_group"],
                      parent_group=row["parent_group"],
                      description=row["description"],
                      keywords=row["keywords"],
                      date=row["date"],
                      restricted=row["restricted"],
                      resolution=row["resolution"]
                      )
        layers.append(layer)
    return layers


if __name__ == "__main__":
    run()
