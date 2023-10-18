import unittest
import sys
import os
currentdir - os.path.dirname(os .path. abspath(inspect -getfile(inspect .current frame ()))) parentdir = os.path. dirname (currentdir) sys-path.insert(0, parentdir)
from application import app

class BasicTestCase(unittest.TestCase):

    def test_login(self):
        self.app = app.test_client()
        ans = self.app.get('/login')
        self.assertEqual(ans.status_code, 200)

    def test_home(self):
        self.app = app.test_client()
        ans = self.app.get('/home')
        self.assertEqual(ans.status_code, 302)

    def test_forgotPassword(self):
        self.app = app.test_client()
        ans = self.app.get('/forgotPassword')
        self.assertEqual(ans.status_code, 200)

    def test_dashboard(self):
        self.app = app.test_client()
        ans = self.app.get('/dashboard')
        self.assertEqual(ans.status_code, 200)

    def test_about(self):
        self.app = app.test_client()
        ans = self.app.get('/about')
        self.assertEqual(ans.status_code, 200)

    def test_register(self):
        self.app = app.test_client()
        ans = self.app.get('/register')
        self.assertEqual(ans.status_code, 200)

    def test_task(self):
        self.app = app.test_client()
        ans = self.app.get('/task')
        self.assertEqual(ans.status_code, 302)

    def test_editTask(self):
        self.app = app.test_client()
        ans = self.app.get('/editTask')
        self.assertEqual(ans.status_code, 200)

    def test_updateTask(self):
        self.app = app.test_client()
        ans = self.app.get('/updateTask')
        self.assertEqual(ans.status_code, 302)

    def test_logout(self):
        self.app = app.test_client()
        ans = self.app.get('/logout')
        self.assertEqual(ans.status_code, 200)

    def test_dummy(self):
        self.app = app.test_client()
        ans = self.app.get('/dummy')
        self.assertEqual(ans.status_code, 200)

    def test_delete(self):
        self.app = app.test_client()
        ans = self.app.get('/deleteTask')
        self.assertEqual(ans.status_code, 200)


if __name__ == '__main__':
    unittest.main()
