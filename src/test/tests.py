import unittest
import application

class BasicTestCase(unittest.TestCase):
    
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

if __name__ == '__main__':
    unittest.main()
