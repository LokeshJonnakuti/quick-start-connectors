import logging
from typing import Any
from flask import current_app as app

from . import UpstreamProviderError
from security import safe_requests


logger = logging.getLogger(__name__)

DEFAULT_SCOPE = "projects"
DEFAULT_SEARCH_URL = "https://gitlab.com/api/v4/search"
DEFAULT_RESULTS_PER_PAGE = 5


def search(query) -> list[dict[str, Any]]:
    url = app.config.get("SEARCH_URL", DEFAULT_SEARCH_URL)
    assert (token := app.config["TOKEN"]), "GITLAB_TOKEN must be set"

    response = safe_requests.get(url,
        headers={
            "PRIVATE-TOKEN": token,
        },
        params={
            "search": query,
            "scope": app.config.get("SCOPE", DEFAULT_SCOPE),
            "per_page": app.config.get("RESULTS_PER_PAGE", DEFAULT_RESULTS_PER_PAGE),
        },
    )

    if response.status_code != 200:
        message = (
            response.json().get("message") or f"Error: HTTP {response.status_code}"
        )
        raise UpstreamProviderError(message)

    return response.json()
