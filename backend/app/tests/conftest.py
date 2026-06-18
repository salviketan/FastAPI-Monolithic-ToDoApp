from collections.abc import Generator
from typing import Any
from unittest.mock import MagicMock

import pytest

from app.api.deps import get_db
from app.main import app

mock_session = MagicMock()


def overide_get_db() -> Generator[MagicMock, Any, None]:
    try:
        yield mock_session
    finally:
        pass


app.dependency_overrides[get_db] = overide_get_db


@pytest.fixture
def mock_db_session() -> MagicMock:
    return mock_session
