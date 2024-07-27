import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import generate_random_string


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_url():
    if request.content_type != 'application/json':
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    data = request.get_json()
    print("Received data:", data)  # Для отладки
    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса", 400)
    if not data or 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', 400)

    custom_id = data.get('custom_id')
    if custom_id:
        if len(custom_id) > 16:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', 400)
        if not re.match(r'^[A-Za-z0-9]+$', custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки',400)
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.', 400)
    else:
        custom_id = generate_random_string()

    url = URLMap(original=data['url'], short=custom_id)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201

