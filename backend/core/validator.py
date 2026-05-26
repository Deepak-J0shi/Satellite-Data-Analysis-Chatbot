from pydantic import BaseModel, field_validator
from typing   import Optional, Literal
from datetime import date

OPERATION_WHITELIST = {
    "NDVI",
    "EVI",
    "NDWI",
    "SAR",
    "LAND_COVER",
    "FLOOD",
    "BURN_AREA",
    "URBAN_HEAT",
    "CLIMATE",
    "TIMESERIES",
}

SATELLITE_WHITELIST = {
    "LANDSAT_8",
    "LANDSAT_9",
    "SENTINEL_1",
    "SENTINEL_2",
    "MODIS",
}

# ── GEE Command Schema ───────────────────────
class RegionSchema(BaseModel):
    type : Literal["named", "bbox"]
    value: str

class DateRangeSchema(BaseModel):
    start: str
    end  : str

    @field_validator("start", "end")
    @classmethod
    def validate_date(cls, v):
        try:
            d = date.fromisoformat(v)
        except ValueError:
            raise ValueError(f"Invalid date format: {v}. Use YYYY-MM-DD")
        if d > date.today():
            raise ValueError(f"Date {v} cannot be in the future")
        return v

class GEECommand(BaseModel):
    operation  : str
    satellite  : str
    region     : RegionSchema
    date_range : DateRangeSchema
    output_mode: Literal["tile_preview", "full_export"] = "tile_preview"
    parameters : Optional[dict] = {}

    @field_validator("operation")
    @classmethod
    def validate_operation(cls, v):
        if v not in OPERATION_WHITELIST:
            raise ValueError(
                f"Operation '{v}' not allowed. "
                f"Allowed: {OPERATION_WHITELIST}"
            )
        return v

    @field_validator("satellite")
    @classmethod
    def validate_satellite(cls, v):
        if v not in SATELLITE_WHITELIST:
            raise ValueError(
                f"Satellite '{v}' not allowed. "
                f"Allowed: {SATELLITE_WHITELIST}"
            )
        return v

# ── Validate function ────────────────────────
def validate_command(raw: dict) -> tuple[GEECommand | None, str | None]:
    """
    Returns (GEECommand, None) on success
    Returns (None, error_message) on failure
    """
    try:
        command = GEECommand(**raw)
        return command, None
    except Exception as e:
        return None, str(e)
    
