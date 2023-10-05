from app import app
from blueprint import get_coordinates
from unittest.mock import patch
import unittest


class TestMKADBlueprint(unittest.TestCase):
    def setup(self):
        self.app = app.test_client()

    def test_valid_address(self):
        response = self.app.post(
            '/distance', json={"address": "Red Square, Moscow"})
        self.assertEqual(response.status_code, 200)

    def test_get_coordinates(self):
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = {
                "response": {
                    "GeoObjectCollection": {
                        "featureMember": [{
                            "GeoObject": {
                                "Point": {
                                    "pos": "37.6156 55.7522"
                                }
                            }
                        }]
                    }
                }
            }
            lat, lon = get_coordinates("Some Address")
            self.assertEqual(lat, 55.7522)
            self.assertEqual(lon, 37.6156)


if __name__ == "__main__":
    unittest.main()
