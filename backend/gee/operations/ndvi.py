import ee

def run_ndvi(params: dict, region: ee.Geometry) -> ee.Image:
    if params["satellite"] == "LANDSAT_8":
        collection = (
            ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
            .filterBounds(region)
            .filterDate(params["start_date"], params["end_date"])
        )
        if params.get("parameters", {}).get("cloud_mask", True):
            def mask_clouds(img):
                qa    = img.select("QA_PIXEL")
                cloud = qa.bitwiseAnd(1 << 3).eq(0)
                return img.updateMask(cloud)
            collection = collection.map(mask_clouds)

        composite = collection.median()
        ndvi = composite.normalizedDifference(["SR_B5", "SR_B4"]).rename("NDVI")

    elif params["satellite"] == "SENTINEL_2":
        collection = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(region)
            .filterDate(params["start_date"], params["end_date"])
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        )
        composite = collection.median()
        ndvi = composite.normalizedDifference(["B8", "B4"]).rename("NDVI")

    else:
        raise ValueError(f"NDVI ke liye {params['satellite']} supported nahi")

    return ndvi