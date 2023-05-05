import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from app1 import app

class TestStoriesRoutes(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
    
    def test_top_stories(self):
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = [123, 456, 789]
            response = self.app.get('/top-stories')
            self.assertEqual(response.status_code, 200)
    
    def test_past_stories(self):
        with patch('cache.Cache.get') as mock_get:
            with patch('cache.Cache.set') as mock_set:
                mock_get.return_value = [{"id": 123, "title": "test story", "url": "http://example.com", "score": 10, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "submitted_by": "test user"}]
                response = self.app.get('/past-stories')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.json), 1)
                mock_get.assert_called_once_with("past_stories")
                mock_set.assert_not_called()

if __name__ == '__main__':
    unittest.main()
