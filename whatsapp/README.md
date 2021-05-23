# Whatsapp example

This app will allow:
1. Users to send messages to other users
2. Sign up of new users
3. User can edit their phone number and the last message
4. User can get their chats

## Setup

1. Install requirements in a virtualenv `$pip install -r requirements.txt`
2. Create database (from python console):
   ```python
   >>> from app import db
   >>> db.create_all()
   ```
3. Run the flask server `$python run.py`