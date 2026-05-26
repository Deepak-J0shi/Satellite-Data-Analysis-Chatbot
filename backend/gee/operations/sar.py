import ee

def run_sar(params: dict, region: ee.Geometry) -> ee.Image:
    collection = (
        ee.ImageCollection("COPERNICUS/S1_GRD")
        .filterBounds(region)
        .filterDate(params["start_date"], params["end_date"])
        .filter(ee.Filter.eq("instrumentMode", "IW"))
        .select("VV")
    )
    return collection.median()