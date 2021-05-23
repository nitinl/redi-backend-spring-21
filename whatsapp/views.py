import operator

from flask import request, make_response, jsonify
from app import app, db
import models


@app.route('/sign_up', methods=['POST'])
def sign_up():
    new_user = models.User(username=request.json['username'],
                           phone_number=request.json['phone_number'])
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify(response='OK'), 201)


@app.route('/user/<int:user_id>/update_number', methods=['PATCH'])
def update_phone_number(user_id):
    user = models.User.query.filter_by(id=user_id).first()
    user.phone_number = request.json['phone_number']
    db.session.commit()
    return make_response(jsonify(response='OK'), 200)


@app.route('/user/<int:from_user_id>/get_messages/<int:to_user_id>', methods=['GET'])
def get_messages(from_user_id, to_user_id):
    sent_messages = models.Message.query.filter_by(sender=from_user_id, receiver=to_user_id).all()
    received_messages = models.Message.query.filter_by(sender=to_user_id, receiver=from_user_id).all()
    all_messages = sent_messages + received_messages
    all_messages.sort(key=operator.attrgetter('timestamp'))
    return make_response(jsonify(data=[m.serialize() for m in all_messages]), 200)


@app.route('/send_message', methods=['POST'])
def send_message():
    message = models.Message(text=request.json['message'],
                             sender=request.json['sender'],
                             receiver=request.json['receiver'])
    db.session.add(message)
    db.session.commit()
    return make_response(jsonify(response='OK'), 201)


@app.route('/update_message', methods=['PUT'])
def update_message():
    message = models.Message.query.filter_by(sender=request.json['sender'],
                                             receiver=request.json['receiver'])\
        .order_by(models.Message.timestamp.desc()).first()
    message.text = request.json['message']
    db.session.commit()
    return make_response(jsonify(response='OK'), 200)

