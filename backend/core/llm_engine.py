import json
from groq import Groq
from config import settings

client = Groq(api_key=settings.groq_api_key)

SYSTEM_PROMPT = """You are a satellite data analysis assistant.
Your ONLY job is to convert natural language queries into a JSON command.

You MUST return ONLY valid JSON — no explanation, no markdown, no extra text.

JSON Schema you must follow:
{
  "operation"  : one of [NDVI, SAR, LAND_COVER, FLOOD, BURN_AREA, EVI, NDWI, URBAN_HEAT, CLIMATE, TIMESERIES],
  "satellite"  : one of [LANDSAT_8, LANDSAT_9, SENTINEL_1, SENTINEL_2, MODIS],
  "region"     : {"type": "named", "value": "<place name>"},
  "date_range" : {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
  "output_mode": "tile_preview" or "full_export",
  "parameters" : {"cloud_mask": true, "composite_method": "median"}
}

Rules:
- operation NDVI, EVI, NDWI, BURN_AREA → use LANDSAT_8 or SENTINEL_2
- operation SAR, FLOOD               → use SENTINEL_1
- operation LAND_COVER, CLIMATE      → use MODIS
- output_mode default is tile_preview unless user says "download" or "export"
- Never return anything except the JSON object
"""

def get_llm_response(
    user_message  : str,
    history       : list[dict] = [],
    retry_error   : str | None = None
) -> dict | None:
    """
    Calls Groq → returns parsed JSON dict
    Falls back to Gemini if rate limited
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Inject conversation history
    for turn in history[-5:]:  # last 5 turns only
        messages.append(turn)

    # If retry, add error context
    if retry_error:
        user_message = (
            f"{user_message}\n\n"
            f"Your previous response had this error: {retry_error}\n"
            f"Fix it and return valid JSON only."
        )

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model          = "llama-3.3-70b-versatile",
            messages       = messages,
            temperature    = 0,
            response_format= {"type": "json_object"},
            max_tokens     = 500,
        )
        raw = response.choices[0].message.content
        return json.loads(raw)

    except Exception as e:
        error_str = str(e)
        print(f"Groq error: {error_str}")

        # Fallback to Gemini
        if "rate_limit" in error_str.lower() or "429" in error_str:
            return _gemini_fallback(messages)

        return None


def _gemini_fallback(messages: list) -> dict | None:
    """Gemini Flash fallback jab Groq rate limit ho."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Combine messages into one prompt
        prompt = "\n".join([
            f"{m['role'].upper()}: {m['content']}"
            for m in messages
        ])

        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)

    except Exception as e:
        print(f"Gemini fallback error: {e}")
        return None