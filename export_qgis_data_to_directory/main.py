import processing
import glob
import zipfile
import os
from os import path

style_path = "C:\\Users\\mosj\\Desktop\\gaa-testing"

layers = QgsProject.instance().mapLayers().values()
for layer in layers:
    name = layer.name()
    print(name, end=", ")
    if isinstance(layer, QgsVectorLayer):
        writer = QgsVectorFileWriter.writeAsVectorFormat(layer, path.join(style_path, name), "utf-8", layer.crs(),
                                                         "ESRI Shapefile")
        files_to_zip = [file for file in glob.glob(f"{path.join(style_path, name)}.*") if not file.endswith(".zip")]

        with zipfile.ZipFile(path.join(style_path, name) + ".zip", "w") as z:
            for file in files_to_zip:
                z.write(file, path.basename(file))

        files_to_remove = files_to_zip
        for file in files_to_remove:
            os.remove(file)
    elif isinstance(layer, QgsRasterLayer):
        pipe = QgsRasterPipe()
        pipe.set(layer.dataProvider().clone())
        filename = path.join(style_path, name + ".tif")
        writer = QgsRasterFileWriter(filename)
        writer.writeRaster(pipe, layer.width(), layer.height(), layer.extent(), layer.crs(),
                           QgsProject().instance().transformContext())
    else:
        ValueError("layer type not supported")

    pathqml = path.join(style_path, str(name) + '.qml')
    pathsld = path.join(style_path, str(name) + '.sld')
    layer.saveNamedStyle(pathqml)
    layer.saveSldStyle(pathsld)

print("\n\nExport finished")
