
import unittest
from app import app
import sys
import os
import sys

class TestModule(unittest.TestCase):

    def test_application(self):
        test = app.test_client(self)
        response = test.get("/reset_all")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get("/", content_type='html/text')
        self.assertEqual(response.status_code, 200)

#
if __name__ == "__main__":
     unittest.main()