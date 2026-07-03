# Street View thumbnails on a kepler.gl map

Hover a road point on the map and see that segment's labelled Street View image
as a tooltip thumbnail.

Files in this folder:
- `thumbs/S####.jpg` — 320 px labelled thumbnails (one per sampled segment)
- `kepler_svi.csv` — the map dataset: `lat, lon, status, speed_limit, f85_kmh,
  percentage_over_speedlimit, road_class, land_use, crashes_2024, <img>`

Regenerate with: `uv run python make_kepler_map.py`

## 1. Host the images on GitHub Pages
The `<img>` column points at `https://IskandarHan.github.io/ADB/thumbs/...`,
so the `docs/` folder must be published:

1. Commit and push `docs/` (thumbnails + CSV) to the **public** `ADB` repo.
2. GitHub repo → **Settings → Pages**.
3. Source: **Deploy from a branch**, branch **main**, folder **/docs**. Save.
4. Wait ~1 minute, then check a thumbnail loads in the browser, e.g.
   `https://IskandarHan.github.io/ADB/thumbs/S0000.jpg`.

(If that URL 404s, the map thumbnails will be blank, so confirm it first.)

## 2. Load the data into kepler.gl
1. Open https://kepler.gl/demo.
2. **Add Data** → either drag in `kepler_svi.csv`, or paste its hosted URL
   `https://IskandarHan.github.io/ADB/kepler_svi.csv`.
3. kepler auto-detects `lat`/`lon` and drops a point layer.

## 3. Turn on the thumbnail tooltip
1. Left panel → **Interactions** → enable **Tooltip**.
2. In the tooltip field list, add **<img>** (kepler renders a URL field as an
   inline image), plus any of `status`, `speed_limit`, `f85_kmh`, `percentage_over_speedlimit`,
   `crashes_2024` you want shown.
3. Hover a point → the labelled Street View thumbnail appears.

## Optional styling
- Colour the points by `status` (OVER/UNDER) or by `percentage_over_speedlimit` to read compliance
  at a glance.
- Size the points by `crashes_2024` to surface crash clusters.

## Notes
- Thumbnails are 320 px (~17 KB) so tooltips load instantly.
- To point at a different host (S3, etc.), edit `BASE_URL` in
  `make_kepler_map.py` and re-run.
