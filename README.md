This repository comprises the scripts utilized for the manuscript entitled "The Association of Podometric Findings in Patients with Hypertension and Type 2 Diabetes: A Retrospective Analysis."

For glomeruli segmentation, we employed the NoCodeSeg method alongside scripts published by Pettersen et al. (https://doi.org/10.3389/fmed.2021.816281; https://github.com/andreped/NoCodeSeg). Specifically, the script "1_exportTiles_with_annotations" was used to export tiles and ground truth files for training our segmentation model, while "2_exportTiles_empty" was employed to export empty tiles for predictions.

The script "3_Detection_Workflow" was utilized to detect podocyte nuclei. It was generated through the "Create Script" function in QuPath.

To export polygons of podocyte nuclei into a GeoJSON file, we utilized "4_Polygon_exporter" (Source: https://github.com/choosehappy/QuPathGeoJSONImportExport/blob/master/qupath_export.groovy).

For extracting the mean caliper diameter of podocyte nuclei, we employed Python. The code for the script "5_extract_mean_caliper" was developed by Maximilian C. Koeller.
