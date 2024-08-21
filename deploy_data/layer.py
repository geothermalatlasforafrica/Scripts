from dataclasses import dataclass


@dataclass
class Layer:
    name: str
    full_name: str
    filename: str
    type: str
    url: str
    unit: str
    workspace: str
    layer_group: str
    parent_group: str
    description: str
    keywords: str
    date: str
    restricted: str
    resolution: str
