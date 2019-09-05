from flask import jsonify, request
from app.api import bp
from app import db
from app.models import ChannelPackets

@bp.route('/channel_packets/<int:id>', methods=['GET'])
def get_channel_packet(id):
    pass

@bp.route('/channel_packets', methods=['GET'])
def get_channel_packets():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 360, type=int), 360)
    data  = ChannelPackets.to_collection_dict(ChannelPackets.query, page, per_page)
    return jsonify(data)

@bp.route('/channel_packets', methods=['POST'])
def create_channel_packets():
    pass

