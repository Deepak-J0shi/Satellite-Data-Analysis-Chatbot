import ee

def run_urban_heat(params: dict, region: ee.Geometry) -> ee.Image:
    # Land Surface Temperature using Landsat thermal band

    collection = (
        ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
        .filterBounds(region)
        .filterDate(params["start_date"], params["end_date"])
    )

    def apply_scale(img):
        # Landsat Collection 2 scaling factors
        thermal = (
            img.select("ST_B10")
               .multiply(0.00341802)
               .add(149.0)
               .subtract(273.15)  # Kelvin → Celsius
               .rename("LST_Celsius")
        )
        return thermal

    lst = collection.map(apply_scale).mean()
    return lst  