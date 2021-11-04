import unittest
from src.app import app
import requests


app.testing = True

class TestModule(unittest.TestCase):
        
    def test_login(self):
        tester = app.test_client(self)
        inp = {"userid": "sriram123", "password": "sriram12345"}
        response = requests.post("http://127.0.0.1:5000/login", data=inp)
        self.assertEqual(response.status_code, 200)
        
        
if __name__ == "__main__":
    unittest.main()
