from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_fields(data, required_fields):
    """
    Check if JSON data is valid and contains required fields.
    Returns tuple (is_valid, error_message).
    """
    if not data:
        return False, "Data empty or format not valid."

    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)

    if missing_fields:
        missing_str = ", ".join(missing_fields)
        return False, f"The next fields are missing: {missing_str}"

    return True, None


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        new_post = request.get_json()
        # Check if post is valid
        is_valid, error_message = validate_fields(new_post, ["title", "content"])
        if not is_valid:
            return jsonify({"error": error_message}), 400
        # If valid, get new id and add to the list
        new_id = max((post['id'] for post in POSTS)) + 1
        new_post['id'] = new_id
        POSTS.append(new_post)
        return jsonify(new_post), 201
    # GET request, return all posts
    return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
