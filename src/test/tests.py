import unittest
import application

class BasicTestCase(unittest.TestCase):
    
    def test_login(self):
        self.app=application.app.test_client()
        ans=self.app.get('/login')
        self.assertEqual(ans.status_code,200)

    def test_home(self):
        self.app=application.app.test_client()
        ans=self.app.get('/home')
        self.assertEqual(ans.status_code,302)

    def test_forgotPassword(self):
        self.app=application.app.test_client()
        ans=self.app.get('/forgotPassword')
        self.assertEqual(ans.status_code,302)
    
    def test_dashboard(self):
        self.app=application.app.test_client()
        ans=self.app.get('/dashboard')
        self.assertEqual(ans.status_code,200)

    def test_about(self):
        self.app=application.app.test_client()
        ans=self.app.get('/about')
        self.assertEqual(ans.status_code,302)

    def test_register(self):
        self.app=application.app.test_client()
        ans=self.app.get('/register')
        self.assertEqual(ans.status_code,200)

    def test_task(self):
        self.app=application.app.test_client()
        ans=self.app.get('/task')
        self.assertEqual(ans.status_code,302)

    def test_editTask(self):
        self.app=application.app.test_client()
        ans=self.app.get('/editTask')
        self.assertEqual(ans.status_code,200)
    
    def test_updateTask(self):
            self.app=application.app.test_client()
            ans=self.app.get('/updateTask')
            self.assertEqual(ans.status_code,302)

    def test_logout(self):
        self.app=application.app.test_client()
        ans=self.app.get('/logout')
        self.assertEqual(ans.status_code,200)

    def test_dummy(self):
        self.app=application.app.test_client()
        ans=self.app.get('/dummy')
        self.assertEqual(ans.status_code,200)

    def test_delete(self):
        self.app=application.app.test_client()
        ans=self.app.get('/deleteTask')
        self.assertEqual(ans.status_code,200)


if __name__ == '__main__':
    unittest.main()
