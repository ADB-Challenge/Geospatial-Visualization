"""Finalize the accident-point Street View experiment into kepler-ready data.

Produces:
  * docs/acc_thumbs/A####.jpg            640px labelled thumbnails (one per point)
  * docs/accident_points.csv             one row per accident point (for the kepler
                                          point layer): lat/lon, image, detections,
                                          segment info, Safety Score Level, count
  * updates docs/kepler.gl_safety_score_1_with_objects.csv  (per SEGMENT, with
    objects_detected_pct aggregated from the segment's 2 accident points)
"""
from __future__ import annotations

import json
from collections import defaultdict

import pandas as pd
from PIL import Image

from adb_pipeline import config

EXP = config.OUTPUT_DIR / "_accident_svi"
DOCS = config.ROOT / "docs"
THUMBS = DOCS / "acc_thumbs"
THUMBS.mkdir(parents=True, exist_ok=True)
BASE_URL = "https://cdn.jsdelivr.net/gh/ADB-Challenge/Geospatial-Visualization@geospatial_viz_kepler/acc_thumbs"
FRAME = 640 * 640
THUMB_PX = 640

samples = pd.read_csv(EXP / "samples.csv")
dets = json.load(open(EXP / "detections.json", encoding="utf-8"))
lanes = pd.read_csv(EXP / "lanes.csv").set_index("sample_id")
frac_cols = [c for c in lanes.columns if c.endswith("_frac")]
seg = pd.read_csv(DOCS / "kepler.gl_safety_score_1.geojson.csv")
level_by_oid = seg.set_index("OBJECTID")["Safety Score Level"].to_dict()


def point_pct(sid):
    """Combined YOLO + Mask2Former coverage % dict for one accident point."""
    pct = {}
    v = dets.get(str(sid))
    if v:
        area = defaultdict(float)
        for o in v:
            x1, y1, x2, y2 = o["box"]
            area[o["label"].split("/")[0]] += max(0.0, x2 - x1) * max(0.0, y2 - y1)
        for c, a in area.items():
            pct[c] = a / FRAME * 100
    if sid in lanes.index:
        row = lanes.loc[sid]
        for c in frac_cols:
            pct[c.replace("_frac", "").replace("_", " ")] = float(row[c]) * 100
    return pct


def fmt(pct):
    p = {c: round(v) for c, v in pct.items() if round(v) >= 1}
    return ", ".join(f"{c}: {v}%" for c, v in sorted(p.items(), key=lambda x: -x[1]))


# --- thumbnails + per-point dataset ---
rows = []
made = 0
for _, r in samples.iterrows():
    sid = r["sample_id"]
    src = EXP / "labelled" / f"{sid}.jpg"
    if not src.exists():
        continue
    dst = THUMBS / f"{sid}.jpg"
    if not dst.exists():
        im = Image.open(src).convert("RGB")
        im.thumbnail((THUMB_PX, THUMB_PX))
        im.save(dst, "JPEG", quality=90)
        made += 1
    pol = r.get("PercentOverLimit")
    rows.append({
        "point_id": sid, "OBJECTID": int(r["OBJECTID"]),
        "accidents_on_segment": int(r["n_accidents_segment"]),
        "point_in_segment": int(r["point_in_segment"]),
        "lat": round(float(r["lat"]), 7), "lon": round(float(r["lon"]), 7),
        "cause": r["cause"], "fatal": int(r["n_fatal"]),
        "speed_limit": r.get("SpeedLimit"),
        "f85_kmh": round(float(r["F85thPercentileSpeed"]), 1) if pd.notna(r.get("F85thPercentileSpeed")) else None,
        "percentage_over_speedlimit": round(float(pol) * 100) if pd.notna(pol) else None,
        "road_class": r.get("RoadClass"), "land_use": r.get("LandUse"),
        "safety_score_level": level_by_oid.get(int(r["OBJECTID"]), ""),
        "objects_detected_pct": fmt(point_pct(sid)),
        "<img>": f"{BASE_URL}/{sid}.jpg",        # kepler renders this as a thumbnail
        "image_url": f"{BASE_URL}/{sid}.jpg",    # clickable link
    })
pts = pd.DataFrame(rows)
pts.to_csv(DOCS / "accident_points.csv", index=False)
print(f"[finalize] thumbnails: {made} new | accident_points.csv rows: {len(pts)}")

# --- per-segment aggregate: average the 2 points' coverage per class ---
agg = {}
for oid, grp in samples.groupby("OBJECTID"):
    tot = defaultdict(float)
    n = 0
    for sid in grp["sample_id"]:
        if (EXP / "labelled" / f"{sid}.jpg").exists():
            n += 1
            for c, v in point_pct(sid).items():
                tot[c] += v
    if n:
        agg[int(oid)] = fmt({c: v / n for c, v in tot.items()})

# --- rebuild the merged per-segment CSV from the updated segment CSV ---
merged = seg.copy()
merged["objects_detected_pct"] = merged["OBJECTID"].map(agg).fillna("")
merged.to_csv(DOCS / "kepler.gl_safety_score_1_with_objects.csv", index=False)
print(f"[finalize] merged CSV segments with objects: {(merged['objects_detected_pct']!='').sum()}")
print("\n=== sample point ===")
print(pts[["point_id", "OBJECTID", "accidents_on_segment", "cause", "fatal",
           "safety_score_level", "objects_detected_pct"]].head(3).to_string(index=False))
