import unittest
from src.app import app
import requests


app.testing = True

class TestModule(unittest.TestCase):
        
    def test_signup_validation(self):
        tester = app.test_client(self)
        inp = {"userid": "test_user", "firstname":"test_first_name", "lastname":"test_last_name", "email":"test@test.com", "password": "test_password"}
        response = requests.post("http://127.0.0.1:5000/signup", data=inp)
        self.assertEqual(response.status_code, 200)
        
        
if __name__ == "__main__":
    unittest.main()
