import os
import zipfile

QgsProject.instance().removeAllMapLayers()

data_dir = "C:\work\projects\geothermal-atlas-africa\data\gaa"
root = QgsProject.instance().layerTreeRoot()
all_files = os.listdir(data_dir)
all_files.reverse()

for file in all_files:
    filename = os.fsdecode(file)
    # Handle rasters
    if filename.endswith(".tif"):
        print(filename)
        raster_layer = os.path.join(data_dir, filename)
        rlayer = QgsRasterLayer(raster_layer, filename)
        if not rlayer.isValid():
            raise Exception(f"Layer {filename} failed to load!")
        iface.addRasterLayer(raster_layer, filename)
        layer = QgsProject.instance().mapLayersByName(filename)[0]
        myLayerNode = root.findLayer(layer.id())
        myLayerNode.setExpanded(False)
        myLayerNode.setItemVisibilityChecked(False)

    # Handle shapefiles (in zip)
    if filename.endswith(".zip"):
        print(filename)
        unzipped_dir = os.path.join(data_dir, filename.split('.')[0])
        with zipfile.ZipFile(os.path.join(data_dir, filename), "r") as zip_ref:
            zip_ref.extractall(unzipped_dir)

        shp_filename = filename.split('.')[0] + ".shp"
        vector_layer = QgsVectorLayer(os.path.join(unzipped_dir, shp_filename), shp_filename, "ogr")

        if not vector_layer.isValid():
            raise Exception(f"Layer {shp_filename} failed to load!")

        QgsProject.instance().addMapLayer(vector_layer)

        myLayerNode = root.findLayer(vector_layer.id())
        myLayerNode.setExpanded(False)
        myLayerNode.setItemVisibilityChecked(False)

        # Add styling
        style_filename = os.path.join(data_dir, filename.split('.')[0] + ".qml")
        vector_layer.loadNamedStyle(style_filename)
        vector_layer.triggerRepaint()
