import json

import pytest

from src.aeroplane import Aeroplane
from src.storage import JSONStorage


class TestJSONStorage:
    def test_save_and_load(self, temp_storage, sample_aeroplane):
        temp_storage.add_aeroplane(sample_aeroplane)
        data = temp_storage._load()
        assert len(data) == 1
        assert data[0]["icao24"] == "abc123"
        assert data[0]["callsign"] == "ABC123"
        assert data[0]["velocity"] == 850.5

    def test_add_duplicate(self, temp_storage, sample_aeroplane):
        temp_storage.add_aeroplane(sample_aeroplane)
        temp_storage.add_aeroplane(sample_aeroplane)
        data = temp_storage._load()
        assert len(data) == 1  # дубликат не добавлен

    def test_get_aeroplanes(self, temp_storage, sample_aeroplane, sample_aeroplane_no_altitude):
        temp_storage.add_aeroplane(sample_aeroplane)
        temp_storage.add_aeroplane(sample_aeroplane_no_altitude)
        criteria = {"origin_country": "Russia"}
        results = temp_storage.get_aeroplanes(criteria)
        assert len(results) == 1
        assert results[0].icao24 == "abc123"
        # Нет совпадений
        results = temp_storage.get_aeroplanes({"origin_country": "Canada"})
        assert len(results) == 0
        # Несколько критериев
        results = temp_storage.get_aeroplanes({"origin_country": "USA", "callsign": "DEF456"})
        assert len(results) == 1

    def test_delete_aeroplane(self, temp_storage, sample_aeroplane, sample_aeroplane_no_altitude):
        temp_storage.add_aeroplane(sample_aeroplane)
        temp_storage.add_aeroplane(sample_aeroplane_no_altitude)
        temp_storage.delete_aeroplane(sample_aeroplane)
        data = temp_storage._load()
        assert len(data) == 1
        assert data[0]["icao24"] == "def456"

    def test_delete_all(self, temp_storage, sample_aeroplane):
        temp_storage.add_aeroplane(sample_aeroplane)
        temp_storage.delete_all()
        data = temp_storage._load()
        assert len(data) == 0

    def test_load_empty(self, temp_storage):
        data = temp_storage._load()
        assert data == []

    def test_to_dict_from_dict(self, temp_storage, sample_aeroplane):
        d = temp_storage._to_dict(sample_aeroplane)
        assert d["callsign"] == "ABC123"
        restored = temp_storage._from_dict(d)
        assert restored.callsign == sample_aeroplane.callsign
        assert restored.origin_country == sample_aeroplane.origin_country
        assert restored.velocity == sample_aeroplane.velocity
        assert restored.altitude == sample_aeroplane.altitude
