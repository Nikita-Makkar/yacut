from flask import flash, redirect, render_template

from . import app, db
from .constants import ERROR_SHORT_ID_EXISTS
from .forms import URLForm
from .models import URLMap
from .utils import generate_random_string


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        original_url = form.original_link.data
        custom_id = form.custom_id.data

        if custom_id:
            url_map = URLMap.query.filter_by(short=custom_id).first()
            if url_map:
                flash(ERROR_SHORT_ID_EXISTS)
                return render_template(
                    'index.html',
                    form=form,
                    generated_short_url=None
                )

            url_map = URLMap(original=original_url, short=custom_id)
            db.session.add(url_map)
            db.session.commit()
            generated_short_url = custom_id
        else:
            custom_id = generate_random_string()
            while URLMap.query.filter_by(short=custom_id).first():
                custom_id = generate_random_string()
            url_map = URLMap(original=original_url, short=custom_id)
            db.session.add(url_map)
            db.session.commit()
            generated_short_url = custom_id
        return render_template(
            'index.html', form=form,
            generated_short_url=generated_short_url)
    return render_template('index.html', form=form, generated_short_url=None)


@app.route('/<short_id>')
def redirect_to_original(short_id):
    url_map_object = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map_object.original, code=302)
