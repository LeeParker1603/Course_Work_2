import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from src.aeroplane import Aeroplane


class BaseStorage(ABC):
    """Абстрактный класс для хранилища"""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавить самолет в хранилище"""
        pass

    @abstractmethod
    def get_aeroplanes(self, criteria: Dict[str, Any]) -> List[Aeroplane]:
        """Получить самолеты по критериям"""
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удалить самолет из хранилища"""
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """Удалить все данные"""
        pass


class JSONStorage(BaseStorage):
    """Реализация хранилища в JSON-файле в папке data"""

    def __init__(self, filename: str = "data/aeroplanes.json"):
        self.filename = filename
        # Создаем папку data, если её нет
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def _load(self) -> List[Dict[str, Any]]:
        """Загрузить данные из файла"""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self, data: List[Dict[str, Any]]) -> None:
        """Сохранить данные в файл"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _to_dict(self, aeroplane: Aeroplane) -> Dict[str, Any]:
        """Преобразовать объект в словарь"""
        return {
            "callsign": aeroplane.callsign,
            "origin_country": aeroplane.origin_country,
            "velocity": aeroplane.velocity,
            "altitude": aeroplane.altitude,
            "icao24": aeroplane.icao24,
            "time_position": aeroplane.time_position,
            "longitude": aeroplane.longitude,
            "latitude": aeroplane.latitude,
        }

    def _from_dict(self, data: Dict[str, Any]) -> Aeroplane:
        """Восстановить объект из словаря"""
        return Aeroplane(
            callsign=data["callsign"],
            origin_country=data["origin_country"],
            velocity=data["velocity"],
            altitude=data["altitude"],
            icao24=data["icao24"],
            time_position=data["time_position"],
            longitude=data["longitude"],
            latitude=data["latitude"],
        )

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавить самолет (если нет дубликата по icao24)"""
        data = self._load()
        if not any(item["icao24"] == aeroplane.icao24 for item in data):
            data.append(self._to_dict(aeroplane))
            self._save(data)

    def get_aeroplanes(self, criteria: Dict[str, Any]) -> List[Aeroplane]:
        """Получить самолеты по критериям"""
        data = self._load()
        result = []
        for item in data:
            match = True
            for key, value in criteria.items():
                if key not in item:
                    match = False
                    break
                if item[key] != value:
                    match = False
                    break
            if match:
                result.append(self._from_dict(item))
        return result

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удалить самолет по icao24"""
        data = self._load()
        new_data = [item for item in data if item["icao24"] != aeroplane.icao24]
        if len(new_data) != len(data):
            self._save(new_data)

    def delete_all(self) -> None:
        """Очистить хранилище"""
        self._save([])
