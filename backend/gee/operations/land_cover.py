import ee

def run_land_cover(params: dict, region: ee.Geometry) -> ee.Image:
    image = (
        ee.ImageCollection("MODIS/006/MCD12Q1")
        .filterDate(params["start_date"], params["end_date"])
        .first()
        .select("LC_Type1")
        .clip(region)
    )
    return image