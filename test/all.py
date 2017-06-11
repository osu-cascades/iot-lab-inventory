import unittest
import pdb
import flask_sqlalchemy
from iot_lab_inventory import app, db
from iot_lab_inventory.models import Part


class IntegrationTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_root_url(self):
        response = self.app.get('/')
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()
