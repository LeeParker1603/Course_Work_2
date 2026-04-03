import pytest

from src.aeroplane import Aeroplane


class TestAeroplane:
    def test_creation(self, sample_aeroplane):
        assert sample_aeroplane.callsign == "ABC123"
        assert sample_aeroplane.origin_country == "Russia"
        assert sample_aeroplane.velocity == 850.5
        assert sample_aeroplane.altitude == 10000
        assert sample_aeroplane.icao24 == "abc123"
        assert sample_aeroplane.time_position is None

    def test_creation_with_none_callsign(self):
        plane = Aeroplane(None, "Russia", 800, 10000, "xyz789")
        assert plane.callsign == "N/A"

    @pytest.mark.parametrize(
        "callsign,origin,velocity,altitude,icao,expected_error",
        [
            (None, "", 100, 1000, "abc", ValueError),  # пустая страна
            ("ABC", "Russia", "not_number", 1000, "abc", ValueError),  # velocity не число
            ("ABC", "Russia", 100, "not_number", "abc", ValueError),  # altitude не число
            ("ABC", "Russia", 100, 1000, "", ValueError),  # пустой icao24
            (123, "Russia", 100, 1000, "abc", ValueError),  # callsign не строка
        ],
    )
    def test_validation(self, callsign, origin, velocity, altitude, icao, expected_error):
        with pytest.raises(expected_error):
            Aeroplane(callsign, origin, velocity, altitude, icao)

    def test_comparison_speed(self, sample_aeroplane, sample_aeroplane_no_altitude):
        p1 = sample_aeroplane  # 850.5
        p2 = sample_aeroplane_no_altitude  # 700.0
        assert p1 > p2
        assert p2 < p1
        # сравнение с None
        p3 = Aeroplane("XYZ", "UK", None, 5000, "xyz")
        assert p3 < p2  # None считается меньше

    def test_comparison_altitude(self, sample_aeroplane, sample_aeroplane_no_velocity):
        p1 = sample_aeroplane  # 10000
        p2 = sample_aeroplane_no_velocity  # 8000
        assert p1.altitude_gt(p2)
        assert p2.altitude_lt(p1)
        # сравнение с None
        p3 = Aeroplane("XYZ", "UK", 500, None, "xyz")
        assert p3.altitude_lt(p2)  # None считается меньше
        assert p2.altitude_gt(p3)

    def test_from_api_data(self, mock_api_response):
        data = mock_api_response.json()["states"]
        planes = Aeroplane.from_api_data(data)
        assert len(planes) == 3
        # Первый самолет
        p1 = planes[0]
        assert p1.icao24 == "abc123"
        assert p1.callsign == "ABC123"
        assert p1.origin_country == "Russia"
        assert p1.velocity == 250.0 * 3.6  # 900.0
        assert p1.altitude == 10000
        # Второй самолет (нет высоты)
        p2 = planes[1]
        assert p2.icao24 == "def456"
        assert p2.callsign == "DEF456"
        assert p2.origin_country == "USA"
        assert p2.velocity == 200.0 * 3.6
        assert p2.altitude is None
        # Третий самолет (нет скорости)
        p3 = planes[2]
        assert p3.icao24 == "ghi789"
        assert p3.callsign == "GHI789"
        assert p3.origin_country == "France"
        assert p3.velocity is None
        assert p3.altitude == 8000

    def test_from_api_data_geo_altitude(self):
        # Проверка использования геометрической высоты, если барометрическая отсутствует
        data = [["abc123", "ABC123", "Russia", 123456, None, 30.0, 50.0, None, False, 250.0, None, 12000]]
        planes = Aeroplane.from_api_data(data)
        p = planes[0]
        assert p.altitude == 12000
