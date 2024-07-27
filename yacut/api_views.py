import re

from flask import jsonify, request

from . import app, db
from .constants import (ERROR_INVALID_ID,
                        ERROR_MISSING_BODY,
                        ERROR_SHORT_ID_EXISTS,
                        ERROR_INVALID_SHORT_ID,
                        SHORT_ID_PATTERN,
                        ERROR_MISSING_URL_FIELD)
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import generate_random_string


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage(ERROR_INVALID_ID, 404)
    return jsonify({'url': url.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_url():
    if request.content_type != 'application/json':
        raise InvalidAPIUsage(ERROR_MISSING_BODY, 400)
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(ERROR_MISSING_BODY, 400)
    if not data or 'url' not in data:
        raise InvalidAPIUsage(ERROR_MISSING_URL_FIELD, 400)

    custom_id = data.get('custom_id')
    if custom_id:
        if len(custom_id) > 16:
            raise InvalidAPIUsage(ERROR_INVALID_SHORT_ID, 400)
        if not re.match(SHORT_ID_PATTERN, custom_id):
            raise InvalidAPIUsage(ERROR_INVALID_SHORT_ID, 400)
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(ERROR_SHORT_ID_EXISTS, 400)
    else:
        custom_id = generate_random_string()

    url = URLMap(original=data['url'], short=custom_id)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201
