import os
from my_app import utils
from my_app.app import app
from flask import jsonify, request, make_response


@app.route('/')
def home():
    return "Welcome to the note app"


@app.route('/sign_up', methods=['POST'])
def sign_up():
    request_body = request.get_json()
    # check inputs: format should be correct and user should not already exist
    if 'username' not in request_body:
        return make_response(jsonify(error="The body must contain 'username' for sign up."), 400)
    username = request_body['username']

    if utils.user_exists(username):
        return make_response(jsonify(error=f"Username {username} already exists"), 400)

    # create a new directory for the user
    user_notes_folder = f'notes/{username}'
    try:
        os.makedirs(user_notes_folder)
        return make_response(jsonify(message='ok'), 200)
    except Exception as e:
        print(f'error: {str(e)}')
        return make_response(jsonify(error=str(e)), 500)


@app.route('/create_note/<string:username>', methods=['POST'])
def create_note(username):
    # inputs: username, note_name, text
    # check if user is present
    user_notes_folder = f'notes/{username}'
    if not utils.user_exists(username):
        return make_response(jsonify(error=f"Username {username} doesn't exist."), 400)
    # check input format
    request_body = request.get_json()
    if 'note_name' not in request_body or 'text' not in request_body:
        return make_response(jsonify(error="The body must contain 'note_name' and 'text' for create note."), 400)

    # if user present, create a new file
    note_name = request_body['note_name']
    text = request_body['text']
    with open(f'{user_notes_folder}/{note_name}.txt', 'w') as notes_file:
        notes_file.write(text)
    return make_response(jsonify(message='ok'), 200)


@app.route('/delete_note/<string:username>', methods=['DELETE'])
def delete_note(username):
    # find if there is a note with the given name
    # if it exists, then delete the file
    # if it does not exist, then error

    # inputs: note_name, username
    #check if user is present
    if not utils.user_exists(username):
        return make_response(jsonify(error=f"Username {username} doesn't exist."), 400)

    request_body = request.get_json()
    if 'note_name' not in request_body:
        return make_response(jsonify(error="Body should contain 'note_name' for delete request"), 400)
    note_name = request_body['note_name']
    file_path = f'notes/{username}/{note_name}.txt'

    try:
        os.remove(file_path)
        return make_response(jsonify(message='success'), 200)
    except FileNotFoundError:
        return make_response(jsonify(error=f"No note named {note_name}"), 400)


@app.route('/get-note/<string:username>', methods=['GET'])
def get_note(username):
    # check if user is present
    if not utils.user_exists(username):
        return make_response(jsonify(error=f"Username {username} doesn't exist."), 400)

    # check input format
    request_body = request.get_json()
    if 'note_name' not in request_body:
        return make_response(jsonify(error="The body must contain 'note_name' for delete note."), 400)
    user_notes_folder = f'notes/{username}'
    note_name = request['note_name']

    try:
        stored_file = open(f'{user_notes_folder}/{note_name}.txt', 'r')
        note_content = stored_file.read()
        stored_file.close()
        return make_response(jsonify(text=note_content), 200)
    except Exception as e:
        print(f'error: {str(e)}')
        return make_response(jsonify(error=str(e)), 500)


@app.route('/modify-note/<string:username>', methods=['PUT'])
def modify_note(username):
    # check if user is present
    if not utils.user_exists(username):
        return make_response(jsonify(error=f"Username {username} doesn't exist."), 400)

    # take new text as input
    request_body = request.get_json()
    if 'text' not in request_body or 'note_name' not in request_body:
        return make_response(jsonify(error="The body must contain 'note_name' and 'text' for modify note."), 400)
    user_notes_folder = f'notes/{username}'
    note_name = request['note_name']
    text = request_body['text']
    # update the file stored locally
    try:
        stored_file = open(f'{user_notes_folder}/{note_name}.txt', 'w')
        stored_file.write(text)
        stored_file.close()
        return make_response(jsonify(message='ok'), 200)
    except Exception as e:
        print(f'error: {str(e)}')
        return make_response(jsonify(error=str(e)), 500)
