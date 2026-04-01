from src.aeroplane import Aeroplane
from src.api import OpenSkyAPI
from src.storage import JSONStorage
from src.user_interface import user_interaction


def main():
    api = OpenSkyAPI()
    country = input("Введите название страны: ").strip()
    try:
        raw_data = api.get_aeroplanes(country)
        if not raw_data:
            print("Нет данных о самолетах в указанном регионе.")
            return
        aeroplanes = Aeroplane.from_api_data(raw_data)
        print(f"Получено {len(aeroplanes)} самолетов.")
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return

    storage = JSONStorage()
    user_interaction(aeroplanes, storage)


if __name__ == "__main__":
    main()
