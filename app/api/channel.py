from flask import jsonify, request
from app.api import bp
from app import db
from app.models import Channel

'''
| id          | int(11)     | NO   | PRI | NULL    | auto_increment |
| name        | varchar(50) | YES  |     | NULL    |                |
| device_id   | int(11)     | NO   |     | NULL    |                |
| channel_num | int(11)     | NO   |     | NULL    |                |
'''

@bp.route('/channels/<int:id>', methods=['GET'])
def get_channel(id):
    return jsonify(Channel.query.get_or_404(id).to_dict())

@bp.route('/channels', methods=['GET'])
def get_channels():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 360, type=int), 360)
    data  = Channel.to_collection_dict(Channel.query, page, per_page)
    return jsonify(data)

@bp.route('/channels', methods=['POST'])
def create_channel():
    data = request.get_json() or {}
    if 'device_id' not in data or 'name' not in data or 'channel_num' not in data:
        return bad_post("Missing required fields.")

	channel = Channel()
	channel.from_dict(data)

	db.session.add(channel)
	db.session.commit()

	response = jsonify(channel.to_dict())
	response.status_code = 200

	return response
