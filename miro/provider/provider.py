import logging
from typing import Any
from flask import current_app as app

from . import UpstreamProviderError
from security import safe_requests


logger = logging.getLogger(__name__)

BASE_PATH = "https://api.miro.com/v2"


def search(query) -> list[dict[str, Any]]:
    url = BASE_PATH + "/boards"
    assert (token := app.config.get("ACCESS_TOKEN")), "MIRO_ACCESS_TOKEN must be set"

    params = {"query": query}

    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = safe_requests.get(url,
        headers=headers,
        params=params,
    )

    if response.status_code != 200:
        message = response.text or f"Error: HTTP {response.status_code}"
        raise UpstreamProviderError(message)

    return response.json()["data"]
