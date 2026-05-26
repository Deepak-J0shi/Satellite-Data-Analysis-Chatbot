import ee

def run_evi(params: dict, region: ee.Geometry) -> ee.Image:
    # EVI = 2.5 * (NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1)
    # NDVI se better — dense forests ke liye

    collection = (
        ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
        .filterBounds(region)
        .filterDate(params["start_date"], params["end_date"])
    )

    def compute_evi(img):
        nir  = img.select("SR_B5").multiply(0.0000275).add(-0.2)
        red  = img.select("SR_B4").multiply(0.0000275).add(-0.2)
        blue = img.select("SR_B2").multiply(0.0000275).add(-0.2)

        evi = (
            nir.subtract(red)
               .multiply(2.5)
               .divide(
                   nir.add(red.multiply(6))
                      .subtract(blue.multiply(7.5))
                      .add(1)
               )
               .rename("EVI")
        )
        return evi

    return collection.map(compute_evi).median()