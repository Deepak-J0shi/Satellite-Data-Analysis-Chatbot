import ee

def run_flood(params: dict, region: ee.Geometry) -> ee.Image:
    # SAR based flood mapping — Sentinel-1
    # Before/after comparison
    start = params["start_date"]
    end   = params["end_date"]

    collection = (
        ee.ImageCollection("COPERNICUS/S1_GRD")
        .filterBounds(region)
        .filter(ee.Filter.eq("instrumentMode", "IW"))
        .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VV"))
        .select("VV")
    )

    # Before flood — start date se 3 months pehle
    before = (
        collection
        .filterDate(
            ee.Date(start).advance(-3, "month"),
            ee.Date(start)
        )
        .median()
    )

    # During/after flood
    after = (
        collection
        .filterDate(start, end)
        .median()
    )

    # Flood = after mein significantly lower backscatter
    diff        = before.subtract(after)
    flood_mask  = diff.gt(3)  # 3dB threshold
    flood_image = after.updateMask(flood_mask)

    return flood_image