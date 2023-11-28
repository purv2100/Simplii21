import inspect
import unittest
import sys
import os
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir) 
sys.path.insert(0, parentdir)
from Simplii_App.application import app
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

    def test_about_us(self):
        self.app = app.test_client()
        ans = self.app.get('/about_us')
        self.assertEqual(ans.status_code, 200)

    def test_register(self):
        self.app = app.test_client()
        ans = self.app.get('/register')
        self.assertEqual(ans.status_code, 200)

    def test_forum(self):
        self.app = app.test_client()
        ans = self.app.get('/forum')
        self.assertEqual(ans.status_code, 200)

    def test_task(self):
        self.app = app.test_client()
        ans = self.app.get('/task')
        self.assertEqual(ans.status_code, 302)

    def test_completeTask(self):
        self.app = app.test_client()
        ans = self.app.get('/completeTask')
        self.assertEqual(ans.status_code, 405)
    
    def test_delete_task(self):
        self.app = app.test_client()
        ans = self.app.get('/deleteTask')
        self.assertEqual(ans.status_code, 200)    

    def test_analytics(self):
        self.app = app.test_client()
        ans = self.app.get('/analytics')
        self.assertEqual(ans.status_code, 302)  

    def test_friends(self):
        self.app = app.test_client()
        ans = self.app.get('/friends')
        self.assertEqual(ans.status_code, 302)  

    def test_logout(self):
        self.app = app.test_client()
        ans = self.app.get('/logout')
        self.assertEqual(ans.status_code, 200)



if __name__ == '__main__':
    unittest.main()
