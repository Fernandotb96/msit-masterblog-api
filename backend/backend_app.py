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
def handle_posts():
    if request.method == 'POST':
        new_post = request.get_json()
        # Check if post is valid
        is_valid, error_message = validate_fields(new_post, ["title", "content"])
        if not is_valid:
            return jsonify({"error": error_message}), 400
        # If valid, get new id and add to the list
        new_id = max((post['id'] for post in POSTS), default=0) + 1
        new_post['id'] = new_id
        POSTS.append(new_post)
        return jsonify(new_post), 201
    # GET request.
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc')
    if sort_field and sort_field not in ['title', 'content']:
        return jsonify({"error": f"Sort field {sort_field} not valid. Only 'title' or 'content' allowed"}), 400
    if direction not in ['asc', 'desc']:
        return jsonify({"error": f"Direction {direction} not valid. Only 'asc' or 'desc' allowed"}), 400
    # Create new sorted list
    if sort_field:
        is_reverse = direction == 'desc'
        sorted_post = sorted(POSTS, key=lambda post: post[sort_field].lower(), reverse=is_reverse)
        return jsonify(sorted_post), 200
    return jsonify(POSTS), 200


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = next((post for post in POSTS if post['id'] == id), None)
    if not post:
        return jsonify({"error": f"Post with id {id} not found."}), 404
    POSTS.remove(post)
    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    # Check post and new content
    post = next((post for post in POSTS if post['id'] == id), None)
    if not post:
        return jsonify({"error": f"Post with id {id} not found."}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": f"Data empty or format not valid."}), 400
    # Updates values
    if 'title' in data:
        post['title'] = data['title']
    if 'content' in data:
        post['content'] = data['content']
    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title = request.args.get('title')
    content = request.args.get('content')
    if not title and not content:
        return jsonify({"error": "Search conditions not provided."}), 400
    results = []
    for post in POSTS:
        match_title = True
        match_content = True
        if title:
            match_title = title.lower() in post['title'].lower()
        if content:
            match_content = content.lower() in post['content'].lower()
        if match_title and match_content:
            results.append(post)
    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
