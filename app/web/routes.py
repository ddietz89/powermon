from flask import render_template, jsonify

from app import db

from app.web import bp
from app.models import Channel


@bp.route('/', methods=['GET'])
def index():

    # Get the main channel...
    main_channel = Channel.query.get(1).to_dict()



    return render_template('index.html', title='PowerMon', main_channel=main_channel)
