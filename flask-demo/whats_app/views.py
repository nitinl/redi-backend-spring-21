from whats_app import messaging, errors
from whats_app.app import app
from flask import jsonify, request, make_response


@app.route('/')
def home():
    return "Welcome to the whatsapp backend."


@app.route('/start_chat/<string:user1>/<string:user2>', methods=['POST'])
def start_new_chat(user1, user2):
    """
    Creates a new file to store the chat between 2 users.
    """
    try:
        messaging.create_chat(user1, user2)
        return make_response(jsonify(message=f"Chat between {user1} and {user2} created :)"), 200)
    except errors.ChatAlreadyExistsException as e:
        return make_response(jsonify(message=str(e)), 400)


@app.route('/get_messages/<string:user1>/<string:user2>', methods=['GET'])
def get_messages(user1, user2):
    try:
        messages = messaging.get_messages(user1, user2, num_messages=10)
        return make_response(jsonify(messages=messages), 200)
    except errors.ChatNotFoundException as e:
        return make_response(jsonify(message=str(e)), 400)


@app.route('/send_message/<string:from_user>/<string:to_user>', methods=['POST'])
def send_message(from_user, to_user):
    request_body = request.get_json()
    if 'message' not in request_body:
        return make_response(jsonify(error="'message' required in request body"), 400)
    message = request_body['message']
    try:
        messaging.add_message(from_user, to_user, message)
        return make_response(jsonify(response='ok'), 200)
    except errors.ChatNotFoundException as e:
        return make_response(jsonify(message=str(e)), 400)


@app.route('/edit_message/<string:from_user>/<string:to_user>', methods=['PATCH'])
def edit_last_message(from_user, to_user):
    request_body = request.get_json()
    if 'message' not in request_body:
        return make_response(jsonify(error="'message' required in request body"), 400)
    message = request_body['message']
    try:
        messaging.edit_last_message(from_user, to_user, message)
        return make_response(jsonify(response='ok'), 200)
    except (errors.ChatNotFoundException, errors.NoPreviousMessageException) as e:
        return make_response(jsonify(message=str(e)), 400)
