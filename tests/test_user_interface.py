from unittest.mock import patch

import pytest

from src.storage import JSONStorage
from src.user_interface import user_interaction


class TestUserInterface:
    @patch("builtins.input", side_effect=["5"])  # выбор выхода
    @patch("builtins.print")
    def test_exit(self, mock_print, mock_input, sample_aeroplane, temp_storage):
        user_interaction([sample_aeroplane], temp_storage)
        # Проверяем, что функция завершилась без ошибок
        mock_print.assert_any_call("\n=== Управление данными о самолетах ===")

    @patch("builtins.input", side_effect=["2", "1", "5"])  # топ, n=1, выход
    @patch("builtins.print")
    def test_top_n(self, mock_print, mock_input, sample_aeroplane, temp_storage):
        user_interaction([sample_aeroplane], temp_storage)
        # Проверяем, что вызвался вывод топа
        # можно проверить вызов print с определенной строкой
        # Для простоты: проверим, что print вызывался с аргументом, содержащим "Топ"
        calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
        assert any("Топ" in str(call) for call in calls)

    @patch("builtins.input", side_effect=["3", "Russia", "5"])  # фильтр, страна, выход
    @patch("builtins.print")
    def test_filter_by_country(self, mock_print, mock_input, sample_aeroplane, temp_storage):
        user_interaction([sample_aeroplane], temp_storage)
        calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
        assert any("Найдено самолетов: 1" in str(call) for call in calls)
