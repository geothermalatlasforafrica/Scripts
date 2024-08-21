import os
import xml.etree.ElementTree as ET
from os import path

from geo.Geoserver import Geoserver
from typing import List

from scripts.deploy_data.layer import Layer


class GeoserverService:
    def __init__(self, geoserver_url: str, username: str, password: str):
        self.geo = Geoserver(geoserver_url, username=username, password=password)

    def check_status(self) -> None:
        self.geo.get_status()

    def create_raster_layers(self, data_path: str, raster_layers: List[Layer], workspace_name: str):
        print("Creating raster layers")
        for layer in raster_layers:
            layer_name = layer.name
            print(f"Creating raster layer {layer_name} with filename {layer.filename} in group {layer.layer_group}")

            layer_data_path = path.join(data_path, layer.filename)

            style_name = f"{layer_name}_style"
            style_filename = os.path.splitext(layer.filename)[0] + '.sld'
            layer_style_path = path.join(data_path, style_filename)
            sld_version = self.extract_sld_version(layer_style_path)

            # TODO: Clean up this repetition
            max_tries = 3
            tries = 0
            success = False
            while tries < max_tries and not success:
                try:
                    tries += 1
                    print(f"Creating coverage store, try {tries}")
                    self.geo.create_coveragestore(layer_name=layer_name, path=layer_data_path, workspace=workspace_name)
                    success = True
                    print(f"Successfully created coverage store")
                except:
                    pass

            tries = 0
            success = False
            while tries < max_tries and not success:
                try:
                    tries += 1
                    print(f"Uploading style, try {tries}")
                    self.geo.upload_style(path=layer_style_path, name=style_name, workspace=workspace_name,
                                          sld_version=sld_version)
                    success = True
                    print(f"Successfully uploaded style")
                except:
                    pass

            tries = 0
            success = False
            while tries < max_tries and not success:
                try:
                    tries += 1
                    print(f"Publishing style, try {tries}")
                    self.geo.publish_style(layer_name=layer_name, style_name=style_name, workspace=workspace_name)
                    success = True
                    print(f"Successfully published style")
                except:
                    pass

    def create_vector_layers(self, data_path: str, vector_layers: List[Layer], workspace_name: str):
        print("Creating vector layers")

        for layer in vector_layers:
            layer_name = layer.name
            print(f"Creating vector layer {layer_name}")

            layer_data_path = path.join(data_path, layer.filename)

            style_name = f"{layer_name}_style"
            style_filename = os.path.splitext(layer.filename)[0] + '.sld'
            layer_style_path = path.join(data_path, style_filename)

            sld_version = self.extract_sld_version(layer_style_path)

            # TODO: Clean up this repetition
            max_tries = 3
            tries = 0
            success = False
            while tries < max_tries and not success:
                try:
                    tries += 1
                    print(f"Creating shp datastore, try {tries}")
                    self.geo.create_shp_datastore(path=layer_data_path, store_name=layer_name, workspace=workspace_name)
                    success = True
                    print(f"Successfully created shp datastore")
                except:
                    pass

            tries = 0
            success = False
            while tries < max_tries and not success:
                try:
                    tries += 1
                    print(f"Uploading style, try {tries}")
                    self.geo.upload_style(path=layer_style_path, name=style_name, workspace=workspace_name, sld_version=sld_version)
                    success = True
                    print(f"Successfully uploaded style")
                except:
                    pass

            tries = 0
            success = False
            while tries < max_tries and not success:
                try:
                    tries += 1
                    print(f"Publishing style, try {tries}")
                    self.geo.publish_style(layer_name=layer_name, style_name=style_name, workspace=workspace_name)
                    success = True
                    print(f"Successfully published style")
                except:
                    pass

    def extract_sld_version(self, layer_style_path):
        tree = ET.parse(layer_style_path)
        root = tree.getroot()
        sld_version = root.attrib["version"]
        return sld_version

    def create_workspace(self, workspace: str):
        print("Checking if workspace exists")
        if self.workspace_exists(workspace):
            print("Workspace exists. Deleting workspace")
            self.geo.delete_workspace(workspace)
        print("Creating workspace")
        self.geo.create_workspace(workspace)

    def workspace_exists(self, workspace: str) -> bool:
        print(f"Checking if workspace exists")
        try:
            self.geo.get_workspace(workspace)
            return True
        except Exception as e:
            if e.args[0].status == 404:
                print(f"Workspace '{workspace}' does not exist.")
                return False
            else:
                raise e
