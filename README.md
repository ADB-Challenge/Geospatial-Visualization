# Geospatial Visualization

Interactive kepler.gl maps for the ADB AI for Safer Roads challenge, published via
GitHub Pages.

## Live maps

- Map 1, Speed Safety Score 1: https://adb-challenge.github.io/Geospatial-Visualization/team-gaudt-speedsafetyscore-1-svi-viz.html
- Map 2, Speed Safety Score 2: https://adb-challenge.github.io/Geospatial-Visualization/team-gaudt-speedsafetyscore-2-svi-viz.html
- Landing page: https://adb-challenge.github.io/Geospatial-Visualization/

Map 1 shows the per-segment Speed Safety Score, with accident points that carry
the Street View image and its object detections. Map 2 shows the final risk
classification, with the 2024 accident count on each segment. Both are in `docs/`.

## Layout

- `docs/`: the two map HTMLs, their segment CSVs, the accident-point CSV, and the
  landing page. This folder is the GitHub Pages source.
- `acc_thumbs/`: labelled Street View thumbnails, served over the jsDelivr CDN so
  Pages stays light.
- `acc_finalize.py`: builds the accident-point dataset and thumbnails.

Point images load from `cdn.jsdelivr.net/gh/ADB-Challenge/Geospatial-Visualization`.
