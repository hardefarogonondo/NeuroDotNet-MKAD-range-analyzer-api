from app import app
from blueprint import API_HIT_COUNTER, API_HIT_START_TIME, get_coordinates
from datetime import datetime
from unittest.mock import patch
import unittest


class TestMKADBlueprint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        global API_HIT_COUNTER, API_HIT_START_TIME
        API_HIT_COUNTER = 0
        API_HIT_START_TIME = datetime.now()

    def test_invalid_address(self):
        with patch('blueprint.get_coordinates', return_value=(None, None, None)):
            response = self.app.post(
                '/distance', json={"address": "Invalid Address"})
            self.assertEqual(response.status_code, 500)

    def test_valid_address(self):
        with patch('requests.get') as mock_get, patch('blueprint.API_limit_checker', return_value=(True, "")):
            mock_get.return_value.json.return_value = {
                "response": {
                    "GeoObjectCollection": {
                        "featureMember": [{
                            "GeoObject": {
                                "Point": {
                                    "pos": "37.6156 55.7522"
                                },
                                "metaDataProperty": {
                                    "GeocoderMetaData": {
                                        "precision": "exact"
                                    }
                                }
                            }
                        }]
                    }
                }
            }
            response = self.app.post(
                '/distance', json={"address": "Red Square, Moscow"})
            self.assertEqual(response.status_code, 200)

    def test_get_coordinates(self):
        with patch('requests.get') as mock_get, patch('blueprint.API_limit_checker', return_value=(True, "")):
            mock_get.return_value.json.return_value = {
                "response": {
                    "GeoObjectCollection": {
                        "featureMember": [{
                            "GeoObject": {
                                "Point": {
                                    "pos": "37.6156 55.7522"
                                },
                                "metaDataProperty": {
                                    "GeocoderMetaData": {
                                        "precision": "exact"
                                    }
                                }
                            }
                        }]
                    }
                }
            }
            response = self.app.post(
                '/distance', json={"address": "Red Square, Moscow"})
            self.assertEqual(response.status_code, 200)
            lat, lon, precision = get_coordinates("Some Address")
            self.assertEqual(lat, 55.7522)
            self.assertEqual(lon, 37.6156)
            self.assertEqual(precision, "exact")

    def test_address_outside_mkad(self):
        outside_mkad_address = "56.90415423821526, 24.161043293273217"
        with patch('requests.get') as mock_get, patch('blueprint.API_limit_checker', return_value=(True, "")):
            mock_get.return_value.json.return_value = {
                "response": {
                    "GeoObjectCollection": {
                        "featureMember": [{
                            "GeoObject": {
                                "Point": {
                                    "pos": "24.161043293273217 56.90415423821526"
                                },
                                "metaDataProperty": {
                                    "GeocoderMetaData": {
                                        "precision": "exact"
                                    }
                                }
                            }
                        }]
                    }
                }
            }
            response = self.app.post(
                '/distance', json={"address": outside_mkad_address})
            self.assertEqual(response.status_code, 200)

    def test_rate_limits(self):
        for _ in range(21):
            response = self.app.post(
                '/distance', json={"address": "Red Square, Moscow"})
        self.assertEqual(response.status_code, 429)

    def tearDown(self):
        global API_HIT_COUNTER, API_HIT_START_TIME
        API_HIT_COUNTER = 0
        API_HIT_START_TIME = datetime.now()


if __name__ == "__main__":
    unittest.main()
