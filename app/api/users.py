from flask import g, jsonify
from app.api.auth import token_auth
from app.api import bp
from app.auth.models import User

@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())
