from datetime import datetime

import requests
from flask import Blueprint, jsonify

from cache import Cache

stories_view = Blueprint('stories_routes', __name__)

cache = Cache()

def get_top_stories():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(url)
    top_stories_ids = response.json()
    top_stories_ids = top_stories_ids[:10]
    top_stories = []
    for id in top_stories_ids:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{id}.json"
        story_response = requests.get(story_url)
        story = story_response.json()
        if story and "title" in story and "url" in story and "score" in story and "time" in story and "by" in story:
            top_stories.append({
                "id": story["id"],
                "title": story["title"],
                "url": story["url"],
                "score": story["score"],
                "time": datetime.fromtimestamp(story["time"]).strftime("%Y-%m-%d %H:%M:%S"),
                "submitted_by": story["by"]
            })
    return top_stories

@stories_view.route('/top-stories', methods=["GET"])
def top_stories():
    cache_key = "top_stories"
    top_stories = cache.get(cache_key)
    if not top_stories:
        top_stories = get_top_stories()
        top_stories = sorted(top_stories, key=lambda x: x['score'], reverse=True)
        cache.set(cache_key, top_stories)
    return jsonify(top_stories)

@stories_view.route('/past-stories', methods=["GET"])
def past_stories():
    cache_key = "past_stories"
    past_stories = cache.get(cache_key)
    if not past_stories:
        past_stories = []
        top_stories = cache.get("top_stories")
        if top_stories:
            past_stories.append(top_stories)
        else:
            # Top stories not in cache, fetch them from API
            past_stories = get_top_stories()
            cache.set(cache_key, past_stories)
    return jsonify(past_stories)
