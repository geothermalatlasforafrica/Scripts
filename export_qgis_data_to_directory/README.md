The script in this folder exports the styles of all the enabled layers in a QGIS project to `.qml` and `.sld` files. To
run the script, follow these steps:

1. In the QGIS project, go to `Plugins > Python console`
2. Paste the code into the console window that appears
3. In the script, change `style_path` to the directory that the styles need to be exported to
4. Then in the QGIS Layers panel, select all the layers that need to be exported.
5. Then, enable or disable them with space bar.
6. Finally, press the green run button in the Python console and the style files should appear in the export directory.