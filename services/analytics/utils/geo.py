from user_agents import parse

def parse_user_agent(ua_string: str) -> dict:
    try:
        ua = parse(ua_string)
        if ua.is_mobile:
            device_type = "mobile"
        elif ua.is_tablet:
            device_type = "tablet"
        else:
            device_type = "desktop"

        return {
            "device_type": device_type,
            "browser": ua.browser.family or "unknown"
        }
    except Exception:
        return {
            "device_type": "unknown",
            "browser": "unknown"
        }