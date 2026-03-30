from typing import Optional, List, Any

class Aeroplane:
    """
    Класс, представляющий самолет с его характеристиками.
    Поддерживает сравнение по скорости и высоте.
    """

    def __init__(
        self,
        callsign: Optional[str],
        origin_country: str,
        velocity: Optional[float],
        altitude: Optional[float],
        icao24: str,
        time_position: Optional[int] = None,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
    ):
        # Валидация
        if not isinstance(origin_country, str) or not origin_country.strip():
            raise ValueError("origin_country must be a non-empty string")
        if callsign is not None and not isinstance(callsign, str):
            raise ValueError("callsign must be a string or None")
        if velocity is not None and not isinstance(velocity, (int, float)):
            raise ValueError("velocity must be a number or None")
        if altitude is not None and not isinstance(altitude, (int, float)):
            raise ValueError("altitude must be a number or None")
        if not isinstance(icao24, str) or not icao24.strip():
            raise ValueError("icao24 must be a non-empty string")

        self.callsign = callsign if callsign else "N/A"
        self.origin_country = origin_country
        self.velocity = velocity
        self.altitude = altitude
        self.icao24 = icao24
        self.time_position = time_position
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self) -> str:
        return (f"Aeroplane(callsign={self.callsign}, country={self.origin_country}, "
                f"velocity={self.velocity}, altitude={self.altitude})")

    def __lt__(self, other: "Aeroplane") -> bool:
        """Сравнение по скорости (меньше)"""
        if self.velocity is None and other.velocity is None:
            return False
        if self.velocity is None:
            return True
        if other.velocity is None:
            return False
        return self.velocity < other.velocity

    def __gt__(self, other: "Aeroplane") -> bool:
        """Сравнение по скорости (больше)"""
        if self.velocity is None and other.velocity is None:
            return False
        if self.velocity is None:
            return False
        if other.velocity is None:
            return True
        return self.velocity > other.velocity

    def altitude_lt(self, other: "Aeroplane") -> bool:
        if self.altitude is None and other.altitude is None:
            return False
        if self.altitude is None:
            return True
        if other.altitude is None:
            return False
        return self.altitude < other.altitude

    def altitude_gt(self, other: "Aeroplane") -> bool:
        if self.altitude is None and other.altitude is None:
            return False
        if self.altitude is None:
            return False
        if other.altitude is None:
            return True
        return self.altitude > other.altitude

    @classmethod
    def from_api_data(cls, data: List[Any]) -> List["Aeroplane"]:
        """
        Преобразует данные от OpenSky в список объектов Aeroplane.
        Позиции в списке (согласно документации):
        0: icao24
        1: callsign
        2: origin_country
        3: time_position
        4: last_contact
        5: longitude
        6: latitude
        7: baro_altitude
        8: on_ground
        9: velocity
        """
        aeroplanes = []
        for state in data:
            if not state:
                continue
            icao24 = state[0]
            callsign = state[1].strip() if state[1] else None
            origin_country = state[2] or "Unknown"
            time_position = state[3]
            longitude = state[5]
            latitude = state[6]
            baro_altitude = state[7]
            geo_altitude = state[11] if len(state) > 11 else None
            # Приоритет: сначала барометрическая высота, если None – геометрическая
            altitude = baro_altitude if baro_altitude is not None else geo_altitude
            velocity = state[9]

            if velocity is not None:
                velocity = velocity * 3.6  # м/с -> км/ч

            aeroplanes.append(cls(
                callsign=callsign,
                origin_country=origin_country,
                velocity=velocity,
                altitude=altitude,
                icao24=icao24,
                time_position=time_position,
                longitude=longitude,
                latitude=latitude
            ))
        return aeroplanes