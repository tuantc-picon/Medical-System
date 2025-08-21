from urllib.parse import urlencode


def build_url(base_url: str, params: dict) -> str:
    filter_parameters = {k: v for k, v in params.items() if v is not None}
    if not params:
        return base_url
    return f"{base_url}?{urlencode(filter_parameters)}"
