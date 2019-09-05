from flask import jsonify, request
from app.api import bp
from app import db
from app.models import ChannelPackets

'''
| id         | int(11)       | NO   | PRI | NULL    | auto_increment |
| channel_id | int(11)       | NO   |     | NULL    |                |
| voltage    | smallint(11)  | NO   |     | NULL    |                |
| seconds    | mediumint(11) | NO   |     | NULL    |                |
| wattsec    | bigint(11)    | NO   |     | NULL    |                |
| datetime   | datetime      | NO   |     | NULL    |                |
'''

@bp.route('/channel_packets/<int:id>', methods=['GET'])
def get_channel_packet(id):
    return jsonify(ChannelPackets.query.get_or_404(id).to_dict())

@bp.route('/channel_packets', methods=['GET'])
def get_channel_packets():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 360, type=int), 360)
    data  = ChannelPackets.to_collection_dict(ChannelPackets.query, page, per_page)
    return jsonify(data)

@bp.route('/channel_packets', methods=['POST'])
def create_channel_packet():
    data = request.get_json() or {}
    if 'channel_id' not in data or 'voltage' not in data or 'seconds' not in data or 'wattsec' not in data:
        return bad_post("Missing required fields.")

    packet = ChannelPacket()
    packet.from_dict(data)
    
    db.session.add(packet)
    db.session.commit()
    
    response = jsonify(packet.to_dict())
    response.status_code = 200
    
    return response
