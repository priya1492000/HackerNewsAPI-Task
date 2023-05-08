import requests
from flask import Blueprint

from cache import Cache

comments_view = Blueprint('comments_routes', __name__)

cache = Cache()

@comments_view.route('/comments/<int:story_id>', methods=["GET"])
def get_comments(story_id):
    try:
        # Check if the comments are already cached
        cached_comments = cache.get(f'comments:{story_id}')
        if cached_comments:
            return cached_comments

        # Fetch the comments for the given story using the Hacker News API
        url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
        response = requests.get(url)
        story = response.json()

        comments = []

        # Process the comments and add them to the list
        for comment_id in story.get('kids', []):
            url = f'https://hacker-news.firebaseio.com/v0/item/{comment_id}.json'
            response = requests.get(url)
            comment = response.json()

            # Add comment details to the list
            comments.append({
                'text': comment.get('text', ''),
                'user': comment.get('by', ''),
                'num_child_comments': comment.get('kids', [])
            })

        # Sort the comments based on the number of child comments
        sorted_comments = sorted(comments, key=lambda c: len(
            c['num_child_comments']), reverse=True)

        # Cache the comments for 15 minutes
        cache.set(f'comments:{story_id}', sorted_comments)

        # Return the top 10 comments
        return sorted_comments[:10]
    except Exception as e:
        print("Error : ", e)
