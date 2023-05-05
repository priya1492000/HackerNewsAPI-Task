from flask import Flask

from routes.comments import comments_view
from routes.stories import stories_view

app = Flask(__name__)

app.register_blueprint(stories_view)
app.register_blueprint(comments_view)

@app.route('/')
def default():
    return 'Hacker News API'

if __name__ == "__main__":
    app.run(debug=True, port=5000,host='0.0.0.0')
