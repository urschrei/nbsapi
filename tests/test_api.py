import json
from unittest.mock import patch

from fastapi.testclient import TestClient

from nbsapi.main import app

client = TestClient(app)
