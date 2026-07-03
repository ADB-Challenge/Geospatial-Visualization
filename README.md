# Geospatial Visualization

Interactive kepler.gl maps for the ADB AI for Safer Roads challenge, published via
GitHub Pages.

## Maps

- Map 1: per-segment Speed Safety Score, with accident points that carry the
  Street View image and its object detections.
- Map 2: final risk classification, with the 2024 accident count on each segment.

Both are in `docs/` and served at
`https://adb-challenge.github.io/Geospatial-Visualization/`.

## Layout

- `docs/`: the two map HTMLs, their segment CSVs, the accident-point CSV, and the
  landing page. This folder is the GitHub Pages source.
- `acc_thumbs/`: labelled Street View thumbnails, served over the jsDelivr CDN so
  Pages stays light.
- `acc_finalize.py`: builds the accident-point dataset and thumbnails.

Point images load from `cdn.jsdelivr.net/gh/ADB-Challenge/Geospatial-Visualization`.
