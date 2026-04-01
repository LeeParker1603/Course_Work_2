from unittest.mock import Mock, patch

import pytest

from src.aeroplane import Aeroplane
from src.storage import JSONStorage


@pytest.fixture
def sample_aeroplane():
    return Aeroplane(callsign="ABC123", origin_country="Russia", velocity=850.5, altitude=10000, icao24="abc123")


@pytest.fixture
def sample_aeroplane_no_altitude():
    return Aeroplane(callsign="DEF456", origin_country="USA", velocity=700.0, altitude=None, icao24="def456")


@pytest.fixture
def sample_aeroplane_no_velocity():
    return Aeroplane(callsign="GHI789", origin_country="France", velocity=None, altitude=8000, icao24="ghi789")


@pytest.fixture
def mock_api_response():
    """Фикстура для мока ответа OpenSky API"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "states": [
            ["abc123", "ABC123  ", "Russia", 123456, None, 30.0, 50.0, 10000, False, 250.0, None, None],
            ["def456", "DEF456  ", "USA", 123457, None, -80.0, 40.0, None, True, 200.0, None, None],
            ["ghi789", "GHI789  ", "France", 123458, None, 10.0, 60.0, 8000, False, None, None, None],
        ]
    }
    mock_response.raise_for_status = Mock()
    return mock_response


@pytest.fixture
def mock_nominatim_response():
    """Фикстура для мока ответа Nominatim"""
    mock_response = Mock()
    mock_response.json.return_value = [{"boundingbox": ["10.0", "20.0", "30.0", "40.0"]}]
    mock_response.raise_for_status = Mock()
    return mock_response


@pytest.fixture
def temp_storage(tmp_path):
    """Фикстура для временного хранилища JSON"""
    return JSONStorage(filename=str(tmp_path / "test_aeroplanes.json"))
