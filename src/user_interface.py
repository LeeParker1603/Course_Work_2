from typing import List

from src.aeroplane import Aeroplane
from src.storage import JSONStorage


def user_interaction(aeroplanes: List[Aeroplane], storage: JSONStorage) -> None:
    """
    Функция взаимодействия с пользователем.
    Выводит меню и обрабатывает действия.
    """
    print("\n=== Управление данными о самолетах ===")
    while True:
        print("\nДоступные действия:")
        print("1. Сохранить данные в файл")
        print("2. Показать топ N самолетов по высоте")
        print("3. Фильтрация по стране регистрации")
        print("4. Показать все самолеты")
        print("5. Выход")
        choice = input("Выберите действие (1-5): ").strip()

        if choice == "1":
            for plane in aeroplanes:
                storage.add_aeroplane(plane)
            print("Данные сохранены в файл.")

        elif choice == "2":
            try:
                n = int(input("Введите количество N для топа: "))
                if n <= 0:
                    print("N должно быть положительным числом.")
                    continue

                # Фильтруем только самолеты с известной высотой
                valid_planes = [p for p in aeroplanes if p.altitude is not None]
                if not valid_planes:
                    print("Нет данных о высоте ни для одного самолета.")
                    continue

                sorted_by_alt = sorted(aeroplanes, key=lambda p: (p.altitude is None, p.altitude), reverse=True)
                top_n = sorted_by_alt[:n]
                print(f"\nТоп {n} самолетов по высоте:")
                for i, plane in enumerate(top_n, 1):
                    alt = plane.altitude if plane.altitude is not None else "нет данных"
                    print(f"{i}. {plane.callsign} ({plane.origin_country}) - высота: {alt} м")
            except ValueError:
                print("Ошибка: введите целое число.")

        elif choice == "3":
            countries = input("Введите названия стран для фильтрации (через пробел): ").split()
            if not countries:
                print("Страны не указаны.")
                continue
            filtered = [p for p in aeroplanes if p.origin_country in countries]
            print(f"\nНайдено самолетов: {len(filtered)}")
            for plane in filtered:
                print(
                    f"  {plane.callsign} ({plane.origin_country}) - скорость: {plane.velocity:.1f} км/ч, "
                    f"высота: {plane.altitude if plane.altitude is not None else 'нет данных'} м"
                )

        elif choice == "4":
            if not aeroplanes:
                print("Нет данных о самолетах.")
            else:
                print("\nВсе самолеты:")
                for plane in aeroplanes:
                    print(
                        f"  {plane.callsign} ({plane.origin_country}) - скорость: {plane.velocity:.1f} км/ч, "
                        f"высота: {plane.altitude if plane.altitude is not None else 'нет данных'} м"
                    )

        elif choice == "5":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
