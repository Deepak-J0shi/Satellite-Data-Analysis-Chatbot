import ee

def run_burn_area(params: dict, region: ee.Geometry) -> ee.Image:
    # NBR = (NIR - SWIR) / (NIR + SWIR)
    # Burn area = pre NBR - post NBR (dNBR)

    start = params["start_date"]
    end   = params["end_date"]

    if params["satellite"] in ("LANDSAT_8", "LANDSAT_9"):
        collection = (
            ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
            .filterBounds(region)
            .filterDate(start, end)
        )
        composite = collection.median()
        # NBR = (B5 - B7) / (B5 + B7)
        nbr = composite.normalizedDifference(["SR_B5", "SR_B7"]).rename("NBR")

    elif params["satellite"] == "SENTINEL_2":
        collection = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(region)
            .filterDate(start, end)
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        )
        composite = collection.median()
        # NBR = (B8 - B12) / (B8 + B12)
        nbr = composite.normalizedDifference(["B8", "B12"]).rename("NBR")

    else:
        raise ValueError(f"Burn area ke liye {params['satellite']} supported nahi")

    # Burn areas = low NBR (negative values)
    burn_mask = nbr.lt(-0.1)
    return nbr.updateMask(burn_mask)