# TEMP in-memory usage (later → DB)

USAGE_COUNTER = {}


def check_usage(api_key: str, plan: str):
    if api_key not in USAGE_COUNTER:
        USAGE_COUNTER[api_key] = 0

    if plan == "free" and USAGE_COUNTER[api_key] >= 2:
        return False

    USAGE_COUNTER[api_key] += 1
    return True
