import os
from datetime import datetime
from whats_app import errors

CHATS_FOLDER = 'chats'


def get_chat_file(user1, user2):
    file_name = f'{user1}_{user2}' if user1 < user2 else f'{user2}_{user1}'
    chat_file_path = f'{CHATS_FOLDER}/{file_name}.txt'
    return chat_file_path


def chat_exists(user1, user2):
    chat_file = get_chat_file(user1, user2)
    return os.path.exists(chat_file)


def create_chat(user1, user2):
    if chat_exists(user1, user2):
        raise errors.ChatAlreadyExistsException(f"Chat between {user1} and {user2} already exists.")

    chat_file = get_chat_file(user1, user2)
    if not os.path.exists(CHATS_FOLDER):  # if the chats folder is not present, then create one
        os.makedirs(CHATS_FOLDER)
    with open(chat_file, 'w'):  # create an empty file
        pass


def parse_message(line):
    timestamp, sender, receiver, text = line.split('<=>')
    return {'timestamp': timestamp, 'from': sender, 'to': receiver, 'text': text}


def create_message(sender, receiver, message):
    formatted_message = '<=>'.join([str(datetime.now()), sender, receiver, message])
    return formatted_message + '\n'


def get_messages(user1, user2, num_messages=10):
    if not chat_exists(user1, user2):
        raise errors.ChatNotFoundException(f'No chat exists between {user1} and {user2}')

    chat_file = get_chat_file(user1, user2)
    with open(chat_file, 'r') as f:
        all_messages = f.readlines()
        recent_history = all_messages[-num_messages:]
        formatted_messages = [parse_message(line) for line in recent_history]
        return formatted_messages


def add_message(user1, user2, message):
    if not chat_exists(user1, user2):
        raise errors.ChatNotFoundException(f'No chat exists between {user1} and {user2}')

    chat_file = get_chat_file(user1, user2)
    with open(chat_file, 'a') as f:
        formatted_message = create_message(user1, user2, message)
        f.write(formatted_message)


def edit_last_message(user1, user2, new_text):
    if not chat_exists(user1, user2):
        raise errors.ChatNotFoundException(f'No chat exists between {user1} and {user2}')

    chat_file = get_chat_file(user1, user2)
    with open(chat_file, 'r') as f:
        lines = f.readlines()

    no_message_found = True
    for index in range(len(lines)-1, -1, -1):
        message = parse_message(lines[index])
        sender = message['from']
        if sender == user1:
            lines[index] = create_message(user1, user2, new_text)
            no_message_found = False
            break

    if no_message_found:
        raise errors.NoPreviousMessageException(f'There is no previous message from {user1}')

    with open(chat_file, 'w') as f:
        f.writelines(lines)
