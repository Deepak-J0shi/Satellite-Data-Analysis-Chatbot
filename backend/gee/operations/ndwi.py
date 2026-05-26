import ee

def run_ndwi(params: dict, region: ee.Geometry) -> ee.Image:
    # NDWI = (Green - NIR) / (Green + NIR)
    # Water bodies detect karta hai

    if params["satellite"] in ("LANDSAT_8", "LANDSAT_9"):
        collection = (
            ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
            .filterBounds(region)
            .filterDate(params["start_date"], params["end_date"])
        )
        composite  = collection.median()
        # B3 = Green, B5 = NIR
        ndwi = composite.normalizedDifference(["SR_B3", "SR_B5"]).rename("NDWI")

    elif params["satellite"] == "SENTINEL_2":
        collection = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(region)
            .filterDate(params["start_date"], params["end_date"])
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        )
        composite = collection.median()
        # B3 = Green, B8 = NIR
        ndwi = composite.normalizedDifference(["B3", "B8"]).rename("NDWI")

    else:
        raise ValueError(f"NDWI ke liye {params['satellite']} supported nahi")

    return ndwi