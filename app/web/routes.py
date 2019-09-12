from flask import render_template, jsonify
from flask_login import current_user, login_required
from datetime import datetime

from app import db

from app.web import bp
from app.models import Channel

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
	db.session.commit()


@bp.route('/', methods=['GET'])
def index():

    # Get the main channel...
    main_channel = Channel.query.get(1).to_dict()



    return render_template('index.html', title='PowerMon', user=current_user, main_channel=main_channel)
