from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from typing import Optional


def build_url(base_url: str, params: dict) -> str:
    filter_parameters = {k: v for k, v in params.items() if v is not None}
    if not params:
        return base_url
    return f"{base_url}?{urlencode(filter_parameters)}"


def update_page_in_url(url: str, page: Optional[int]) -> str:
    if not page:
        return url
    p = urlparse(url)  # get each element in url into dict
    q = parse_qs(p.query)  # convert string query to dict
    q["page"] = [str(page)]  # change value page
    return urlunparse(p._replace(query=urlencode(q, doseq=True)))
