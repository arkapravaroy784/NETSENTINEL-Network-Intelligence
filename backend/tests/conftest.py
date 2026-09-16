"""Database isolation for backend API tests."""

from __future__ import annotations

import sys
from collections.abc import Iterator
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BACKEND_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.db import Base
from app.main import app
import app.main as main


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    """Provide an API client backed by a fresh SQLite database per test."""
    test_directory = Path(__file__).parent / ".test-tmp"
    test_directory.mkdir(exist_ok=True)
    database_path = test_directory / f"netsentinel-{uuid4()}.db"
    test_engine = create_engine(
        f"sqlite+pysqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )
    test_session = sessionmaker(bind=test_engine, expire_on_commit=False)

    # The API module owns the runtime references used by both its dependency
    # and startup handler. Replacing those references leaves production
    # settings/engines untouched while allowing TestClient's lifespan to build
    # the schema against this test-only database.
    monkeypatch.setattr(main, "engine", test_engine)
    monkeypatch.setattr(main, "Session", test_session)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(test_engine)
    test_engine.dispose()
    database_path.unlink(missing_ok=True)
