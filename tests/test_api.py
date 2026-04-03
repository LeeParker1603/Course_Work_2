from unittest.mock import Mock, patch

import pytest

from src.api import OpenSkyAPI


class TestOpenSkyAPI:
    @patch("src.api.requests.Session.get")
    def test_get_country_bbox(self, mock_get, mock_nominatim_response):
        mock_get.return_value = mock_nominatim_response
        api = OpenSkyAPI()
        bbox = api.get_country_bbox("Spain")
        assert bbox == (10.0, 20.0, 30.0, 40.0)
        # Проверка параметров запроса
        args, kwargs = mock_get.call_args
        assert kwargs["params"]["q"] == "Spain"
        assert kwargs["params"]["format"] == "json"

    @patch("src.api.requests.Session.get")
    def test_get_country_bbox_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        api = OpenSkyAPI()
        with pytest.raises(ValueError, match="Страна 'NotFound' не найдена"):
            api.get_country_bbox("NotFound")

    @patch("src.api.requests.Session.get")
    def test_get_aeroplanes(self, mock_get, mock_nominatim_response, mock_api_response):
        # Первый вызов (nominatim) -> bbox
        # Второй вызов (opensky) -> данные самолетов
        mock_get.side_effect = [mock_nominatim_response, mock_api_response]
        api = OpenSkyAPI()
        states = api.get_aeroplanes("Spain")
        assert len(states) == 3
        # Проверка параметров второго запроса
        args_list = mock_get.call_args_list
        # Первый вызов: nominatim
        assert args_list[0][1]["params"]["q"] == "Spain"
        # Второй вызов: opensky с bbox
        expected_params = {"lamin": 10.0, "lamax": 20.0, "lomin": 30.0, "lomax": 40.0}
        assert args_list[1][1]["params"] == expected_params

    @patch("src.api.requests.Session.get")
    def test_get_aeroplanes_empty_states(self, mock_get, mock_nominatim_response):
        mock_sky_response = Mock()
        mock_sky_response.json.return_value = {"states": []}
        mock_sky_response.raise_for_status = Mock()
        mock_get.side_effect = [mock_nominatim_response, mock_sky_response]
        api = OpenSkyAPI()
        states = api.get_aeroplanes("Spain")
        assert states == []
