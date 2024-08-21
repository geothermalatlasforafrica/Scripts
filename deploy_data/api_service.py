import requests
from typing import List

from requests import Response

from scripts.deploy_data.layer import Layer


class ApiService:
    def __init__(self, api_url: str, api_token: str):
        self.api_url = api_url
        self.api_token = api_token

    def check_status(self):
        """
        Check if the API is running and connected to the database.
        A get request to the API's default route is made.
        That endpoint tries to get the date/time from the database.
        If it succeeds, the API is running and connected to the database.
        """
        try:
            r = requests.get(url=self.api_url)
            print(f"API is running, is connected to the database and returned {r}")
        except Exception:
            raise RuntimeError("API is not running or is not connected to the database properly")

    def migrate_database(self) -> None:
        """
        Migrate the database to the latest version.
        A "database migration" is a set of SQL scripts that are executed in order to update the database to the latest
        version. The migration scripts are location in the API folder under "migrations".
        """
        print("Migrating database...")
        try:
            headers = {'Authorization': self.api_token}
            response: Response = requests.post(self.api_url + "/database-migration", headers=headers)
            if response.status_code != 200:
                raise ApiException(f"The database migration was not successful. Server returned: {response.text}")
        except Exception as ex:
            print("An error occurred while migrating the database")
            raise ex

        print("Database migrated successfully")

    def delete_layers(self, workspace: str) -> None:
        """Delete all layers from the database that are in the given workspace."""
        print(f"Deleting all layers from workspace {workspace}")

        r = requests.delete(url=self.api_url + "/layers",
                            json={"workspace": workspace},
                            headers={"Authorization": self.api_token})

        rows_count = r.json()["rowCount"]

        print(f"Deleted {rows_count} rows")

    def add_layers(self, layers: List[Layer]) -> None:
        """Add the given layers to the database."""
        print(f"Adding {len(layers)} to the database")

        for layer in layers:
            self.add_layer(layer)

        print("Finished adding layers to the database")

    def add_layer(self, layer: Layer) -> None:
        """Add the given layer to the database."""
        print(f"Adding layer {layer.name}")

        r = requests.post(url=self.api_url + "/layer",
                          data=layer.__dict__,
                          headers={"Authorization": self.api_token})

        print(f"Added layer {r.json()[0]['name']} with id {r.json()[0]['id']}")


class ApiException(Exception):
    ...
