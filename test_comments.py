import unittest
from unittest.mock import patch

from app1 import app

class TestCommentsRoutes(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    @patch('requests.get')
    def test_get_comments(self, mock_requests_get):
        # Mock the response of the Hacker News API
        story_id = 123456
        mock_comment = {
            'id': 123,
            'text': 'This is a comment',
            'by': 'testuser',
            'kids': [456, 789]
        }
        mock_response = {
            'id': story_id,
            'kids': [mock_comment['id']],
        }
        mock_requests_get.side_effect = [
            # Response for the story
            type('Response', (object,), {'json': lambda: mock_response}),
            # Response for the comment
            type('Response', (object,), {'json': lambda: mock_comment})
        ]

        # Call the endpoint
        response = self.client.get(f'/comments/{story_id}')

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(len(response.json[0]['num_child_comments']), 2)
        self.assertEqual(response.json[0]['user'], 'testuser')
        self.assertEqual(response.json[0]['text'], 'This is a comment')
