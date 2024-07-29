import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .constants import (ERROR_INVALID_ID, ERROR_INVALID_SHORT_ID,
                        ERROR_MISSING_BODY, ERROR_MISSING_URL_FIELD,
                        ERROR_SHORT_ID_EXISTS, MAX_SHORT_ID_LENGTH,
                        SHORT_ID_PATTERN)
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import generate_random_string


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage(ERROR_INVALID_ID, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(ERROR_MISSING_BODY, HTTPStatus.BAD_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage(ERROR_MISSING_URL_FIELD, HTTPStatus.BAD_REQUEST)

    custom_id = data.get('custom_id')
    if custom_id:
        if len(custom_id) > MAX_SHORT_ID_LENGTH:
            raise InvalidAPIUsage(ERROR_INVALID_SHORT_ID, HTTPStatus.BAD_REQUEST)
        if not re.match(SHORT_ID_PATTERN, custom_id):
            raise InvalidAPIUsage(ERROR_INVALID_SHORT_ID, HTTPStatus.BAD_REQUEST)
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(ERROR_SHORT_ID_EXISTS, HTTPStatus.BAD_REQUEST)
    else:
        custom_id = generate_random_string()

    url = URLMap(original=data['url'], short=custom_id)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201
