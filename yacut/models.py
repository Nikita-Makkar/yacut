from datetime import datetime
from urllib.parse import urljoin

from flask import request

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': urljoin(request.url_root, self.short)
        }

    def from_dict(self, data):
        self.original = data.get('original', self.original)
        self.short = data.get('short', self.short)
