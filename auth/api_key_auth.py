from fastapi import Header, HTTPException

# TEMP: hardcoded keys (later → DB / Supabase)
VALID_API_KEYS = {
    "free-key-123": "free",
    "paid-key-456": "paid"
}


def validate_api_key(x_api_key: str = Header(...)):
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return VALID_API_KEYS[x_api_key]
